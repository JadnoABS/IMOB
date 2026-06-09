from fastapi import APIRouter, HTTPException
from api.models import RealtorCreate
from api.database import realtors_collection
from core.security import get_password_hash

router = APIRouter(prefix="/realtors", tags=["Realtors"])

@router.post("", status_code=201)
async def create_realtor(realtor: RealtorCreate):
    if await realtors_collection.find_one({"email": realtor.email}):
        raise HTTPException(400, "Email já cadastrado.")
        
    realtor_dict = realtor.model_dump()
    realtor_dict["password"] = get_password_hash(realtor_dict.pop("password"))
    
    result = await realtors_collection.insert_one(realtor_dict)
    
    realtor_dict.pop("password", None)
    realtor_dict['_id'] = str(result.inserted_id)
    return realtor_dict
