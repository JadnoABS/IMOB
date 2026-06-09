from motor.motor_asyncio import AsyncIOMotorClient
from core.env import MONGO_URL

client = AsyncIOMotorClient(MONGO_URL)

db = client.imob_db
leads_collection = db.leads
