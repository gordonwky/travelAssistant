from redis.asyncio import Redis
import json
from typing import Any, Optional 
from hashlib import md5
class RedisManagement:
    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0):
        self.r = Redis(host=host, port=port, db=db, decode_responses=True)

    async def set_cache(self, key: str, value: Any, expire: int = 3600) -> None:
        """Set a cache value with optional expiration (default: 1 hour)."""
        await self.r.set(key, json.dumps(value), ex=expire)

    async def get_cache(self, key: str) -> Optional[Any]:
        """Get a cache value if it exists, otherwise None."""
        value = await self.r.get(key)
        if value is not None:
            return json.loads(value)
        return None

class ItineraryRedis(RedisManagement):
    def __init__(self, host="localhost", port=6379):
        super().__init__(host, port)

    def _make_key(self, prefix: str, user_id: int, query: str) -> str:
        return f"{prefix}:{user_id}:{md5(query.encode()).hexdigest()}"

    # --- Flight cache ---
    async def set_flight_cache(self, user_id: int, query: str, result: dict, expire: int = 3600):
        key = self._make_key("flight", user_id, query)
        await self.set_cache(key, result, expire)

    async def get_flight_cache(self, user_id: int, query: str):
        key = self._make_key("flight", user_id, query)
        return await self.get_cache(key)

    # --- Itinerary cache ---
    async def set_itinerary_cache(self, user_id: int, query: str, result: dict, expire: int = 3600):
        key = self._make_key("itinerary", user_id, query)
        await self.set_cache(key, result, expire)

    async def get_itinerary_cache(self, user_id: int, query: str):
        key = self._make_key("itinerary", user_id, query)
        return await self.get_cache(key)
