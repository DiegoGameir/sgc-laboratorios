import axios from 'axios';

export const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json'
  }
});

export interface DocumentoVigente {
  id_documento: string;
  codigo_formato: string;
  titulo: string;
  numero_revision: number;
  fecha_emision: string;
  fecha_vigencia: string;
  hash_sha256: string;
  url_descarga: string;
}

export const catalogoService = {
  obtenerDocumentosVigentes: async (carreraId?: string, semestre?: number) => {
    const params: Record<string, string | number> = {};
    if (carreraId) params.carrera_id = carreraId;
    if (semestre) params.semestre = semestre;

    const response = await api.get<DocumentoVigente[]>('/catalogo/documentos', { params });
    return response.data;
  }
};