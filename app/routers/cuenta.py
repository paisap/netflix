from fastapi import FastAPI, Depends, HTTPException, APIRouter, Request
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from app.database import SessionLocal, engine
from app.models.usuario import Base, Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioResponse
from app.models.cuenta import Base, Cuenta, CuentaUsuario, CuentaDueno
from app.schemas.cuenta import CuentaCreate

router = APIRouter(prefix="/cuentas", tags=["Cuentas"])

@router.post("/cuenta/")
def crear_cuenta(cuenta: CuentaCreate, db: Session = Depends(get_db)):
    # Verificar que no exista el correo
    db_cuenta = db.query(Cuenta).filter(Cuenta.correo == cuenta.correo).first()
    if db_cuenta:
        raise HTTPException(status_code=400, detail="Ya existe una cuenta con ese correo")

    # Crear cuenta base
    nueva_cuenta = Cuenta(correo=cuenta.correo)
    db.add(nueva_cuenta)
    db.flush()  # Aquí ya se genera el ID de nueva_cuenta

    # Crear entrada en la tabla intermedia con el ID generado
    dueno_cuenta = CuentaDueno(usuario_id=cuenta.dueno, cuenta_id=nueva_cuenta.id)
    db.add(dueno_cuenta)

    # Guardar todos los cambios de una vez
    db.commit()

    # Refrescar el objeto para retornar la versión actualizada con ID
    db.refresh(nueva_cuenta)

    return {"status": "ok"}


@router.get("/")
def mostrar_usuario(db: Session = Depends(get_db)):
    db_usuario = db.query(Cuenta).all()
    return {"status": "ok"}

# @router.get("/usuario", response_model=List[CuentaUsuarioResponse])
# def mostrar_usuario(db: Session = Depends(get_db)):
#     db_usuario = db.query(CuentaUsuario).all()
#     print(db_usuario[0].__dict__)
#     return db_usuario

# @router.put("/{cuenta_id}/usuarios")
# async def modificar_usuarios_cuenta(
#     cuenta_id: int,
#     request: Request,
#     db: Session = Depends(get_db)
# ):
#     body = await request.json()
#     usuario_id = body.get("usuario_id")
#     accion = body.get("accion")

#     if not usuario_id or not accion:
#         raise HTTPException(status_code=400, detail="Faltan datos requeridos")

#     if accion not in ["agregar", "eliminar"]:
#         raise HTTPException(status_code=400, detail="Acción no válida. Usa 'agregar' o 'eliminar'")

#     cuenta = db.query(Cuenta).filter(Cuenta.id == cuenta_id).first()
#     if not cuenta:
#         raise HTTPException(status_code=404, detail="Cuenta no encontrada")

#     usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
#     if not usuario:
#         raise HTTPException(status_code=404, detail="Usuario no encontrado")

#     relacion = db.query(CuentaUsuario).filter_by(cuenta_id=cuenta_id, usuario_id=usuario_id).first()

#     if accion == "agregar":
#         if relacion:
#             raise HTTPException(status_code=400, detail="Usuario ya está asociado a la cuenta")
#         nueva_relacion = CuentaUsuario(usuario_id=usuario_id, cuenta_id=cuenta_id)
#         db.add(nueva_relacion)
#         db.commit()
#         return {"mensaje": "Usuario agregado a la cuenta"}

#     elif accion == "eliminar":
#         if not relacion:
#             raise HTTPException(status_code=400, detail="La relación no existe")
#         db.delete(relacion)
#         db.commit()
#         return {"mensaje": "Usuario eliminado de la cuenta"}
