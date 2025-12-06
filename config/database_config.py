import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_CONFIG = {
    'uri': os.getenv('MONGODB_URI', 'mongodb://localhost:27017/'),
    'database': os.getenv('MONGODB_DB', 'climate_analytics'),
    'collections': {
        'climate_raw': 'climate_data_raw',
        'economic_raw': 'economic_data_raw',
        'renewable_raw': 'renewable_data_raw'
    }
}

POSTGRES_CONFIG = {
    'uri': os.getenv('POSTGRES_URI', 'postgresql://localhost:5432/climate_analytics'),
    'tables': {
        'countries': 'countries',
        'climate_indicators': 'climate_indicators',
        'economic_indicators': 'economic_indicators',
        'renewable_energy': 'renewable_energy',
        'combined_analysis': 'combined_analysis'
    }
}

API_CONFIG = {
    'world_bank_base': os.getenv('WORLD_BANK_API_BASE', 'https://api.worldbank.org/v2/'),
    'timeout': 30,
    'retry_attempts': 3
}


