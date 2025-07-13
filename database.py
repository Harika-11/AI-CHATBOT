# database.py

from pymongo import MongoClient, ASCENDING, DESCENDING
from datetime import datetime

class MongoDatabaseManager:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="chatbot"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.chat_history = self.db["chat_history"]
        self.sessions = self.db["sessions"]

        self.chat_history.create_index([("session_id", ASCENDING), ("timestamp", DESCENDING)])
        self.sessions.create_index("session_id", unique=True)

    def save_message(self, session_id, user_message, bot_response):
        self.chat_history.insert_one({
            "session_id": session_id,
            "user_message": user_message,
            "bot_response": bot_response,
            "timestamp": datetime.utcnow()
        })
        self.sessions.update_one(
            {"session_id": session_id},
            {
                "$setOnInsert": {"created_at": datetime.utcnow()},
                "$set": {"last_activity": datetime.utcnow()}
            },
            upsert=True
        )

    def get_chat_history(self, session_id, limit=50):
        cursor = self.chat_history.find({"session_id": session_id}).sort("timestamp", DESCENDING).limit(limit)
        return [
            {
                "user": entry["user_message"],
                "bot": entry["bot_response"],
                "timestamp": entry["timestamp"]
            }
            for entry in reversed(list(cursor))
        ]

    def clear_history(self, session_id):
        self.chat_history.delete_many({"session_id": session_id})
