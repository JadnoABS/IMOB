from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str
    country: str = "BR"

class Realtor(BaseModel):
    document_number: str = Field(..., description="ID Universal (ex: CPF, SSN)")
    name: str
    email: EmailStr
    phone: str
    address: Address

class Property(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    title: str
    address: Address
    image_url: str
    realtor_email: EmailStr

class Lead(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    phone: str
    property_id: str

class RealtorCreate(Realtor):
    password: str = Field(..., min_length=6)

class Token(BaseModel):
    access_token: str
    token_type: str
