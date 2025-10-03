from motor.motor_asyncio import AsyncIOMotorClient
from config.settings import settings
import asyncio

client = None
database = None

async def connect_to_mongo():
    global client, database
    try:
        # Set a timeout to avoid hanging indefinitely
        client = AsyncIOMotorClient(
            settings.MONGODB_URL,
            serverSelectionTimeoutMS=5000  # 5 seconds timeout
        )
        database = client[settings.DATABASE_NAME]

        # Force a connection check
        await database.command("ping")
        print(f"✅ Connected to MongoDB: {settings.DATABASE_NAME}")

    except Exception as e:
        print("❌ MongoDB connection error:", e)
        # Optional: do not raise to allow app to start
        database = None
        client = None

async def close_mongo_connection():
    global client
    if client:
        client.close()
        print("❌ Closed MongoDB connection")

def get_database():
    return database
