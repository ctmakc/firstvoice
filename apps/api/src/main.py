from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import get_settings
from src.routers import recordings, communities, auth, transcription, admin, provenance
from src.middleware.errors import add_error_handlers

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0-mvp",
    description="AI-native digital heritage API for Indigenous and endangered-language communities.",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

# Global error handlers
add_error_handlers(app)

# CORS — restrict in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.nextauth_url, "http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(communities.router, prefix="/api/v1/communities", tags=["Communities"])
app.include_router(recordings.router, prefix="/api/v1/recordings", tags=["Recordings"])
app.include_router(transcription.router, prefix="/api/v1/transcription", tags=["Transcription"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])
app.include_router(provenance.router, prefix="/api/v1/provenance", tags=["Provenance"])


@app.get("/health")
async def health_check():
    return {"status": "ok", "env": settings.app_env}


@app.get("/")
async def root():
    return {
        "name": settings.app_name,
        "version": "0.1.0-mvp",
        "message": "FirstVoice API — returning data sovereignty to communities.",
    }
