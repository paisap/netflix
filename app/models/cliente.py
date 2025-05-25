from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    administrador_id = Column(Integer, ForeignKey("usuarios.id"))
    cliente_id = Column(Integer, ForeignKey("usuarios.id"))
    
    # Relaciones
    administrador = relationship("Usuario", foreign_keys=[administrador_id])
    cliente = relationship("Usuario", foreign_keys=[cliente_id])