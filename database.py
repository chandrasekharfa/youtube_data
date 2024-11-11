from pymongo import MongoClient
from datetime import datetime
from fastapi import HTTPException


client = MongoClient("mongodb://localhost:27017/")
db = client["youtube_stats"]
collection = db["video_stats"]

def save_video_stats_to_db(video_data):
    """
    Save new video stats to the MongoDB collection.
    """
    try:
        video_data["created_at"] = datetime.utcnow()
        video_data["last_updated_at"] = datetime.utcnow()
        result = collection.insert_one(video_data)
        return str(result.inserted_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error saving data to MongoDB: " + str(e))


def update_video_stats_in_db(video_id, updated_data):
    """
    Update existing video stats in the MongoDB collection.
    """
    collection.update_one(
        {"_id": video_id},
        {"$set": updated_data}
    )
