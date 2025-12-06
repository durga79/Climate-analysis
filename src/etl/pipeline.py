import logging
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.etl.extract import DataExtractor
from src.etl.transform import DataTransformer
from src.etl.load import DataLoader

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_etl_pipeline():
    logger.info("=" * 80)
    logger.info("STARTING ETL PIPELINE - 2 DATASETS")
    logger.info("Dataset 1: Climate & Energy (Climate + Renewable combined)")
    logger.info("Dataset 2: Economic Development")
    logger.info("=" * 80)
    
    try:
        logger.info("\n[STEP 1/3] EXTRACT - Reading data from MongoDB...")
        extractor = DataExtractor()
        raw_data = extractor.extract_all_raw_data()
        
        total_records = sum(len(df) for df in raw_data.values())
        logger.info(f"Extracted total of {total_records} raw records")
        
        logger.info("\n[STEP 2/3] TRANSFORM - Cleaning and transforming data...")
        transformer = DataTransformer()
        combined_df, separate_tables = transformer.transform_all_data(raw_data)
        
        logger.info(f"Transformed data shape: {combined_df.shape}")
        logger.info(f"Number of tables: {len(separate_tables)}")
        
        logger.info("\n[STEP 3/3] LOAD - Loading data to PostgreSQL...")
        loader = DataLoader()
        success = loader.load_to_postgres(separate_tables)
        
        if success:
            loader.create_countries_table(combined_df)
            
            logger.info("\nVerifying data load...")
            record_counts = loader.verify_load()
            
            logger.info("\n" + "=" * 80)
            logger.info("ETL PIPELINE COMPLETED SUCCESSFULLY")
            logger.info("=" * 80)
            logger.info("\nFinal Record Counts:")
            for table, count in record_counts.items():
                logger.info(f"  {table}: {count:,} records")
        else:
            raise Exception("Data loading failed")
            
    except Exception as e:
        logger.error(f"ETL Pipeline failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_etl_pipeline()


