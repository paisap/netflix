from typing import List, Optional
from pydantic import BaseModel, EmailStr, validator


# ✅ Base sin ID (para crear o actualizar)
class CuentaBase(BaseModel):
    correo: EmailStr


# ✅ Base sin ID (para crear o actualizar)
class CuentaUsuarioBase(BaseModel):
    id: int
    cuenta_id: int
    usuario_id: int



# ✅ Leer cuenta con ID y usuarios opcional
class CuentaResponse(CuentaBase):
    id: int

