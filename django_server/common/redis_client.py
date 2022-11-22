import redis
from django.conf import settings

__cache = {}


def get_simple_redis_client(broker) -> redis.Redis:
    if not __cache.get(broker):
        __cache[broker] = redis.StrictRedis.from_url(broker, max_connections=2 ** 10)
    return __cache[broker]


def get_snowflake_client():
    return get_simple_redis_client(settings.SNOWFLAKE_WORKER_CACHE_BROKER)


def get_redis_cache_client() -> redis.Redis:
    return get_simple_redis_client(settings.REDIS_DB_CONFIG.REDIS_CACHE_BROKER)
