from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
import logging
from typing import Optional, List
from config.database_config import POSTGRES_CONFIG

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PostgresHandler:
    
    def __init__(self):
        self.uri = POSTGRES_CONFIG['uri']
        self.engine = None
        
    def connect(self):
        try:
            self.engine = create_engine(self.uri)
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("Successfully connected to PostgreSQL database")
            return True
        except SQLAlchemyError as e:
            logger.error(f"Failed to connect to PostgreSQL: {e}")
            return False
            
    def disconnect(self):
        if self.engine:
            self.engine.dispose()
            logger.info("Disconnected from PostgreSQL")
            
    def execute_query(self, query: str, params: dict = None) -> bool:
        try:
            with self.engine.connect() as conn:
                conn.execute(text(query), params or {})
                conn.commit()
            logger.info("Query executed successfully")
            return True
        except SQLAlchemyError as e:
            logger.error(f"Error executing query: {e}")
            return False
            
    def create_table_from_dataframe(self, df: pd.DataFrame, table_name: str, 
                                   if_exists: str = 'replace') -> bool:
        try:
            df.to_sql(table_name, self.engine, if_exists=if_exists, index=False)
            logger.info(f"Created/updated table {table_name} with {len(df)} records")
            return True
        except SQLAlchemyError as e:
            logger.error(f"Error creating table {table_name}: {e}")
            return False
            
    def read_table(self, table_name: str, query: str = None) -> Optional[pd.DataFrame]:
        try:
            if query is None:
                query = f"SELECT * FROM {table_name}"
            df = pd.read_sql(query, self.engine)
            logger.info(f"Retrieved {len(df)} records from {table_name}")
            return df
        except SQLAlchemyError as e:
            logger.error(f"Error reading table {table_name}: {e}")
            return None
            
    def table_exists(self, table_name: str) -> bool:
        inspector = inspect(self.engine)
        return table_name in inspector.get_table_names()
        
    def get_table_names(self) -> List[str]:
        inspector = inspect(self.engine)
        return inspector.get_table_names()
        
    def drop_table(self, table_name: str) -> bool:
        try:
            with self.engine.connect() as conn:
                conn.execute(text(f"DROP TABLE IF EXISTS {table_name} CASCADE"))
                conn.commit()
            logger.info(f"Dropped table: {table_name}")
            return True
        except SQLAlchemyError as e:
            logger.error(f"Error dropping table {table_name}: {e}")
            return False


