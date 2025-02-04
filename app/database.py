from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb://127.0.0.1:27017"  # Use IP instead of "localhost" for Docker compatibility
DATABASE_NAME = "olympics"

client = AsyncIOMotorClient(MONGO_URI)
db = client[DATABASE_NAME]
