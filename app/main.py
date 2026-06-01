from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.models import Lead
from app.database import leads_collection
from app.kafka_producer import producer, send_lead_event 

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    print("Desligando aplicação... limpando fila do Kafka.")
    producer.flush()

app = FastAPI(
    title="API de Captura de Leads Imobiliários",
    lifespan=lifespan
)

@app.post("/leads", status_code=201)
async def criar_lead(lead: Lead):
    lead_dict = lead.model_dump()
    
    result = await leads_collection.insert_one(lead_dict)
    
    lead_dict['_id'] = str(result.inserted_id)
    
    send_lead_event(lead_dict)
    
    return {
        "mensagem": "Lead criado, salvo e evento publicado com sucesso!",
        "id": lead_dict['_id']
    }
