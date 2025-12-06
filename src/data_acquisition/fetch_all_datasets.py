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
    logger.info("STARTING COMPLETE DATA ACQUISITION PIPELINE")
    logger.info("=" * 80)
    
    try:
        logger.info("\n[1/3] Fetching Climate Data...")
        fetch_climate()
        
        logger.info("\n[2/3] Fetching Economic Data...")
        fetch_economic()
        
        logger.info("\n[3/3] Fetching Renewable Energy Data...")
        fetch_renewable()
        
        logger.info("\n" + "=" * 80)
        logger.info("DATA ACQUISITION COMPLETED SUCCESSFULLY")
        logger.info("=" * 80)
        
    except Exception as e:
        logger.error(f"Data acquisition failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()


