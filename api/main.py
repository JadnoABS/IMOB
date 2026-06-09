from fastapi import FastAPI
from fastapi import FastAPI, Request
from prometheus_fastapi_instrumentator import Instrumentator
from contextlib import asynccontextmanager

from api.models import Lead
from api.database import leads_collection
from api.kafka_producer import producer, init_topic, send_lead_event
from core.logger import get_logger

logger = get_logger("imob_api")

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_topic()
    logger.info("Starting IMOB", extra={"action": "startup"})
    yield
    logger.info("Shutting IMOB down... cleaning Kafka queue.", extra={"action": "shutdown"})
    producer.flush()

app = FastAPI(title="IMOB: API de Captura de Leads Imobiliários", lifespan=lifespan)

Instrumentator().instrument(app).expose(app)

@app.post("/leads", status_code=201)
async def create_lead(lead: Lead, request: Request):
    client_ip = request.client.host
    
    logger.info("Receiving new lead", extra={"email": lead.email, "ip": client_ip})
    
    lead_dict = lead.model_dump()
    
    try:
        result = await leads_collection.insert_one(lead_dict)
        lead_id = str(result.inserted_id)
        lead_dict['_id'] = lead_id
        
        logger.info("Lead saved on database", extra={"lead_id": lead_id, "database": "mongodb"})
        
        send_lead_event(lead_dict)
        logger.info("Event published", extra={"lead_id": lead_id, "topic": "lead"})
        
        return {
            "mensagem": "Lead criado com sucesso!",
            "id": lead_id
        }
    except Exception as e:
        logger.error("Failed to process lead", extra={"error": str(e), "email": lead.email})
        raise

