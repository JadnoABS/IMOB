import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from prometheus_fastapi_instrumentator import Instrumentator
from contextlib import asynccontextmanager

from api.kafka_producer import producer, init_topic
from api.seeding import seed_database
from core.logger import get_logger

from api.routers import leads, properties, realtors, auth

logger = get_logger("imob_api")

os.makedirs("uploads", exist_ok=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_topic()
    await seed_database()
    logger.info("Starting IMOB API", extra={"action": "startup"})
    
    yield
    
    logger.info("Shutting IMOB down... cleaning Kafka queue.", extra={"action": "shutdown"})
    producer.flush()

app = FastAPI(
    title="IMOB", 
    description="Real-time lead capture and distribution engine for real estate.",
    version="1.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Instrumentator().instrument(app).expose(app)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(auth.router)
app.include_router(realtors.router)
app.include_router(properties.router)
app.include_router(leads.router)
