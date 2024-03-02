import json
import os
from typing import Union, Optional

from dotenv import load_dotenv
from fastapi_redis_cache import FastApiRedisCache
from fastapi_redis_cache.enums import RedisStatus


class RedisCacheService:
    def __init__(self):
        load_dotenv()
        redis_client = FastApiRedisCache()
        redis_client.init(host_url=os.environ.get("REDIS_HOST"))
        if redis_client.status != RedisStatus.CONNECTED:
            raise ConnectionError("Redis Client could not be connected.")
        self.client = redis_client.redis

    def get(self, key: str) -> Optional[str]:
        return self.client.get(key)

    def set(self, key: str, value: Union[str, dict], expire: int):
        if isinstance(value, dict):
            value = json.dumps(value)
        self.client.set(name=key, value=value, ex=expire)

    def close(self):
        self.client.close()
