from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .routes import user, challenge

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(
    title="Challenge API",
    description="API for the Challenge project",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.allow_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix=f"{settings.api_prefix}/users", tags=["users"])
app.include_router(challenge.router, prefix=f"{settings.api_prefix}/challenges", tags=["challenges"])