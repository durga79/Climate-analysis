import pandas as pd
import numpy as np
import logging
from typing import Dict, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataTransformer:
    
    def clean_world_bank_data(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df
            
        df_clean = df.copy()
        
        df_clean['year'] = df_clean['date'].astype(int)
        df_clean['country_code'] = df_clean['countryiso3code']
        df_clean['country_name'] = df_clean['country'].apply(lambda x: x.get('value') if isinstance(x, dict) else x)
        df_clean['indicator_id'] = df_clean['indicator'].apply(lambda x: x.get('id') if isinstance(x, dict) else None)
        df_clean['metric_value'] = pd.to_numeric(df_clean['value'], errors='coerce')
        
        columns_to_keep = ['year', 'country_code', 'country_name', 'indicator_name', 
                          'indicator_id', 'metric_value']
        df_clean = df_clean[columns_to_keep]
        
        df_clean = df_clean.dropna(subset=['metric_value'])
        
        df_clean = df_clean.drop_duplicates(subset=['year', 'country_code', 'indicator_name'])
        
        logger.info(f"Cleaned data: {len(df_clean)} records remaining")
        return df_clean
        
    def pivot_indicators(self, df: pd.DataFrame, prefix: str) -> pd.DataFrame:
        if df.empty:
            return df
            
        pivot_df = df.pivot_table(
            index=['year', 'country_code', 'country_name'],
            columns='indicator_name',
            values='metric_value',
            aggfunc='first'
        ).reset_index()
        
        pivot_df.columns.name = None
        
        indicator_cols = [col for col in pivot_df.columns 
                         if col not in ['year', 'country_code', 'country_name']]
        rename_dict = {col: f"{prefix}_{col}" for col in indicator_cols}
        pivot_df = pivot_df.rename(columns=rename_dict)
        
        logger.info(f"Pivoted {prefix} data: {pivot_df.shape}")
        return pivot_df
        
    def merge_datasets(self, climate_df: pd.DataFrame, economic_df: pd.DataFrame, 
                      renewable_df: pd.DataFrame) -> pd.DataFrame:
        merge_keys = ['year', 'country_code', 'country_name']
        
        combined_df = climate_df.merge(economic_df, on=merge_keys, how='outer')
        combined_df = combined_df.merge(renewable_df, on=merge_keys, how='outer')
        
        combined_df = combined_df.sort_values(['country_code', 'year'])
        
        logger.info(f"Merged dataset: {combined_df.shape}")
        return combined_df
        
    def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        df_filled = df.copy()
        
        numeric_cols = df_filled.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            missing_pct = df_filled[col].isnull().sum() / len(df_filled) * 100
            if missing_pct > 0:
                logger.info(f"{col}: {missing_pct:.2f}% missing")
        
        df_filled = df_filled.groupby('country_code').apply(
            lambda group: group.fillna(method='ffill').fillna(method='bfill')
        ).reset_index(drop=True)
        
        threshold = 0.5
        df_filled = df_filled.dropna(thresh=int(threshold * len(df_filled.columns)))
        
        logger.info(f"After handling missing values: {df_filled.shape}")
        return df_filled
        
    def create_derived_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df_features = df.copy()
        
        if 'climate_co2_emissions' in df_features.columns and 'economic_gdp_current_usd' in df_features.columns:
            df_features['co2_per_gdp'] = (
                df_features['climate_co2_emissions'] / 
                (df_features['economic_gdp_current_usd'] / 1e9)
            )
            
        if 'renewable_renewable_energy_consumption_pct' in df_features.columns:
            df_features['renewable_adoption_category'] = pd.cut(
                df_features['renewable_renewable_energy_consumption_pct'],
                bins=[0, 20, 40, 60, 100],
                labels=['Low', 'Medium', 'High', 'Very High']
            )
            
        if 'economic_gdp_per_capita' in df_features.columns:
            df_features['gdp_per_capita_category'] = pd.cut(
                df_features['economic_gdp_per_capita'],
                bins=[0, 5000, 15000, 40000, np.inf],
                labels=['Low Income', 'Lower Middle', 'Upper Middle', 'High Income']
            )
            
        logger.info(f"Created derived features: {df_features.shape}")
        return df_features
        
    def transform_all_data(self, raw_data: Dict[str, pd.DataFrame]) -> Tuple[pd.DataFrame, Dict[str, pd.DataFrame]]:
        logger.info("Starting data transformation...")
        
        climate_clean = self.clean_world_bank_data(raw_data.get('climate_raw', pd.DataFrame()))
        economic_clean = self.clean_world_bank_data(raw_data.get('economic_raw', pd.DataFrame()))
        renewable_clean = self.clean_world_bank_data(raw_data.get('renewable_raw', pd.DataFrame()))
        
        climate_pivot = self.pivot_indicators(climate_clean, 'climate')
        economic_pivot = self.pivot_indicators(economic_clean, 'economic')
        renewable_pivot = self.pivot_indicators(renewable_clean, 'renewable')
        
        combined = self.merge_datasets(climate_pivot, economic_pivot, renewable_pivot)
        
        combined = self.handle_missing_values(combined)
        
        combined = self.create_derived_features(combined)
        
        separate_tables = {
            'climate_indicators': climate_pivot,
            'economic_indicators': economic_pivot,
            'renewable_energy': renewable_pivot,
            'combined_analysis': combined
        }
        
        logger.info("Data transformation completed successfully")
        return combined, separate_tables

def main():
    from src.etl.extract import DataExtractor
    
    extractor = DataExtractor()
    raw_data = extractor.extract_all_raw_data()
    
    transformer = DataTransformer()
    combined_df, separate_tables = transformer.transform_all_data(raw_data)
    
    logger.info(f"Final combined dataset: {combined_df.shape}")
    logger.info(f"Columns: {list(combined_df.columns)}")
    
    return combined_df, separate_tables

if __name__ == "__main__":
    main()


