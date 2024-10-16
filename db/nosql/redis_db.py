import os

import redis

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = os.getenv("REDIS_PORT", 6379)
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=0)
try:
    redis_client.ping()
    print("Connected to Redis")
except redis.ConnectionError as e:
    print(f"Failed to connect to Redis: {e}")
