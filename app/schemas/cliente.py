from pydantic import BaseModel
from .usuario import Usuario

class ClienteBase(BaseModel):
    administrador_id: int
    cliente_id: int

class ClienteCreate(ClienteBase):
    pass

class Cliente(ClienteBase):
    id: int
    administrador: Usuario
    cliente: Usuario

    class Config:
        from_attributes = True