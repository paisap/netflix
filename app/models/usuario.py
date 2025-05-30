from sqlalchemy import Column, Integer, String, Boolean
from ..database import Base
from sqlalchemy.orm import relationship

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    usuario = Column(String, unique=True, index=True)
    correo = Column(String, unique=True, index=True)
    contrasena = Column(String)
    celular = Column(String, unique=True, index=True, nullable=True)
    id_telegram = Column(String, unique=True, index=True, nullable=True)
    administrator = Column(Boolean, default=False)
    dueno = Column(Boolean, default=False)
    cliente = Column(Boolean, default=False)

    cuentas = relationship("CuentaUsuario", back_populates="usuario")