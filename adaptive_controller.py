import time
from redis_client import redis_client
from config import (
    REDIS_CONFIG_KEY,
    REDIS_METRICS_LATENCY,
    REDIS_METRICS_ERRORS,
    MIN_LIMIT,
    MAX_LIMIT
)

def adaptive_controller():
    redis_client.hsetnx(REDIS_CONFIG_KEY, "capacity", 5)
    redis_client.hsetnx(REDIS_CONFIG_KEY, "refill_rate", 5)

    while True:
        latency = redis_client.get(REDIS_METRICS_LATENCY)
        errors = redis_client.get(REDIS_METRICS_ERRORS)

        if latency is None:
            time.sleep(5)
            continue

        latency = float(latency)
        errors = int(errors or 0)

        config = redis_client.hgetall(REDIS_CONFIG_KEY)
        capacity = int(config["capacity"])

        if latency < 150 and errors < 1:
            capacity = min(capacity + 1, MAX_LIMIT)

        elif latency > 300 or errors > 5:
            capacity = max(capacity - 2, MIN_LIMIT)

        redis_client.hset(REDIS_CONFIG_KEY, mapping={
            "capacity": capacity,
            "refill_rate": capacity
        })

        redis_client.set(REDIS_METRICS_ERRORS, 0)
        time.sleep(5)
