from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings
from app.db.session import Base, engine

# Create all DB tables on startup (use Alembic for prod migrations)
Base.metadata.create_all(bind=engine)

# Import models so SQLAlchemy picks them up for create_all
from app.models import task, user  # noqa: F401, E402


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        docs_url="/docs",       # Swagger UI
        redoc_url="/redoc",     # ReDoc UI
    )

    app.include_router(api_router)

    @app.get("/health", tags=["Health"])
    def health_check():
        return {"status": "ok", "version": settings.APP_VERSION}

    return app


app = create_app()
