import os
from dotenv import load_dotenv
from services.redis_services import ItineracyRedisCache

load_dotenv()
redisManager = ItineracyRedisCache( host = "localhost", port= 6379)
