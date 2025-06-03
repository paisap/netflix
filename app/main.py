from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from fastapi.middleware.cors import CORSMiddleware

from app.database import SessionLocal, engine
from app.models.usuario import Base, Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioResponse
from app.models.cuenta import Base, Cuenta, CuentaUsuario
from app.schemas.cuenta import CuentaCreate
from app.routers import usuario, cuenta, menu

app = FastAPI()

app.include_router(usuario.router)
app.include_router(cuenta.router)
app.include_router(menu.router)

Base.metadata.create_all(bind=engine)  # Crea las tablas si no existen

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringir esto por dominio, ej: ["https://tudominio.com"]
    allow_credentials=True,
    allow_methods=["*"],  # ["GET", "POST", "PUT", "DELETE"]
    allow_headers=["*"],
)