from fastapi import FastAPI
import logging
from pythonjsonlogger import jsonlogger
from fastapi import FastAPI, Request
from prometheus_fastapi_instrumentator import Instrumentator
from contextlib import asynccontextmanager

from app.models import Lead
from app.database import leads_collection
from app.kafka_producer import producer, send_lead_event

logger = logging.getLogger("imob_api")
logger.setLevel(logging.INFO)

if logger.hasHandlers():
    logger.handlers.clear()

logHandler = logging.StreamHandler()

formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(message)s')
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Iniciando IMOB", extra={"action": "startup"})
    yield
    logger.info("Desligando IMOB... limpando fila do Kafka.", extra={"action": "shutdown"})
    producer.flush()

app = FastAPI(title="API de Captura de Leads Imobiliários", lifespan=lifespan)

Instrumentator().instrument(app).expose(app)

@app.post("/leads", status_code=201)
async def criar_lead(lead: Lead, request: Request):
    client_ip = request.client.host
    
    logger.info("Recebendo novo lead", extra={"email": lead.email, "ip": client_ip})
    
    lead_dict = lead.model_dump()
    
    try:
        result = await leads_collection.insert_one(lead_dict)
        lead_id = str(result.inserted_id)
        lead_dict['_id'] = lead_id
        
        logger.info("Lead salvo no banco de dados", extra={"lead_id": lead_id, "database": "mongodb"})
        
        send_lead_event(lead_dict)
        logger.info("Evento publicado", extra={"lead_id": lead_id, "topic": "lead"})
        
        return {
            "mensagem": "Lead criado com sucesso!",
            "id": lead_id
        }
    except Exception as e:
        logger.error("Falha ao processar lead", extra={"error": str(e), "email": lead.email})
        raise

