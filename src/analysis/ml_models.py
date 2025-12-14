import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import KMeans
from sklearn.metrics import r2_score, mean_squared_error, silhouette_score
import logging
import sys
import os
from typing import Dict, Tuple, List

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.database.postgres_handler import PostgresHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MachineLearningAnalyzer:
    
    def __init__(self):
        self.postgres_handler = PostgresHandler()
        self.models = {}
        self.results = {}
        
    def load_analysis_data(self) -> pd.DataFrame:
        if not self.postgres_handler.connect():
            raise ConnectionError("Failed to connect to PostgreSQL")
            
        try:
            df = self.postgres_handler.read_table('combined_analysis')
            logger.info(f"Loaded {len(df)} records for ML analysis")
            return df
        finally:
            self.postgres_handler.disconnect()
            
    def prepare_features_for_regression(self, df: pd.DataFrame, 
                                        target: str) -> Tuple[pd.DataFrame, pd.Series]:
        feature_columns = [
            'economic_gdp_per_capita',
            'economic_gdp_growth',
            'economic_population',
            'economic_urban_population_pct',
            'economic_industry_value_added_pct',
            'renewable_renewable_energy_consumption_pct',
            'climate_energy_use',
            'climate_fossil_fuel_consumption'
        ]
        
        available_features = [col for col in feature_columns 
                            if col in df.columns and col != target]
        
        data = df[available_features + [target]].dropna()
        
        X = data[available_features]
        y = data[target]
        
        logger.info(f"Prepared {len(X)} samples with {len(available_features)} features for {target}")
        
        return X, y
        
    def train_regression_models(self, X: pd.DataFrame, y: pd.Series, 
                               target_name: str) -> Dict:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        models = {
            'Linear Regression': LinearRegression(),
            'Ridge Regression': Ridge(alpha=1.0),
            'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42)
        }
        
        results = {}
        
        for model_name, model in models.items():
            logger.info(f"Training {model_name}...")
            
            if model_name == 'Random Forest':
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
            else:
                model.fit(X_train_scaled, y_train)
                y_pred = model.predict(X_test_scaled)
                
            r2 = r2_score(y_test, y_pred)
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            
            results[model_name] = {
                'r2_score': r2,
                'rmse': rmse,
                'model': model
            }
            
            logger.info(f"  {model_name} - R²: {r2:.4f}, RMSE: {rmse:.2f}")
            
            if model_name == 'Random Forest':
                feature_importance = pd.DataFrame({
                    'feature': X.columns,
                    'importance': model.feature_importances_
                }).sort_values('importance', ascending=False)
                
                results[model_name]['feature_importance'] = feature_importance
                logger.info(f"  Top 3 features: {list(feature_importance['feature'].head(3))}")
                
        self.models[target_name] = results
        return results
        
    def perform_clustering(self, df: pd.DataFrame, n_clusters: int = 4) -> Tuple[np.ndarray, Dict]:
        feature_columns = [
            'economic_gdp_per_capita',
            'renewable_renewable_energy_consumption_pct',
            'climate_energy_use'
        ]
        
        if 'climate_co2_per_capita' in df.columns:
            feature_columns.append('climate_co2_per_capita')
        
        available_features = [col for col in feature_columns if col in df.columns]
        
        data = df[available_features].dropna()
        
        scaler = StandardScaler()
        data_scaled = scaler.fit_transform(data)
        
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(data_scaled)
        
        silhouette_avg = silhouette_score(data_scaled, cluster_labels)
        
        cluster_centers = scaler.inverse_transform(kmeans.cluster_centers_)
        
        centers_df = pd.DataFrame(cluster_centers, columns=available_features)
        centers_df['cluster'] = range(n_clusters)
        
        logger.info(f"Clustering completed: {n_clusters} clusters")
        logger.info(f"Silhouette score: {silhouette_avg:.3f}")
        
        results = {
            'labels': cluster_labels,
            'centers': centers_df,
            'silhouette_score': silhouette_avg,
            'n_clusters': n_clusters
        }
        
        self.results['clustering'] = results
        
        return cluster_labels, results
        
    def identify_sustainability_leaders(self, df: pd.DataFrame) -> pd.DataFrame:
        required_cols = ['climate_co2_per_capita', 'economic_gdp_per_capita', 
                        'renewable_renewable_energy_consumption_pct']
        
        if not all(col in df.columns for col in required_cols):
            logger.warning("Missing required columns for sustainability analysis")
            return pd.DataFrame()
            
        recent_year = df['year'].max()
        recent_data = df[df['year'] == recent_year].copy()
        
        recent_data['co2_percentile'] = recent_data['climate_co2_per_capita'].rank(pct=True)
        recent_data['renewable_percentile'] = recent_data['renewable_renewable_energy_consumption_pct'].rank(pct=True)
        
        recent_data['sustainability_score'] = (
            (1 - recent_data['co2_percentile']) * 0.5 + 
            recent_data['renewable_percentile'] * 0.5
        )
        
        leaders = recent_data.nlargest(10, 'sustainability_score')[
            ['country_name', 'climate_co2_per_capita', 'renewable_renewable_energy_consumption_pct',
             'economic_gdp_per_capita', 'sustainability_score']
        ]
        
        logger.info(f"Identified top 10 sustainability leaders for {recent_year}")
        self.results['sustainability_leaders'] = leaders
        
        return leaders
        
    def run_complete_ml_analysis(self) -> Dict:
        logger.info("=" * 80)
        logger.info("STARTING MACHINE LEARNING ANALYSIS")
        logger.info("=" * 80)
        
        df = self.load_analysis_data()
        
        logger.info("\n[1/3] Regression Analysis...")
        
        if 'climate_co2_per_capita' in df.columns:
            logger.info("\nPredicting CO2 per capita...")
            X, y = self.prepare_features_for_regression(df, 'climate_co2_per_capita')
            co2_results = self.train_regression_models(X, y, 'co2_per_capita')
            self.results['co2_regression'] = co2_results
            
        logger.info("\n[2/3] Clustering Analysis...")
        cluster_labels, cluster_results = self.perform_clustering(df)
        
        df_clustered = df.copy()
        
        # Use available columns for clustering context
        cluster_cols = ['economic_gdp_per_capita', 'renewable_renewable_energy_consumption_pct']
        if 'climate_co2_per_capita' in df.columns:
            cluster_cols.append('climate_co2_per_capita')
        elif 'climate_energy_use' in df.columns:
             cluster_cols.append('climate_energy_use')
            
        valid_indices = df[cluster_cols].dropna().index
        df_clustered.loc[valid_indices, 'cluster'] = cluster_labels
        
        logger.info("\n[3/3] Sustainability Leaders Identification...")
        leaders = self.identify_sustainability_leaders(df)
        
        logger.info("\n" + "=" * 80)
        logger.info("MACHINE LEARNING ANALYSIS COMPLETED")
        logger.info("=" * 80)
        
        return self.results

def main():
    analyzer = MachineLearningAnalyzer()
    results = analyzer.run_complete_ml_analysis()
    
    logger.info("\nML Analysis Summary:")
    logger.info(f"  Results generated: {list(results.keys())}")
    
    return results

if __name__ == "__main__":
    main()


