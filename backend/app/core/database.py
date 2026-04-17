import motor.motor_asyncio
import redis.asyncio as redis
import os
from dotenv import load_dotenv

load_dotenv()

# --- MONGODB: The Permanent Memory ---
# Mandatory for Phase 1 (Ingestion) to store candidate JSONs
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "lat_ai_recruitment")

mongo_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = mongo_client[MONGO_DB_NAME]

# --- REDIS: The Telemetry Layer (With Emergency Bypass) ---
# Created to handle Phase 4 Feedback Loops
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)

async def check_redis():
    """Diagnostic helper to check if the 'Nervous System' is online."""
    try:
        await redis_client.ping()
        print("✅ Redis Connected")
        return True
    except Exception:
        print("⚠️ Redis Offline: Telemetry and History will be disabled.")
        return False