from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime

class Cuenta(Base):
    __tablename__ = "cuentas"

    id = Column(Integer, primary_key=True, index=True)
    correo = Column(String, unique=True, index=True)
    dueno = Column(String)

    usuarios = relationship("CuentaUsuario", back_populates="cuenta")


class CuentaUsuario(Base):
    __tablename__ = "cuenta_usuarios"

    cuenta_id = Column(Integer, ForeignKey("cuentas.id"), primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), primary_key=True)
    fecha_asignacion = Column(DateTime, default=datetime.utcnow)

    cuenta = relationship("Cuenta", back_populates="usuarios")
    usuario = relationship("Usuario", back_populates="cuentas")
    