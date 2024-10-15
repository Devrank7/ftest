import json
from typing import Any

from db.nosql.redis_db import redis_client


async def cacheable(key: str, func, lifetime: int = 3600) -> dict[str, Any]:
    val = redis_client.get(key)
    if val is None:
        spk = key.split('_')
        val = await func(spk[0:len(spk) - 2])
        print("Val = ", val)
        print('key = ',key)
        data_json = json.dumps(val)
        redis_client.setex(key, lifetime, data_json)
        return val
    return json.loads(val)
