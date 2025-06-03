from typing import List, Optional
from pydantic import BaseModel, EmailStr, validator





class CuentaCreate(BaseModel):
    correo: str
    dueno: int
