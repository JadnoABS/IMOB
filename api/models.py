from pydantic import BaseModel, EmailStr, Field

class Lead(BaseModel):
    name: str = Field(..., min_length=2, description="Nome completo do cliente")
    email: EmailStr
    phone: str
    property_id: str = Field(..., description="ID do imóvel de interesse na base")
