import redis


def get_redis_client():
    client = redis.Redis(decode_responses=True)
    return client
