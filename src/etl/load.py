import pandas as pd
import logging
from typing import Dict
from src.database.postgres_handler import PostgresHandler
from config.database_config import POSTGRES_CONFIG

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataLoader:
    
    def __init__(self):
        self.postgres_handler = PostgresHandler()
        
    def create_countries_table(self, df: pd.DataFrame) -> bool:
        if not self.postgres_handler.connect():
            raise ConnectionError("Failed to connect to PostgreSQL")
            
        try:
            countries_df = df[['country_code', 'country_name']].drop_duplicates()
            
            table_name = POSTGRES_CONFIG['tables']['countries']
            success = self.postgres_handler.create_table_from_dataframe(
                countries_df, table_name, if_exists='replace'
            )
            
            if success:
                logger.info(f"Created countries table with {len(countries_df)} countries")
            return success
            
        finally:
            self.postgres_handler.disconnect()
            
    def load_to_postgres(self, tables: Dict[str, pd.DataFrame]) -> bool:
        if not self.postgres_handler.connect():
            raise ConnectionError("Failed to connect to PostgreSQL")
            
        try:
            for table_type, df in tables.items():
                if df.empty:
                    logger.warning(f"Skipping empty table: {table_type}")
                    continue
                    
                table_name = POSTGRES_CONFIG['tables'].get(table_type, table_type)
                
                success = self.postgres_handler.create_table_from_dataframe(
                    df, table_name, if_exists='replace'
                )
                
                if success:
                    logger.info(f"Loaded {len(df)} records to {table_name}")
                else:
                    logger.error(f"Failed to load {table_type}")
                    return False
                    
            logger.info("All tables loaded successfully to PostgreSQL")
            return True
            
        finally:
            self.postgres_handler.disconnect()
            
    def verify_load(self) -> Dict[str, int]:
        if not self.postgres_handler.connect():
            raise ConnectionError("Failed to connect to PostgreSQL")
            
        try:
            table_names = self.postgres_handler.get_table_names()
            logger.info(f"Tables in database: {table_names}")
            
            record_counts = {}
            for table_name in table_names:
                df = self.postgres_handler.read_table(table_name, f"SELECT COUNT(*) as count FROM {table_name}")
                if df is not None and not df.empty:
                    record_counts[table_name] = df['count'].iloc[0]
                    
            return record_counts
            
        finally:
            self.postgres_handler.disconnect()

def main():
    from src.etl.extract import DataExtractor
    from src.etl.transform import DataTransformer
    
    extractor = DataExtractor()
    raw_data = extractor.extract_all_raw_data()
    
    transformer = DataTransformer()
    combined_df, separate_tables = transformer.transform_all_data(raw_data)
    
    loader = DataLoader()
    
    logger.info("Loading data to PostgreSQL...")
    success = loader.load_to_postgres(separate_tables)
    
    if success:
        logger.info("Creating countries reference table...")
        loader.create_countries_table(combined_df)
        
        logger.info("Verifying data load...")
        record_counts = loader.verify_load()
        
        for table, count in record_counts.items():
            logger.info(f"  {table}: {count} records")
    else:
        logger.error("Data loading failed")
        
    return success

if __name__ == "__main__":
    main()


