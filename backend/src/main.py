from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from .database import engine, Base
from . import models, schemas, crud
from .api import router as api_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database
    logger.info("Initializing database...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database initialized successfully")
    yield
    # Shutdown logic can go here if needed

app = FastAPI(
    title="AI-Native Robotics Book API",
    description="API for the AI-Native Software Development book with RAG capabilities",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1", tags=["api"])

@app.get("/")
async def root():
    return {"message": "AI-Native Robotics Book API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "AI-Native Robotics Book API"}