import json
from abc import ABC, abstractmethod

from db.nosql.redis_db import redis_client


class RedisCachable(ABC):
    @abstractmethod
    async def cacheable(self):
        pass


class RedisDictCachable(RedisCachable):
    def __init__(self, key: str, func, lifetime: int = 3600):
        self.key = key
        self.func = func
        self.lifetime = lifetime

    async def cacheable(self):
        val = redis_client.get(self.key)
        if val is None:
            spk = self.key.split('_')
            val = await self.func(spk[0:len(spk) - 2])
            data_json = json.dumps(val)
            redis_client.setex(self.key, self.lifetime, data_json)
            return val
        return json.loads(val)
