import redis

from source.core.settings import settings

redis_client = redis.Redis(settings.REDIS_URL, db=0)

