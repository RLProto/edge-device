from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import Crop, Filter, Model, Predict, Video
from app.utils import start_system, stop_stream

from .sql_app import models
from .sql_app.db_manager import engine

models.Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_system()
    yield
    stop_stream()


app = FastAPI(lifespan=lifespan)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(Crop.router)
app.include_router(Filter.router)
app.include_router(Model.router)
app.include_router(Predict.router)
app.include_router(Video.router)

if __name__ == "__main__":
    ...
