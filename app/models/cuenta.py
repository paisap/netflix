from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime

class Cuenta(Base):
    __tablename__ = "cuentas"

    id = Column(Integer, primary_key=True, index=True)
    correo = Column(String, unique=True, index=True)



class CuentaUsuario(Base):
    __tablename__ = "cuenta_usuarios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cuenta_id = Column(Integer)
    usuario_id = Column(Integer)
    #fecha_asignacion = Column(DateTime, default=datetime.utcnow)


class CuentaDueno(Base):
    __tablename__ = "cuenta_dueno"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cuenta_id = Column(Integer)
    usuario_id = Column(Integer)
    #fecha_asignacion = Column(DateTime, default=datetime.utcnow)

