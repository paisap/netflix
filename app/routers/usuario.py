from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from app.database import SessionLocal, engine
from app.models.usuario import Base, Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, UsuarioUpdate
from app.models.cuenta import Base, Cuenta, CuentaUsuario
from app.schemas.cuenta import CuentaBase, CuentaCreate, CuentaResponse

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.post("/", response_model=UsuarioResponse)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = Usuario(**usuario.dict())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@router.get("/", response_model=List[UsuarioResponse])
def mostrar_usuario(db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).all()
    return db_usuario


@router.patch("/{usuario_id}", response_model=UsuarioResponse)
def actualizar_usuario(usuario_id: int, datos_actualizados: UsuarioUpdate, db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    for campo, valor in datos_actualizados.dict(exclude_unset=True).items():
        setattr(db_usuario, campo, valor)

    db.commit()
    db.refresh(db_usuario)
    return db_usuario
# Añade más endpoints según necesidad