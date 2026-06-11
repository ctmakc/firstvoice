from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from src.config import get_settings
from src.routers import recordings, communities, auth, transcription, admin, provenance
from src.middleware.errors import add_error_handlers
from src.middleware.rate_limit import RateLimitMiddleware
from src.database import async_engine, sync_engine
from src.services.storage import get_minio
import redis

settings = get_settings()


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses."""

    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(self), geolocation=()"
        if settings.app_env == "production":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response


app = FastAPI(
    title=settings.app_name,
    version="0.1.0-mvp",
    description="AI-native digital heritage API for Indigenous and endangered-language communities.",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

# Global error handlers
add_error_handlers(app)

# Security headers
app.add_middleware(SecurityHeadersMiddleware)

# Rate limiting
app.add_middleware(RateLimitMiddleware)

# CORS — restrict in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.nextauth_url, "http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3050"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(communities.router, prefix="/api/communities", tags=["Communities"])
app.include_router(recordings.router, prefix="/api/recordings", tags=["Recordings"])
app.include_router(transcription.router, prefix="/api/transcription", tags=["Transcription"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
app.include_router(provenance.router, prefix="/api/provenance", tags=["Provenance"])


@app.get("/health")
async def health_check():
    """Deep health check: tests DB, Redis, MinIO connectivity."""
    health = {
        "status": "ok",
        "env": settings.app_env,
        "version": "0.1.0-mvp",
        "services": {},
    }

    # Database check
    try:
        from sqlalchemy import text
        async with async_engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        health["services"]["database"] = "ok"
    except Exception as e:
        health["services"]["database"] = f"error: {str(e)}"
        health["status"] = "degraded"

    # Redis check
    try:
        r = redis.from_url(settings.redis_url)
        r.ping()
        r.close()
        health["services"]["redis"] = "ok"
    except Exception as e:
        health["services"]["redis"] = f"error: {str(e)}"
        health["status"] = "degraded"

    # MinIO check
    try:
        client = get_minio()
        client.list_buckets()
        health["services"]["minio"] = "ok"
    except Exception as e:
        health["services"]["minio"] = f"error: {str(e)}"
        health["status"] = "degraded"

    return health


@app.get("/")
async def root():
    return {
        "name": settings.app_name,
        "version": "0.1.0-mvp",
        "message": "FirstVoice API — returning data sovereignty to communities.",
        "docs": "/docs" if settings.debug else None,
        "health": "/health",
    }
