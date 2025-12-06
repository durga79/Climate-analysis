import requests
import time
import logging
import sys
import os
from typing import List, Dict, Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from config.database_config import API_CONFIG, MONGODB_CONFIG
from src.database.mongodb_handler import MongoDBHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ClimateDataFetcher:
    
    def __init__(self):
        self.base_url = API_CONFIG['world_bank_base']
        self.timeout = API_CONFIG['timeout']
        self.retry_attempts = API_CONFIG['retry_attempts']
        
    def fetch_indicator_data(self, indicator_code: str, countries: List[str], 
                            start_year: int = 2000, end_year: int = 2023) -> List[Dict[str, Any]]:
        all_data = []
        
        country_str = ';'.join(countries)
        url = f"{self.base_url}country/{country_str}/indicator/{indicator_code}"
        params = {
            'date': f'{start_year}:{end_year}',
            'format': 'json',
            'per_page': 1000
        }
        
        for attempt in range(self.retry_attempts):
            try:
                logger.info(f"Fetching {indicator_code} (attempt {attempt + 1})")
                response = requests.get(url, params=params, timeout=self.timeout)
                response.raise_for_status()
                
                data = response.json()
                
                if len(data) > 1 and data[1]:
                    records = data[1]
                    logger.info(f"Retrieved {len(records)} records for {indicator_code}")
                    all_data.extend(records)
                    break
                else:
                    logger.warning(f"No data returned for {indicator_code}")
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed for {indicator_code}: {e}")
                if attempt < self.retry_attempts - 1:
                    time.sleep(2 ** attempt)
                    
        return all_data
        
    def fetch_climate_indicators(self, countries: List[str]) -> Dict[str, List]:
        indicators = {
            'co2_emissions': 'EN.ATM.CO2E.KT',
            'co2_per_capita': 'EN.ATM.CO2E.PC',
            'energy_use': 'EG.USE.PCAP.KG.OE',
            'fossil_fuel_consumption': 'EG.USE.COMM.FO.ZS',
            'methane_emissions': 'EN.ATM.METH.KT.CE',
            'nitrous_oxide_emissions': 'EN.ATM.NOXE.KT.CE'
        }
        
        climate_data = {}
        
        for name, code in indicators.items():
            logger.info(f"Fetching {name}...")
            data = self.fetch_indicator_data(code, countries)
            climate_data[name] = data
            time.sleep(0.5)
            
        return climate_data
        
    def save_to_mongodb(self, data: Dict[str, List], collection_name: str) -> bool:
        mongo_handler = MongoDBHandler()
        
        if not mongo_handler.connect():
            return False
            
        try:
            mongo_handler.delete_collection(collection_name)
            
            all_records = []
            for indicator_name, records in data.items():
                for record in records:
                    record['indicator_name'] = indicator_name
                    all_records.append(record)
                    
            if all_records:
                mongo_handler.insert_many(collection_name, all_records)
                logger.info(f"Saved {len(all_records)} climate records to MongoDB")
                return True
            else:
                logger.warning("No climate records to save")
                return False
                
        finally:
            mongo_handler.disconnect()

def main():
    countries = ['USA', 'CHN', 'IND', 'DEU', 'GBR', 'FRA', 'JPN', 'CAN', 'AUS', 'BRA',
                'RUS', 'MEX', 'IDN', 'NLD', 'SAU', 'TUR', 'POL', 'BEL', 'SWE', 'NOR',
                'DNK', 'FIN', 'ITA', 'ESP', 'KOR', 'ZAF', 'ARG', 'CHL', 'NZL', 'SGP']
    
    fetcher = ClimateDataFetcher()
    
    logger.info("Starting climate data acquisition...")
    climate_data = fetcher.fetch_climate_indicators(countries)
    
    total_records = sum(len(records) for records in climate_data.values())
    logger.info(f"Total climate records fetched: {total_records}")
    
    collection_name = MONGODB_CONFIG['collections']['climate_raw']
    success = fetcher.save_to_mongodb(climate_data, collection_name)
    
    if success:
        logger.info("Climate data acquisition completed successfully")
    else:
        logger.error("Climate data acquisition failed")

if __name__ == "__main__":
    main()


