from fastapi import FastAPI, Depends, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from app.database import SessionLocal, engine
from app.models.usuario import Base, Usuario, AdminUsuario
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, UsuarioUpdate
from app.models.cuenta import Base, Cuenta, CuentaUsuario, CuentaDueno
from app.schemas.cuenta import CuentaCreate

router = APIRouter(prefix="/menu", tags=["menu"])


@router.get("/{usuario_id}")
def mostrar_menu(usuario_id: int, db: Session = Depends(get_db)):
    print(usuario_id)
    informacion = []
    ids_ususarios = []
    ids_cuentas = []
    cuentas_usuario = db.query(CuentaDueno).filter(usuario_id == CuentaDueno.usuario_id).all()
    admin_usuario = db.query(AdminUsuario).filter(usuario_id == AdminUsuario.dueno).all()

    for i in cuentas_usuario:
        ids_cuentas.append(i.cuenta_id)
    for i in admin_usuario:
        ids_ususarios.append(i.cliente)

    usuarios = db.query(Usuario).filter(Usuario.id.in_(ids_ususarios)).all()
    cuentas = db.query(Cuenta).filter(Cuenta.id.in_(ids_cuentas)).all()
    # Convertir objetos Usuario a diccionarios
    cuentas_usuario_json = [u.__dict__ for u in cuentas]
    usuarios_json = [u.__dict__ for u in usuarios]

    # Eliminar claves internas de SQLAlchemy (_sa_instance_state)
    for u in usuarios_json:
        u.pop('_sa_instance_state', None)
    for u in cuentas_usuario_json:
        u.pop('_sa_instance_state', None)

    return JSONResponse(content={
        "status": "ok",
        "usuarios": usuarios_json,
        "cuentas": cuentas_usuario_json
    })



@router.get("/")
def mostrar_usuario(db: Session = Depends(get_db)):
    db_usuario = db.query(AdminUsuario).all()
    for i in db_usuario:
        print(i.__dict__)
    return None