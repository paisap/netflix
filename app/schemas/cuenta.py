from typing import List, Optional
from pydantic import BaseModel, EmailStr, validator


# ✅ Base sin ID (para crear o actualizar)
class CuentaBase(BaseModel):
    correo: EmailStr
    dueno: Optional[str] = None


# ✅ Crear cuenta – incluye lista de usuarios
class CuentaCreate(CuentaBase):
    usuarios_ids: Optional[List[int]] = []

    @validator("usuarios_ids")
    def max_usuarios(cls, v):
        if len(v) > 5:
            raise ValueError("No se pueden asignar más de 5 usuarios a una cuenta")
        return v


# ✅ Leer cuenta con ID y usuarios opcional
class CuentaResponse(CuentaBase):
    id: int
    usuarios_ids: List[int] = []

    class Config:
        orm_mode = True
