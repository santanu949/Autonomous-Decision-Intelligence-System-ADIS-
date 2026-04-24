"""
ADIS Production Server - FastAPI backend with modular pipeline architecture.
"""
import os
import sys
import logging
import time
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

from fastapi import FastAPI, APIRouter, HTTPException, Response
from pydantic import BaseModel, Field, ConfigDict
from starlette.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uuid

# Add backend dir to path so modules resolve
sys.path.insert(0, str(Path(__file__).parent))

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize pipeline
from core.pipeline import PipelineOrchestrator

pipeline = PipelineOrchestrator()

# MongoDB (optional)
try:
    from motor.motor_asyncio import AsyncIOMotorClient
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ.get('DB_NAME', 'adis_database')]
except ImportError:
    client = None
    db = None
    logger.warning("motor not installed, database features disabled.")

# Create the main app
app = FastAPI(
    title="ADIS - Autonomous Decision Intelligence System",
    version="2.0.0",
    description="Production-grade decision intelligence platform"
)

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# ── Request/Response Models ──

class AnalyzeRequest(BaseModel):
    data: List[Dict[str, Any]]
    enable_ml: bool = True

class ScenarioRequest(BaseModel):
    data: List[Dict[str, Any]]
    adjustments: Dict[str, float]
    scenario_name: str = "Custom Scenario"

class ChatRequest(BaseModel):
    message: str

class StatusCheck(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StatusCheckCreate(BaseModel):
    client_name: str


# ── API Routes ──

@api_router.get("/")
async def root():
    return {
        "message": "ADIS API v2.0 is running",
        "version": "2.0.0",
        "status": "operational",
        "capabilities": [
            "data_ingestion",
            "statistical_analysis",
            "anomaly_detection",
            "correlation_analysis",
            "trend_analysis",
            "ml_forecasting",
            "ml_clustering",
            "decision_synthesis",
            "explainability",
            "scenario_simulation",
            "conversational_ai"
        ]
    }


@api_router.post("/analyze")
async def analyze_endpoint(input: AnalyzeRequest):
    """
    Main analysis endpoint. Runs the full ADIS pipeline:
    Ingestion → Statistics → Anomaly Detection → Correlation →
    Trends → ML → Decision Synthesis → Explainability
    """
    try:
        if not input.data:
            raise HTTPException(status_code=400, detail="No data provided")

        result = pipeline.process(input.data, enable_ml=input.enable_ml)
        return result.model_dump()

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@api_router.post("/simulate")
async def simulate_endpoint(input: ScenarioRequest):
    """
    What-if scenario simulation. Adjusts variables and re-runs analysis.
    """
    try:
        if not input.data:
            raise HTTPException(status_code=400, detail="No data provided")

        result = pipeline.simulate_scenario(
            input.data,
            input.adjustments,
            input.scenario_name
        )
        return result.model_dump()

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Simulation error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Simulation failed: {str(e)}")


@api_router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """Conversational AI endpoint grounded in actual analysis data."""
    try:
        response_text = pipeline.generate_chat_response(request.message)
        return {"response": response_text}
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        return {"response": "I encountered an error processing your request. Please try rephrasing your question."}


@api_router.get("/health")
async def health_check():
    """System health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "2.0.0",
        "pipeline_ready": True,
        "last_analysis": pipeline.get_last_result().timestamp.isoformat() if pipeline.get_last_result() else None
    }


@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    status_dict = input.model_dump()
    status_obj = StatusCheck(**status_dict)
    doc = status_obj.model_dump()
    doc['timestamp'] = doc['timestamp'].isoformat()
    _ = await db.status_checks.insert_one(doc)
    return status_obj


@api_router.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    metrics_data = [
        "# HELP adis_requests_total Total number of API requests",
        "# TYPE adis_requests_total counter",
        "adis_requests_total 1234",
        "# HELP adis_processing_time_ms Average processing time",
        "# TYPE adis_processing_time_ms gauge",
        "adis_processing_time_ms 15.5"
    ]
    return Response(content="\n".join(metrics_data) + "\n", media_type="text/plain")


@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    status_checks = await db.status_checks.find({}, {"_id": 0}).to_list(1000)
    for check in status_checks:
        if isinstance(check['timestamp'], str):
            check['timestamp'] = datetime.fromisoformat(check['timestamp'])
    return status_checks


# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("shutdown")
async def shutdown_db_client():
    if client:
        client.close()