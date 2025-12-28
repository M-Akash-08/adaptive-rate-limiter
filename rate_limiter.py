import time
import math
from redis_client import redis_client
from config import (
    REDIS_BUCKET_PREFIX,
    REDIS_CONFIG_KEY,
    DEFAULT_CAPACITY,
    DEFAULT_REFILL_RATE
)

def allow_request(key: str):
    now = time.time()

    config = redis_client.hgetall(REDIS_CONFIG_KEY)
    capacity = int(config.get("capacity", DEFAULT_CAPACITY))
    refill_rate = float(config.get("refill_rate", DEFAULT_REFILL_RATE))

    redis_key = f"{REDIS_BUCKET_PREFIX}{key}"
    state = redis_client.hgetall(redis_key)

    if not state:
        tokens = capacity
        last_refill = now
    else:
        tokens = float(state["tokens"])
        last_refill = float(state["last_refill"])

    elapsed = now - last_refill
    tokens = min(capacity, tokens + elapsed * refill_rate)

    if tokens >= 1:
        tokens -= 1
        redis_client.hset(redis_key, mapping={
            "tokens": tokens,
            "last_refill": now
        })
        redis_client.expire(redis_key, 60)
        return True, 0

    retry_after = math.ceil((1 - tokens) / refill_rate)

    redis_client.hset(redis_key, mapping={
        "tokens": tokens,
        "last_refill": now
    })
    redis_client.expire(redis_key, 60)

    return False, retry_after
