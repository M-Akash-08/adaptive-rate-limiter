import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from rate_limiter import allow_request
from redis_client import redis_client
from config import REDIS_METRICS_LATENCY, REDIS_METRICS_ERRORS

class RateLimiterMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        user_id = request.headers.get("X-User-Id")
        if user_id:
            key = f"user:{user_id}"
        else:
            key = f"ip:{request.client.host}"

        start = time.time()
        allowed, retry_after = allow_request(key)

        if not allowed:
            return JSONResponse(
                status_code=429,
                content={"detail": "Too Many Requests"},
                headers={"Retry-After": str(retry_after)}
            )

        response = await call_next(request)
        latency = (time.time() - start) * 1000

        redis_client.set(REDIS_METRICS_LATENCY, latency)
        if response.status_code >= 500:
            redis_client.incr(REDIS_METRICS_ERRORS)

        return response
