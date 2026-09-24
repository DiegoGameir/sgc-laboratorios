import uuid
from sqlalchemy import Column, String, SmallInteger, Numeric, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class PracticaCatalogo(Base):
    __tablename__ = "practica_catalogo"

    id_practica = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_asignatura = Column(UUID(as_uuid=True), ForeignKey("asignatura.id_asignatura"), nullable=False)
    numero_practica = Column(SmallInteger, nullable=False)
    titulo = Column(String(200), nullable=False)
    id_revision_documento = Column(UUID(as_uuid=True), ForeignKey("documento_revision.id_revision"))

    asignatura = relationship("Asignatura", back_populates="practicas")
    criterios = relationship("RubricaCriterio", back_populates="practica", cascade="all, delete-orphan")


class RubricaCriterio(Base):
    __tablename__ = "rubrica_criterio"

    id_criterio = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_practica = Column(UUID(as_uuid=True), ForeignKey("practica_catalogo.id_practica"), nullable=False)
    descripcion = Column(String(255), nullable=False)
    peso_porcentaje = Column(Numeric(5, 2), nullable=False)

    practica = relationship("PracticaCatalogo", back_populates="criterios")


class EvaluacionBanco(Base):
    __tablename__ = "evaluacion_banco"

    id_evaluacion = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_practica = Column(UUID(as_uuid=True), ForeignKey("practica_catalogo.id_practica"), nullable=False)
    id_evaluador = Column(UUID(as_uuid=True), ForeignKey("usuario_sgc.id_usuario"))
    identificador_banco = Column(String(50), nullable=False)
    fecha_evaluacion = Column(DateTime(timezone=True), server_default=func.now())
    hash_evidencia_inmutable = Column(String(64))
    comentarios_profesor = Column(Text)

    detalles = relationship("EvaluacionDetalle", back_populates="evaluacion", cascade="all, delete-orphan")


class EvaluacionDetalle(Base):
    __tablename__ = "evaluacion_detalle"

    id_detalle = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_evaluacion = Column(UUID(as_uuid=True), ForeignKey("evaluacion_banco.id_evaluacion"), nullable=False)
    id_criterio = Column(UUID(as_uuid=True), ForeignKey("rubrica_criterio.id_criterio"), nullable=False)
    calificacion_obtenida = Column(Numeric(5, 2), nullable=False)

    evaluacion = relationship("EvaluacionBanco", back_populates="detalles")


class AuditLogSGC(Base):
    __tablename__ = "audit_log_sgc"

    id_log = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fecha_evento = Column(DateTime(timezone=True), server_default=func.now())
    id_usuario = Column(UUID(as_uuid=True), ForeignKey("usuario_sgc.id_usuario"))
    tabla_afectada = Column(String(50), nullable=False)
    id_registro_afectado = Column(UUID(as_uuid=True), nullable=False)
    accion = Column(String(20), nullable=False)
    valores_anteriores = Column(JSONB)
    valores_nuevos = Column(JSONB)
    ip_origen = Column(String(45))