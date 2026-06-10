from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from src.config import get_settings
import redis
import time

settings = get_settings()

# Lazy-init Redis client for rate limiting
_redis_client: redis.Redis | None = None


def _get_redis() -> redis.Redis:
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.from_url(settings.redis_url, decode_responses=True)
    return _redis_client


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple per-IP rate limiting using Redis sliding window."""

    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for health checks
        if request.url.path in ("/", "/health", "/docs", "/redoc", "/openapi.json"):
            return await call_next(request)

        # X-Forwarded-For may be a comma-separated list and is client-spoofable.
        # Trust only the entry appended by our reverse proxy (the right-most one);
        # never key on the raw header or an attacker gets a fresh bucket per request.
        forwarded = request.headers.get("x-forwarded-for")
        if forwarded:
            client_ip = forwarded.split(",")[-1].strip()
        else:
            client_ip = request.client.host if request.client else "unknown"
        if client_ip == "unknown":
            return await call_next(request)

        key = f"rate_limit:{client_ip}:{request.url.path}"
        now = time.time()
        window = 60  # 1 minute
        limit = settings.rate_limit_per_minute

        try:
            r = _get_redis()
            pipe = r.pipeline()
            pipe.zremrangebyscore(key, 0, now - window)
            pipe.zcard(key)
            pipe.zadd(key, {str(now): now})
            pipe.expire(key, window)
            _, current_count, _, _ = pipe.execute()

            if current_count > limit:
                raise HTTPException(status_code=429, detail="Rate limit exceeded. Please slow down.")
        except redis.ConnectionError:
            # If Redis is down, allow the request (fail open)
            pass

        return await call_next(request)
