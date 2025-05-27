from pydantic import BaseModel, EmailStr

class UsuarioCreate(BaseModel):
    usuario: str
    correo: EmailStr
    contrasena: str
    administrator: bool = False
    dueno: bool = False
    cliente: bool = False

class UsuarioResponse(BaseModel):
    id: int
    usuario: str
    correo: EmailStr
    dueno: bool
    cliente: bool

    class Config:
        orm_mode = True
