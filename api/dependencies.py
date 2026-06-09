from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from core.security import JWT_SECRET, ALGORITHM
from api.database import realtors_collection

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_realtor(token: str = Depends(oauth2_scheme)) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
        
    realtor = await realtors_collection.find_one({"email": email})
    if realtor is None:
        raise credentials_exception
        
    return realtor
