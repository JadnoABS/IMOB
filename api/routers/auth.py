from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from api.database import realtors_collection
from core.security import verify_password, create_access_token
from api.models import Token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    realtor = await realtors_collection.find_one({"email": form_data.username})
    
    if not realtor or not verify_password(form_data.password, realtor["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token = create_access_token(data={"sub": realtor["email"]})
    return {"access_token": access_token, "token_type": "bearer"}
