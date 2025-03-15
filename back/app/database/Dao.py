from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.config import Config
from bson import ObjectId
from typing import Optional, Dict, Any

import datetime


def get_database(config_class=Config):
    client = AsyncIOMotorClient(config_class.MONGO_URI)
    db = client.get_default_database()

    return db

class MongoDB:
    _client: Optional[AsyncIOMotorClient] = None
    _db: Optional[AsyncIOMotorDatabase] = None

    @classmethod
    def connect(cls, config_class=Config):
        """Establish a singleton connection to the MongoDB server."""
        if cls._client is None:
            cls._client = AsyncIOMotorClient(config_class.MONGO_URI)
            cls._db = cls._client.get_database()  # Uses the default database from URI

    @classmethod
    def get_database(cls) -> AsyncIOMotorDatabase:
        """Return the singleton database instance."""
        if cls._db is None:
            raise RuntimeError(
                "Database connection has not been initialized. Call MongoDB.connect() first."
            )
        return cls._db

MongoDB.connect()

class DAO:
    """Data Access Object for interacting with MongoDB collections."""

    @staticmethod
    def serialize_document(doc: Any) -> Any:
        """
        Recursively converts ObjectId to string in a MongoDB document.
        """
        if isinstance(doc, dict):
            return {key: DAO.serialize_document(value) for key, value in doc.items()}
        elif isinstance(doc, list):
            return [DAO.serialize_document(item) for item in doc]
        elif isinstance(doc, ObjectId):
            return str(doc)
        return doc

    @staticmethod
    async def insert_db(collection_name: str, document: Dict) -> Optional[str]:
        """Insert a document and return its inserted ID."""
        try:
            db = MongoDB.get_database()
            result = await db[collection_name].insert_one(document)
            return str(result.inserted_id) if result.acknowledged else None
        except Exception as e:
            print(f"Insert Error: {e}")
            return None

    @staticmethod
    async def find_db(collection_name: str, key: str, value: Any) -> Optional[Dict]:
        """Find a single document by key-value pair."""
        try:
            db = MongoDB.get_database()
            document = await db[collection_name].find_one({key: value})
            return DAO.serialize_document(document) if document else None
        except Exception as e:
            print(f"Find Error: {e}")
            return None

    @staticmethod
    async def update_db(
        collection_name: str, key: str, value: Any, updated_document: Dict
    ) -> bool:
        """Update a document and return True if modified."""
        try:
            db = MongoDB.get_database()
            result = await db[collection_name].update_one(
                {key: value}, {"$set": updated_document}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Update Error: {e}")
            return False
    
    @staticmethod
    async def insert_google_account(account):
        return await get_database().google.insert_one(account)

    @staticmethod
    async def update_user(username, updated_user):
        updated_user["updated_at"] = datetime.datetime.now()
        return await get_database().users.update_one({"username": username}, {"$set": updated_user})

    @staticmethod
    async def find_all_users():
        return await get_database().users.find({}).to_list(length=None)

    @staticmethod
    async def find_user_by_email(username):
        return await get_database().users.find_one({"email": username})

    @staticmethod
    async def find_user_by_username(username):
        return await get_database().users.find_one({"username": username})

    @staticmethod
    async def delete_user_by_username(username):
        return await get_database().users.delete_one({"username": username})


    # Areas
    @staticmethod
    async def insert_area(area):
        return await get_database().areas.insert_one(area)

    @staticmethod
    async def update_area(_id, updated_area):
        return await get_database().areas.update_one({"_id": ObjectId(_id)}, {"$set": updated_area})

    @staticmethod
    async def find_area_by_id(_id):
        return await get_database().areas.find_one({"_id": ObjectId(_id)})

    @staticmethod
    async def delete_area_by_id(_id):
        return await get_database().areas.delete_one({"_id": ObjectId(_id)})

    @staticmethod
    async def find_all_areas():
        documents = await get_database().areas.find({}).to_list(length=None)
        return [DAO.serialize_document(doc) for doc in documents]

    @staticmethod
    async def insert(database, document):
        return await database.insert_one(document)

    @staticmethod
    async def find(database, key, value):
        return await database.find_one({key: value})

    @staticmethod
    async def update(database, key, value, updated_document):
        return await database.update_one({key: value}, {"$set": updated_document})

    # Github actions
    @staticmethod
    async def set_user_github_repo_star_count(email, repo, star_count):
        return await get_database().users.update_one({"email": email}, {"$set": {f"github_repos.{repo}.star_count": star_count}})

    @staticmethod
    async def get_user_github_repo_star_count(user_email, repo_name):
        user = await DAO.find_user_by_email(user_email)
        if not user:
            return 0

        keys = f"github_repos.{repo_name}.star_count".split('.')
        value = user
        for key in keys:
            value = value.get(key, {})
            if not value:
                return 0
        return value

    @staticmethod
    async def set_user_github_repo_fork_count(email, repo, fork_count):
        return await get_database().users.update_one({"email": email}, {"$set": {f"github_repos.{repo}.fork_count": fork_count}})

    @staticmethod
    async def get_user_github_repo_fork_count(user_email, repo_name):
        user = await DAO.find_user_by_email(user_email)
        if not user:
            return 0

        keys = f"github_repos.{repo_name}.fork_count".split('.')
        value = user
        for key in keys:
            value = value.get(key, {})
            if not value:
                return 0
        return value
