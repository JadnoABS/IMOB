from fastapi import APIRouter, HTTPException, Request
from bson import ObjectId
from api.models import Lead
from api.database import leads_collection, properties_collection
from api.kafka_producer import send_lead_event
from core.logger import get_logger

logger = get_logger("imob_api")
router = APIRouter(prefix="/leads", tags=["Leads"])

@router.post("", status_code=201)
async def create_lead(lead: Lead, request: Request):
    client_ip = request.client.host
    logger.info("Receiving new lead", extra={"email": lead.email, "ip": client_ip})
    
    try:
        prop = await properties_collection.find_one({"_id": ObjectId(lead.property_id)})
        if not prop:
            raise HTTPException(404, "Property not found")
    except Exception:
        raise HTTPException(400, "Invalid property ID")
    
    lead_dict = lead.model_dump()
    lead_dict["realtor_email"] = prop["realtor_email"]
    
    try:
        result = await leads_collection.insert_one(lead_dict)
        lead_id = str(result.inserted_id)
        lead_dict['_id'] = lead_id
        
        logger.info("Lead saved on database", extra={"lead_id": lead_id, "database": "mongodb"})
        send_lead_event(lead_dict)
        
        return {"mensagem": "Lead created successfully!", "id": lead_id}
    except Exception as e:
        logger.error("Failed to process lead", extra={"error": str(e)})
        raise HTTPException(500, "Internal error while processing lead")
