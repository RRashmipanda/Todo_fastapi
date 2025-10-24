from pymongo import MongoClient # type: ignore
from app.config import MONGO_URL, DB_NAME

client = MongoClient(MONGO_URL)
db = client[DB_NAME]
todos_collection = db["todos"]
