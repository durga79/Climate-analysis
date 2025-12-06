from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError
import logging
from typing import List, Dict, Any, Optional
from config.database_config import MONGODB_CONFIG

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoDBHandler:
    
    def __init__(self):
        self.uri = MONGODB_CONFIG['uri']
        self.db_name = MONGODB_CONFIG['database']
        self.client = None
        self.db = None
        
    def connect(self):
        try:
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=5000)
            self.client.admin.command('ping')
            self.db = self.client[self.db_name]
            logger.info(f"Successfully connected to MongoDB database: {self.db_name}")
            return True
        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            return False
            
    def disconnect(self):
        if self.client:
            self.client.close()
            logger.info("Disconnected from MongoDB")
            
    def insert_many(self, collection_name: str, documents: List[Dict[str, Any]]) -> Optional[List]:
        try:
            collection = self.db[collection_name]
            result = collection.insert_many(documents)
            logger.info(f"Inserted {len(result.inserted_ids)} documents into {collection_name}")
            return result.inserted_ids
        except PyMongoError as e:
            logger.error(f"Error inserting documents into {collection_name}: {e}")
            return None
            
    def insert_one(self, collection_name: str, document: Dict[str, Any]) -> Optional[str]:
        try:
            collection = self.db[collection_name]
            result = collection.insert_one(document)
            logger.info(f"Inserted document into {collection_name}")
            return str(result.inserted_id)
        except PyMongoError as e:
            logger.error(f"Error inserting document into {collection_name}: {e}")
            return None
            
    def find_all(self, collection_name: str, filter_query: Dict = None) -> List[Dict[str, Any]]:
        try:
            collection = self.db[collection_name]
            if filter_query is None:
                filter_query = {}
            documents = list(collection.find(filter_query))
            logger.info(f"Retrieved {len(documents)} documents from {collection_name}")
            return documents
        except PyMongoError as e:
            logger.error(f"Error retrieving documents from {collection_name}: {e}")
            return []
            
    def count_documents(self, collection_name: str, filter_query: Dict = None) -> int:
        try:
            collection = self.db[collection_name]
            if filter_query is None:
                filter_query = {}
            count = collection.count_documents(filter_query)
            logger.info(f"Count in {collection_name}: {count}")
            return count
        except PyMongoError as e:
            logger.error(f"Error counting documents in {collection_name}: {e}")
            return 0
            
    def delete_collection(self, collection_name: str) -> bool:
        try:
            self.db[collection_name].drop()
            logger.info(f"Dropped collection: {collection_name}")
            return True
        except PyMongoError as e:
            logger.error(f"Error dropping collection {collection_name}: {e}")
            return False
            
    def create_index(self, collection_name: str, field: str) -> bool:
        try:
            collection = self.db[collection_name]
            collection.create_index(field)
            logger.info(f"Created index on {field} in {collection_name}")
            return True
        except PyMongoError as e:
            logger.error(f"Error creating index: {e}")
            return False


