from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import SessionLocal, engine
from app.models.usuario import Base, Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioResponse
from app.models.cuenta import Base, Cuenta, CuentaUsuario
from app.schemas.cuenta import CuentaBase, CuentaCreate, CuentaResponse
from app.routers import usuario, cuenta

app = FastAPI()

app.include_router(usuario.router)
app.include_router(cuenta.router)

Base.metadata.create_all(bind=engine)  # Crea las tablas si no existen

