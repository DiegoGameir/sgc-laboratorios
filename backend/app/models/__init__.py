from app.models.academico import Carrera, Laboratorio, Asignatura
from app.models.calidad import UsuarioSGC, DocumentoMatriz, DocumentoRevision, EstadoRevisionEnum
from app.models.evaluacion import PracticaCatalogo, RubricaCriterio, EvaluacionBanco, EvaluacionDetalle, AuditLogSGC

__all__ = [
    "Carrera", "Laboratorio", "Asignatura",
    "UsuarioSGC", "DocumentoMatriz", "DocumentoRevision", "EstadoRevisionEnum",
    "PracticaCatalogo", "RubricaCriterio", "EvaluacionBanco", "EvaluacionDetalle", "AuditLogSGC"
]