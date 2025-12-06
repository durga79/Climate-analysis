import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import pearsonr, spearmanr
import logging
import sys
import os
from typing import Dict, List, Tuple

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.database.postgres_handler import PostgresHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StatisticalAnalyzer:
    
    def __init__(self):
        self.postgres_handler = PostgresHandler()
        self.results = {}
        
    def load_analysis_data(self) -> pd.DataFrame:
        if not self.postgres_handler.connect():
            raise ConnectionError("Failed to connect to PostgreSQL")
            
        try:
            df = self.postgres_handler.read_table('combined_analysis')
            logger.info(f"Loaded {len(df)} records for analysis")
            return df
        finally:
            self.postgres_handler.disconnect()
            
    def descriptive_statistics(self, df: pd.DataFrame) -> pd.DataFrame:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        desc_stats = df[numeric_cols].describe()
        
        desc_stats.loc['median'] = df[numeric_cols].median()
        desc_stats.loc['skewness'] = df[numeric_cols].skew()
        desc_stats.loc['kurtosis'] = df[numeric_cols].kurtosis()
        
        logger.info("Calculated descriptive statistics")
        self.results['descriptive_stats'] = desc_stats
        
        return desc_stats
        
    def correlation_analysis(self, df: pd.DataFrame) -> pd.DataFrame:
        key_columns = [
            'climate_co2_emissions',
            'climate_co2_per_capita',
            'economic_gdp_current_usd',
            'economic_gdp_per_capita',
            'economic_gdp_growth',
            'renewable_renewable_energy_consumption_pct',
            'renewable_renewable_electricity_output_pct'
        ]
        
        available_cols = [col for col in key_columns if col in df.columns]
        
        correlation_matrix = df[available_cols].corr()
        
        logger.info("Calculated correlation matrix")
        self.results['correlation_matrix'] = correlation_matrix
        
        return correlation_matrix
        
    def test_correlation_significance(self, df: pd.DataFrame, 
                                     var1: str, var2: str) -> Dict:
        clean_df = df[[var1, var2]].dropna()
        
        if len(clean_df) < 3:
            logger.warning(f"Insufficient data for correlation test between {var1} and {var2}")
            return {}
            
        pearson_r, pearson_p = pearsonr(clean_df[var1], clean_df[var2])
        spearman_r, spearman_p = spearmanr(clean_df[var1], clean_df[var2])
        
        result = {
            'variables': f"{var1} vs {var2}",
            'pearson_correlation': pearson_r,
            'pearson_pvalue': pearson_p,
            'spearman_correlation': spearman_r,
            'spearman_pvalue': spearman_p,
            'sample_size': len(clean_df),
            'pearson_significant': pearson_p < 0.05,
            'spearman_significant': spearman_p < 0.05
        }
        
        logger.info(f"Correlation test: {var1} vs {var2}")
        logger.info(f"  Pearson r={pearson_r:.3f}, p={pearson_p:.4f}")
        logger.info(f"  Spearman r={spearman_r:.3f}, p={spearman_p:.4f}")
        
        return result
        
    def test_group_differences(self, df: pd.DataFrame, 
                              grouping_var: str, test_var: str) -> Dict:
        groups = df.groupby(grouping_var)[test_var].apply(list)
        
        if len(groups) < 2:
            logger.warning(f"Insufficient groups for comparison")
            return {}
            
        group_data = [group for group in groups if len(group) > 0]
        
        if len(group_data) >= 2:
            f_stat, p_value = stats.f_oneway(*group_data)
            
            result = {
                'grouping_variable': grouping_var,
                'test_variable': test_var,
                'f_statistic': f_stat,
                'p_value': p_value,
                'significant': p_value < 0.05,
                'num_groups': len(group_data)
            }
            
            logger.info(f"ANOVA test: {test_var} across {grouping_var}")
            logger.info(f"  F={f_stat:.3f}, p={p_value:.4f}")
            
            return result
        else:
            logger.warning("Insufficient data for ANOVA test")
            return {}
            
    def analyze_trends_over_time(self, df: pd.DataFrame, 
                                 metric: str, countries: List[str] = None) -> pd.DataFrame:
        if countries is None:
            countries = df['country_code'].unique()[:10]
            
        trend_df = df[df['country_code'].isin(countries)].copy()
        
        trends = []
        for country in countries:
            country_data = trend_df[trend_df['country_code'] == country].sort_values('year')
            
            if len(country_data) < 2 or metric not in country_data.columns:
                continue
                
            clean_data = country_data[['year', metric]].dropna()
            
            if len(clean_data) >= 2:
                slope, intercept, r_value, p_value, std_err = stats.linregress(
                    clean_data['year'], clean_data[metric]
                )
                
                trends.append({
                    'country_code': country,
                    'metric': metric,
                    'slope': slope,
                    'r_squared': r_value ** 2,
                    'p_value': p_value,
                    'significant': p_value < 0.05
                })
                
        trends_df = pd.DataFrame(trends)
        
        logger.info(f"Analyzed trends for {metric} across {len(trends)} countries")
        self.results[f'trends_{metric}'] = trends_df
        
        return trends_df
        
    def run_complete_analysis(self) -> Dict:
        logger.info("=" * 80)
        logger.info("STARTING STATISTICAL ANALYSIS")
        logger.info("=" * 80)
        
        df = self.load_analysis_data()
        
        logger.info("\n[1/5] Descriptive Statistics...")
        desc_stats = self.descriptive_statistics(df)
        
        logger.info("\n[2/5] Correlation Analysis...")
        corr_matrix = self.correlation_analysis(df)
        
        logger.info("\n[3/5] Significance Testing...")
        correlation_tests = []
        
        test_pairs = [
            ('climate_co2_per_capita', 'economic_gdp_per_capita'),
            ('renewable_renewable_energy_consumption_pct', 'climate_co2_per_capita'),
            ('economic_gdp_per_capita', 'renewable_renewable_energy_consumption_pct')
        ]
        
        for var1, var2 in test_pairs:
            if var1 in df.columns and var2 in df.columns:
                result = self.test_correlation_significance(df, var1, var2)
                if result:
                    correlation_tests.append(result)
                    
        self.results['correlation_tests'] = pd.DataFrame(correlation_tests)
        
        logger.info("\n[4/5] Group Differences Analysis...")
        if 'renewable_adoption_category' in df.columns and 'climate_co2_per_capita' in df.columns:
            group_test = self.test_group_differences(
                df, 'renewable_adoption_category', 'climate_co2_per_capita'
            )
            self.results['group_test'] = group_test
            
        logger.info("\n[5/5] Trend Analysis...")
        trend_metrics = ['climate_co2_per_capita', 'renewable_renewable_energy_consumption_pct']
        
        for metric in trend_metrics:
            if metric in df.columns:
                trends = self.analyze_trends_over_time(df, metric)
                
        logger.info("\n" + "=" * 80)
        logger.info("STATISTICAL ANALYSIS COMPLETED")
        logger.info("=" * 80)
        
        return self.results

def main():
    analyzer = StatisticalAnalyzer()
    results = analyzer.run_complete_analysis()
    
    logger.info("\nAnalysis Summary:")
    logger.info(f"  Results generated: {list(results.keys())}")
    
    return results

if __name__ == "__main__":
    main()


