from dotenv import load_dotenv
from services.redis_services import ItineraryRedis

load_dotenv()
redisManager = ItineraryRedis( host = "localhost", port= 6379)
