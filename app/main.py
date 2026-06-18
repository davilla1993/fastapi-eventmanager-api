from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.modules.iam.api.controllers.auth_controller import router as auth_router
from app.modules.organizers.api.controllers.organizer_controller import (
    router as organizer_router,
)
from app.modules.categories.api.controllers.category_controller import (
    router as category_router,
)
from app.modules.venues.api.controllers.venue_controller import router as venue_router
from app.settings import settings
from app.shared.exceptions import AppException, app_exception_handler

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_hosts,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(AppException, app_exception_handler)  # type: ignore[arg-type]

app.include_router(auth_router, prefix="/api/v1")
app.include_router(organizer_router, prefix="/api/v1")
app.include_router(venue_router, prefix="/api/v1")
app.include_router(category_router, prefix="/api/v1")


@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok", "version": settings.app_version}
