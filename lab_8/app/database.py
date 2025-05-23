from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
load_dotenv()
MONGO_DETAILS = os.getenv("MONGO_URL", "mongodb://localhost:87001")

client = AsyncIOMotorClient(MONGO_DETAILS)
db = client.library
book_collection = db.get_collection("books")
user_collection = db.get_collection("users")