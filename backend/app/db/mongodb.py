from motor.motor_asyncio import AsyncIOMotorClient
import os

class MongoDBClient:
    def __init__(self):
        self.client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
        self.db = self.client.recruitment_db
        # Stores final reports and Agentic Analyst signals [cite: 383]
        self.results = self.db.recommendations 

    async def save_verdict(self, candidate_id: str, verdict: dict):
        """Phase 6: Explanation & Persistence [cite: 378]"""
        await self.results.update_one(
            {"candidate_id": candidate_id},
            {"$set": verdict},
            upsert=True
        )

    async def get_candidate_json(self, candidate_id: str):
        """Pull full JSON (Audit + Depth scores) for finalists [cite: 413]"""
        return await self.results.find_one({"candidate_id": candidate_id})