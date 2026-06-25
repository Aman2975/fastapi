"""
Database connection and utilities
"""
from pymongo import MongoClient
from app.config import settings

# MongoDB client
client = None
db = None
users_collection = None


def connect_to_mongo():
    """Connect to MongoDB"""
    global client, db, users_collection
    try:
        client = MongoClient(settings.MONGODB_URI)
        db = client[settings.DATABASE_NAME]
        users_collection = db["users"]
        
        # Create index on email for faster queries
        users_collection.create_index("email", unique=True)
        
        print("✓ MongoDB connected successfully")
        return True
    except Exception as e:
        print(f"✗ MongoDB connection failed: {e}")
        return False


def close_mongo_connection():
    """Close MongoDB connection"""
    global client
    if client:
        client.close()
        print("✓ MongoDB connection closed")


def get_database():
    """Get database instance"""
    return db


def get_users_collection():
    """Get users collection"""
    return users_collection
