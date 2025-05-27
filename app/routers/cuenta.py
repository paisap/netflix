from fastapi import FastAPI, Depends, HTTPException, APIRouter, Request
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from app.database import SessionLocal, engine
from app.models.usuario import Base, Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioResponse
from app.models.cuenta import Base, Cuenta, CuentaUsuario
from app.schemas.cuenta import CuentaBase, CuentaCreate, CuentaResponse, CuentaUsuarioResponse

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

@router.get("/usuario", response_model=List[CuentaUsuarioResponse])
def mostrar_usuario(db: Session = Depends(get_db)):
    db_usuario = db.query(CuentaUsuario).all()
    print(db_usuario[0].__dict__)
    return db_usuario

@router.put("/{cuenta_id}/usuarios")
async def modificar_usuarios_cuenta(
    cuenta_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    body = await request.json()
    usuario_id = body.get("usuario_id")
    accion = body.get("accion")

    if not usuario_id or not accion:
        raise HTTPException(status_code=400, detail="Faltan datos requeridos")

    if accion not in ["agregar", "eliminar"]:
        raise HTTPException(status_code=400, detail="Acción no válida. Usa 'agregar' o 'eliminar'")

    cuenta = db.query(Cuenta).filter(Cuenta.id == cuenta_id).first()
    if not cuenta:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")

    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    relacion = db.query(CuentaUsuario).filter_by(cuenta_id=cuenta_id, usuario_id=usuario_id).first()

    if accion == "agregar":
        if relacion:
            raise HTTPException(status_code=400, detail="Usuario ya está asociado a la cuenta")
        nueva_relacion = CuentaUsuario(usuario_id=usuario_id, cuenta_id=cuenta_id)
        db.add(nueva_relacion)
        db.commit()
        return {"mensaje": "Usuario agregado a la cuenta"}

    elif accion == "eliminar":
        if not relacion:
            raise HTTPException(status_code=400, detail="La relación no existe")
        db.delete(relacion)
        db.commit()
        return {"mensaje": "Usuario eliminado de la cuenta"}
