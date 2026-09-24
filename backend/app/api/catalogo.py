from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.core.database import get_db
from app.models.academico import Asignatura, Carrera, Laboratorio
from app.models.calidad import DocumentoMatriz, DocumentoRevision, EstadoRevisionEnum
from app.schemas.catalogo import DocumentoVigenteOut

router = APIRouter(prefix="/catalogo", tags=["Catálogo Público SGC"])

@router.get("/documentos", response_model=List[DocumentoVigenteOut])
def listar_documentos_vigentes(
    carrera_id: Optional[UUID] = Query(None, description="Filtrar por carrera"),
    laboratorio_id: Optional[UUID] = Query(None, description="Filtrar por laboratorio"),
    semestre: Optional[int] = Query(None, ge=1, le=10, description="Filtrar por semestre (1-10)"),
    db: Session = Depends(get_db)
):
    """
    Consulta pública indexada de documentos vigentes (Cláusula 7.5 ISO 9001).
    No requiere autenticación.
    """
    query = (
        db.query(DocumentoMatriz, DocumentoRevision)
        .join(DocumentoRevision, DocumentoMatriz.id_documento == DocumentoRevision.id_documento)
        .filter(DocumentoRevision.estado == EstadoRevisionEnum.Aprobado_Vigente)
    )

    if laboratorio_id:
        query = query.filter(DocumentoMatriz.id_laboratorio == laboratorio_id)

    if carrera_id or semestre:
        query = query.join(Asignatura, DocumentoMatriz.id_asignatura == Asignatura.id_asignatura)
        if carrera_id:
            query = query.filter(Asignatura.id_carrera == carrera_id)
        if semestre:
            query = query.filter(Asignatura.semestre == semestre)

    resultados = query.all()

    respuesta = []
    for doc, rev in resultados:
        respuesta.append(
            DocumentoVigenteOut(
                id_documento=doc.id_documento,
                codigo_formato=doc.codigo_formato,
                titulo=doc.titulo,
                numero_revision=rev.numero_revision,
                fecha_emision=rev.fecha_emision,
                fecha_vigencia=rev.fecha_vigencia,
                hash_sha256=rev.hash_sha256,
                url_descarga=f"/api/v1/catalogo/descargar/{rev.id_revision}"
            )
        )

    return respuesta

from fastapi.responses import RedirectResponse
from app.core.minio_client import get_minio_client
from app.core.config import settings

@router.get("/descargar/{id_revision}")
def descargar_documento_vigente(
    id_revision: UUID, 
    db: Session = Depends(get_db)
):
    """
    Genera una URL prefirmada (válida por 5 minutos) para descargar el PDF físico desde MinIO.
    """
    revision = db.query(DocumentoRevision).filter(
        DocumentoRevision.id_revision == id_revision,
        DocumentoRevision.estado == EstadoRevisionEnum.Aprobado_Vigente
    ).first()

    if not revision:
        raise HTTPException(status_code=404, detail="Documento no encontrado o no vigente.")

    minio_client = get_minio_client()
    
    try:
        # Genera un link temporal para que el frontend descargue el archivo directo de S3
        url = minio_client.presigned_get_object(
            bucket_name=settings.MINIO_BUCKET,
            object_name=revision.ruta_almacenamiento_minio
        )
        return RedirectResponse(url=url)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error de conexión con el repositorio SGC.")