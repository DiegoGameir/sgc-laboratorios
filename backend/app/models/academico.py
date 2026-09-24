import uuid
from sqlalchemy import Column, String, SmallInteger, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base

class Carrera(Base):
    __tablename__ = "carrera"

    id_carrera = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    clave = Column(String(20), unique=True, nullable=False)
    nombre = Column(String(150), nullable=False)
    activo = Column(Boolean, default=True)

    asignaturas = relationship("Asignatura", back_populates="carrera")


class Laboratorio(Base):
    __tablename__ = "laboratorio"

    id_laboratorio = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo = Column(String(20), unique=True, nullable=False)
    nombre = Column(String(150), nullable=False)
    ubicacion = Column(String(100))

    documentos = relationship("DocumentoMatriz", back_populates="laboratorio")


class Asignatura(Base):
    __tablename__ = "asignatura"

    id_asignatura = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_carrera = Column(UUID(as_uuid=True), ForeignKey("carrera.id_carrera"), nullable=False)
    clave = Column(String(20), nullable=False)
    nombre = Column(String(150), nullable=False)
    semestre = Column(SmallInteger, nullable=False)

    carrera = relationship("Carrera", back_populates="asignaturas")
    documentos = relationship("DocumentoMatriz", back_populates="asignatura")
    practicas = relationship("PracticaCatalogo", back_populates="asignatura")