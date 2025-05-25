from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from app.database import SessionLocal, engine
from app.models.usuario import Base, Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioResponse
from app.models.cuenta import Base, Cuenta, CuentaUsuario
from app.schemas.cuenta import CuentaBase, CuentaCreate, CuentaResponse

router = APIRouter(prefix="/cuentas", tags=["Cuentas"])

@router.post("/cuenta/", response_model=CuentaResponse)
def crear_cuenta(cuenta: CuentaCreate, db: Session = Depends(get_db)):
    # Verificar que no exista el correo
    db_cuenta = db.query(Cuenta).filter(Cuenta.correo == cuenta.correo).first()
    if db_cuenta:
        raise HTTPException(status_code=400, detail="Ya existe una cuenta con ese correo")
    # Crear cuenta base
    nueva_cuenta = Cuenta(correo=cuenta.correo, dueno=cuenta.dueno)
    db.add(nueva_cuenta)
    db.commit()
    db.refresh(nueva_cuenta)

    # Asociar usuarios si se enviaron
    for user_id in cuenta.usuarios_ids:
        user = db.query(Usuario).filter(Usuario.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail=f"Usuario con ID {user_id} no encontrado")
        cuenta_usuario = CuentaUsuario(usuario_id=user_id, cuenta_id=nueva_cuenta.id)
        db.add(cuenta_usuario)

    db.commit()
    return nueva_cuenta

@router.get("/", response_model=List[CuentaResponse])
def mostrar_usuario(db: Session = Depends(get_db)):
    db_usuario = db.query(Cuenta).all()
    return db_usuario
