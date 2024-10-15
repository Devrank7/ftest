import redis

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
try:
    redis_client.ping()
    print("Connected to Redis")
except redis.ConnectionError as e:
    print(f"Failed to connect to Redis: {e}")
