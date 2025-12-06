import pandas as pd
import logging
from typing import Dict
from src.database.mongodb_handler import MongoDBHandler
from config.database_config import MONGODB_CONFIG

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataExtractor:
    
    def __init__(self):
        self.mongo_handler = MongoDBHandler()
        
    def extract_from_mongodb(self, collection_name: str) -> pd.DataFrame:
        if not self.mongo_handler.connect():
            raise ConnectionError("Failed to connect to MongoDB")
            
        try:
            documents = self.mongo_handler.find_all(collection_name)
            
            if not documents:
                logger.warning(f"No documents found in {collection_name}")
                return pd.DataFrame()
                
            df = pd.DataFrame(documents)
            
            if '_id' in df.columns:
                df = df.drop('_id', axis=1)
                
            logger.info(f"Extracted {len(df)} records from {collection_name}")
            return df
            
        finally:
            self.mongo_handler.disconnect()
            
    def extract_all_raw_data(self) -> Dict[str, pd.DataFrame]:
        collections = MONGODB_CONFIG['collections']
        
        raw_data = {}
        
        for data_type, collection_name in collections.items():
            logger.info(f"Extracting {data_type}...")
            df = self.extract_from_mongodb(collection_name)
            raw_data[data_type] = df
            
        return raw_data

def main():
    extractor = DataExtractor()
    
    logger.info("Starting data extraction from MongoDB...")
    raw_data = extractor.extract_all_raw_data()
    
    for data_type, df in raw_data.items():
        logger.info(f"{data_type}: {len(df)} records, {df.shape[1]} columns")
        
    return raw_data

if __name__ == "__main__":
    main()


