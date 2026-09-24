from pydantic import BaseModel
from uuid import UUID
from datetime import date
from typing import Optional, List

# Metadatos del documento vigente para consulta pública
class DocumentoVigenteOut(BaseModel):
    id_documento: UUID
    codigo_formato: str
    titulo: str
    numero_revision: int
    fecha_emision: Optional[date] = None
    fecha_vigencia: Optional[date] = None
    hash_sha256: str
    # URL de descarga prefirmada o ruta directa
    url_descarga: Optional[str] = None

    class Config:
        from_attributes = True

# Agrupación por asignatura para navegación en árbol
class AsignaturaCatalogoOut(BaseModel):
    id_asignatura: UUID
    clave: str
    nombre: str
    semestre: int
    documentos: List[DocumentoVigenteOut] = []

    class Config:
        from_attributes = True