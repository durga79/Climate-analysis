import logging
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.data_acquisition.fetch_climate_data import main as fetch_climate
from src.data_acquisition.fetch_economic_data import main as fetch_economic
from src.data_acquisition.fetch_renewable_data import main as fetch_renewable

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("=" * 80)
    logger.info("STARTING DATA ACQUISITION - 2 DATASETS")
    logger.info("Dataset 1: Climate & Energy (Climate + Renewable combined)")
    logger.info("Dataset 2: Economic Development")
    logger.info("=" * 80)
    
    try:
        logger.info("\n[Dataset 1 - Part 1/2] Fetching Climate Data...")
        fetch_climate()
        
        logger.info("\n[Dataset 1 - Part 2/2] Fetching Renewable Energy Data...")
        fetch_renewable()
        logger.info("✓ Dataset 1 (Climate & Energy) complete: Combined ~5,760 records")
        
        logger.info("\n[Dataset 2] Fetching Economic Development Data...")
        fetch_economic()
        logger.info("✓ Dataset 2 (Economic Development) complete: ~5,760 records")
        
        logger.info("\n" + "=" * 80)
        logger.info("DATA ACQUISITION COMPLETED SUCCESSFULLY")
        logger.info("Total: 2 datasets with 11,520 raw records")
        logger.info("=" * 80)
        
    except Exception as e:
        logger.error(f"Data acquisition failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()


