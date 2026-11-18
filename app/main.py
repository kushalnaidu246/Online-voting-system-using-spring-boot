from contextlib import asynccontextmanager

from fastapi import FastAPI

from . import models  # noqa: F401  (registers tables)
from .database import Base, engine
from .routers import candidates, users, votes


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)  # like spring.jpa.hibernate.ddl-auto=update
    yield


app = FastAPI(title="Online Voting System", version="0.1.0", lifespan=lifespan)
app.include_router(users.router)
app.include_router(candidates.router)
app.include_router(votes.router)
