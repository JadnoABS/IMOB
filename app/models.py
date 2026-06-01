from pydantic import BaseModel, EmailStr, Field

class Lead(BaseModel):
    nome: str = Field(..., min_length=2, description="Nome completo do cliente")
    email: EmailStr
    telefone: str
    imovel_id: str = Field(..., description="ID do imóvel de interesse na base")
