from pymongo import MongoClient
from datetime import datetime, timezone


class AtlasClient:

    def __init__(self, altas_uri, dbname, video_metadata, account_details):
        self.mongodb_client = MongoClient(altas_uri, maxPoolSize=5, minPoolSize=1, serverSelectionTimeoutMS=5000)
        self.database = self.mongodb_client[dbname]
        self.video_metadata = video_metadata
        self.account_details = account_details
        
    def find_video_metadata(self, s3_key: str):
        collection = self.database[self.video_metadata]
        filter = {"s3_key": s3_key}
        item = collection.find_one(filter=filter)
        return item
    
    def find_account_details(self, discord_id: str):
        collection = self.database[self.account_details]
        filter = {"discord_id": discord_id}
        return collection.find_one(filter=filter)
    
    def upsert_index_id(self, discord_id: str, index_id: str):
        collection = self.database[self.account_details]
        document = {
            "discord_id": discord_id,
            "index_id": index_id,
            "created_at": datetime.now(timezone.utc)
        }
        collection.update_one({"discord_id": discord_id}, {"$set": document}, upsert=True)
    
    def update_video_metadata(self, s3_key: str, fields: dict):
        collection = self.database[self.video_metadata]
        collection.update_one({"s3_key": s3_key}, {"$set": fields})
