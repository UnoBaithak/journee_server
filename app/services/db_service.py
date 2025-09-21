import logging
from typing import Optional
from pymongo import MongoClient
import os
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class DBService():
    _instance: Optional["DBService"] = None
    _client: Optional[MongoClient] = None
    _db = None

    def __new__(cls, *args, **kwargs):
        """Singleton Pattern: Ensure only one instance is created"""
        if cls._instance is None:
            cls._instance = super(DBService, cls).__new__(cls)
            cls._instance._initialize_db()
        return cls._instance

    def _initialize_db(self):
        """Initialize MongoDB connection and select database"""
        try:
            logger.info("Initializing MongoDB connection...")
            MONGO_URL = os.getenv("MONGO_URL")
            self._client = MongoClient(MONGO_URL)
            self._db = self._client["journee"]
            logger.info("MongoDB connection established successfully!")
        except Exception as e:
            logger.error(f"Error connecting to MongoDB: {str(e)}")
            raise
    
    def get_collection(self, collection_name: str):
        """Get a MongoDB collection by name"""
        if self._db is None:
            raise RuntimeError("Database not initialized.")
        return self._db[collection_name]

    def close_connection(self):
        """Gracefully close MongoDB connection"""
        if self._client:
            self._client.close()
            logger.info("MongoDB connection closed successfully!")

    
        