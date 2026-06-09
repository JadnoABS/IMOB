import shutil
from fastapi import APIRouter, UploadFile, File, Form, Depends
from bson import ObjectId
from api.database import properties_collection
from api.dependencies import get_current_realtor

router = APIRouter(prefix="/properties", tags=["Properties"])

@router.post("", status_code=201)
async def create_property(
    title: str = Form(...), street: str = Form(...), city: str = Form(...),
    state: str = Form(...), country: str = Form(...), zip_code: str = Form(...),
    image: UploadFile = File(...),
    current_realtor: dict = Depends(get_current_realtor) 
):
    realtor_email = current_realtor["email"]

    file_location = f"uploads/{image.filename}"
    with open(file_location, "wb+") as buffer:
        shutil.copyfileobj(image.file, buffer)

    prop_dict = {
        "title": title,
        "address": {"street": street, "city": city, "state": state, "zip_code": zip_code, "country": "BR"},
        "image_url": f"https://localhost:8000/uploads/{image.filename}",
        "realtor_email": realtor_email
    }
    result = await properties_collection.insert_one(prop_dict)
    prop_dict['_id'] = str(result.inserted_id)
    return prop_dict

@router.get("")
async def list_properties():
    props = await properties_collection.find().to_list(100)
    for p in props: 
        p['_id'] = str(p['_id'])
    return props

@router.get("/{prop_id}")
async def get_property(prop_id: str):
    try:
        prop = await properties_collection.find_one({"_id": ObjectId(prop_id)})
        if prop:
            prop['_id'] = str(prop['_id'])
            return prop
        raise HTTPException(404, "Imóvel não encontrado")
    except Exception:
        raise HTTPException(400, "ID Inválido")
