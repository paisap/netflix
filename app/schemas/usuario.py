from pydantic import BaseModel, EmailStr
from typing import Optional

class UsuarioCreate(BaseModel):
    usuario: str
    correo: EmailStr
    contrasena: str
    administrator: bool = False
    dueno: bool = False
    cliente: bool = False
    id_telegram: str
    celular: str

class UsuarioUpdate(BaseModel):
    usuario: Optional[str] = None
    correo: Optional[EmailStr] = None
    contrasena: Optional[str] = None
    celular: Optional[str] = None
    id_telegram: Optional[str] = None
    administrator: Optional[bool] = None
    dueno: Optional[bool] = None
    cliente: Optional[bool] = None


class UsuarioResponse(BaseModel):
    id: int
    usuario: str
    correo: EmailStr
    dueno: bool
    cliente: bool
    administrator: bool
    id_telegram: str
    celular: str

    class Config:
        orm_mode = True
