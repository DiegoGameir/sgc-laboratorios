import uuid
import enum
from sqlalchemy import Column, String, Integer, Date, DateTime, Text, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class EstadoRevisionEnum(str, enum.Enum):
    Borrador = "Borrador"
    En_Revision = "En_Revision"
    Aprobado_Vigente = "Aprobado_Vigente"
    Obsoleto = "Obsoleto"


class UsuarioSGC(Base):
    __tablename__ = "usuario_sgc"

    id_usuario = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre_completo = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    rol = Column(String(50), nullable=False)
    activo = Column(Boolean, default=True)


class DocumentoMatriz(Base):
    __tablename__ = "documento_matriz"

    id_documento = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo_formato = Column(String(50), unique=True, nullable=False)
    titulo = Column(String(200), nullable=False)
    id_laboratorio = Column(UUID(as_uuid=True), ForeignKey("laboratorio.id_laboratorio"))
    id_asignatura = Column(UUID(as_uuid=True), ForeignKey("asignatura.id_asignatura"))
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    laboratorio = relationship("Laboratorio", back_populates="documentos")
    asignatura = relationship("Asignatura", back_populates="documentos")
    revisiones = relationship("DocumentoRevision", back_populates="documento", cascade="all, delete-orphan")


class DocumentoRevision(Base):
    __tablename__ = "documento_revision"

    id_revision = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_documento = Column(UUID(as_uuid=True), ForeignKey("documento_matriz.id_documento"), nullable=False)
    numero_revision = Column(Integer, nullable=False)
    estado = Column(SQLEnum(EstadoRevisionEnum, name="estado_revision"), default=EstadoRevisionEnum.Borrador, nullable=False)

    # Trazabilidad de firmas
    id_elaboro = Column(UUID(as_uuid=True), ForeignKey("usuario_sgc.id_usuario"))
    id_reviso = Column(UUID(as_uuid=True), ForeignKey("usuario_sgc.id_usuario"))
    id_aprobo = Column(UUID(as_uuid=True), ForeignKey("usuario_sgc.id_usuario"))

    fecha_emision = Column(Date)
    fecha_vigencia = Column(Date)
    resumen_modificaciones = Column(Text)

    hash_sha256 = Column(String(64), nullable=False)
    ruta_almacenamiento_minio = Column(String(255), nullable=False)

    documento = relationship("DocumentoMatriz", back_populates="revisiones")