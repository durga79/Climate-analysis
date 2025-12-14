import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import sys
import logging

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.database.postgres_handler import PostgresHandler
from src.analysis.ml_models import MachineLearningAnalyzer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def save_fig(fig, filename):
    output_dir = os.path.join(os.path.dirname(__file__), '../../docs/images')
    ensure_dir(output_dir)
    path = os.path.join(output_dir, filename)
    fig.write_image(path, width=1200, height=800, scale=2)
    logger.info(f"Saved image: {path}")

def generate_visualizations():
    logger.info("Connecting to database...")
    pg = PostgresHandler()
    if not pg.connect():
        logger.error("Failed to connect to DB")
        return

    try:
        df = pg.read_table('combined_analysis')
        logger.info(f"Loaded {len(df)} records")
        
        # 1. Trend Line: Energy Use
        logger.info("Generating Trend Line...")
        top_countries = df.groupby('country_name')['climate_energy_use'].mean().nlargest(5).index
        df_trend = df[df['country_name'].isin(top_countries)]
        
        fig_trend = px.line(
            df_trend, x='year', y='climate_energy_use', color='country_name',
            title='Energy Use per Capita Over Time (Top 5 Consumers)',
            labels={'climate_energy_use': 'Energy Use (kg oil eq.)', 'year': 'Year'},
            template='plotly_white'
        )
        save_fig(fig_trend, 'trend_energy_use.png')

        # 2. Correlation Heatmap
        logger.info("Generating Correlation Heatmap...")
        corr_cols = [
            'climate_energy_use', 'climate_fossil_fuel_consumption',
            'economic_gdp_per_capita', 'renewable_renewable_energy_consumption_pct',
            'economic_urban_population_pct'
        ]
        # Filter only numeric columns that exist
        valid_cols = [c for c in corr_cols if c in df.columns]
        corr_matrix = df[valid_cols].corr()
        
        fig_corr = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=valid_cols,
            y=valid_cols,
            colorscale='RdBu', zmid=0,
            text=corr_matrix.values.round(2),
            texttemplate='%{text}'
        ))
        fig_corr.update_layout(title='Correlation Matrix', template='plotly_white')
        save_fig(fig_corr, 'correlation_heatmap.png')

        # 3. ML Clustering Result
        logger.info("Generating Clustering Plot...")
        ml = MachineLearningAnalyzer()
        # Rerun clustering logic to get labels
        # Note: We duplicate logic briefly here or we can use the ML class if it returns the DF
        # Let's use the ML class logic
        df_ml = ml.load_analysis_data()
        labels, results = ml.perform_clustering(df_ml)
        
        # Add labels back to a copy for plotting
        cluster_cols = ['economic_gdp_per_capita', 'renewable_renewable_energy_consumption_pct']
        if 'climate_co2_per_capita' in df_ml.columns:
            cluster_cols.append('climate_co2_per_capita')
        elif 'climate_energy_use' in df_ml.columns:
            cluster_cols.append('climate_energy_use')
            
        valid_indices = df_ml[cluster_cols].dropna().index
        df_ml.loc[valid_indices, 'cluster'] = labels
        df_ml['cluster'] = df_ml['cluster'].astype(str) # For categorical coloring
        
        # Plot Clusters
        fig_cluster = px.scatter(
            df_ml.dropna(subset=['cluster']),
            x='economic_gdp_per_capita',
            y='renewable_renewable_energy_consumption_pct',
            color='cluster',
            hover_data=['country_name'],
            title='K-Means Clustering: GDP vs Renewable Adoption',
            labels={'economic_gdp_per_capita': 'GDP per Capita', 
                    'renewable_renewable_energy_consumption_pct': 'Renewable %'},
            template='plotly_white'
        )
        save_fig(fig_cluster, 'kmeans_clusters.png')

        # 4. Feature Importance
        logger.info("Generating Feature Importance...")
        target = 'climate_co2_per_capita'
        if target not in df_ml.columns:
            target = 'climate_energy_use'
            logger.info(f"Target {target} used for Feature Importance (fallback)")

        if target in df_ml.columns:
            X, y = ml.prepare_features_for_regression(df_ml, target)
            results = ml.train_regression_models(X, y, target)
            rf_results = results.get('Random Forest')
            
            if rf_results and 'feature_importance' in rf_results:
                imp_df = rf_results['feature_importance']
                fig_imp = px.bar(
                    imp_df, x='importance', y='feature', orientation='h',
                    title=f'Random Forest Feature Importance (Predicting {target})',
                    template='plotly_white'
                )
                save_fig(fig_imp, 'feature_importance.png')

    finally:
        pg.disconnect()

if __name__ == "__main__":
    generate_visualizations()

