import React, { useEffect, useState } from 'react';
import { catalogoService, DocumentoVigente } from '../services/api';
import { FileText, Download, ShieldCheck, Search, Filter } from 'lucide-react';

export const CatalogoPublico: React.FC = () => {
  const [documentos, setDocumentos] = useState<DocumentoVigente[]>([]);
  const [cargando, setCargando] = useState<boolean>(true);
  const [busqueda, setBusqueda] = useState<string>('');

  useEffect(() => {
    cargarDocumentos();
  }, []);

  const cargarDocumentos = async () => {
    try {
      setCargando(true);
      const data = await catalogoService.obtenerDocumentosVigentes();
      setDocumentos(data);
    } catch (error) {
      console.error("Error al conectar con la API del SGC:", error);
    } finally {
      setCargando(false);
    }
  };

  const documentosFiltrados = documentos.filter(doc => 
    doc.titulo.toLowerCase().includes(busqueda.toLowerCase()) ||
    doc.codigo_formato.toLowerCase().includes(busqueda.toLowerCase())
  );

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Banner informativo ISO 9001 */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 flex items-start gap-3">
        <ShieldCheck className="w-6 h-6 text-blue-700 flex-shrink-0 mt-0.5" />
        <div className="text-sm text-blue-900">
          <span className="font-semibold">Control de Información Documentada (Cláusula 7.5 ISO 9001):</span>
          <p className="mt-0.5 text-blue-800">
            Este catálogo muestra exclusivamente formatos y manuales en estado <strong>Aprobado y Vigente</strong>. El uso de copias impresas o versiones anteriores carece de validez técnica.
          </p>
        </div>
      </div>

      {/* Barra de búsqueda y filtros */}
      <div className="flex flex-col sm:flex-row gap-3 items-center justify-between bg-white p-4 rounded-lg shadow-sm border border-slate-200">
        <div className="relative w-full sm:w-96">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
          <input
            type="text"
            placeholder="Buscar por código (ej. FO-LAB) o título..."
            value={busqueda}
            onChange={(e) => setBusqueda(e.target.value)}
            className="w-full pl-9 pr-4 py-2 border border-slate-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-600 focus:border-transparent"
          />
        </div>
        <div className="flex items-center gap-2 text-sm text-slate-500">
          <Filter className="w-4 h-4" />
          <span>{documentosFiltrados.length} documentos vigentes</span>
        </div>
      </div>

      {/* Tabla de Documentos SGC */}
      <div className="bg-white rounded-lg shadow-sm border border-slate-200 overflow-hidden">
        {cargando ? (
          <div className="p-8 text-center text-slate-500">Consultando catálogo institucional...</div>
        ) : documentosFiltrados.length === 0 ? (
          <div className="p-8 text-center text-slate-500">No se encontraron documentos vigentes registrados.</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse text-sm">
              <thead>
                <tr className="bg-slate-100 border-b border-slate-200 text-slate-700 font-semibold">
                  <th className="py-3 px-4">Código SGC</th>
                  <th className="py-3 px-4">Título del Documento</th>
                  <th className="py-3 px-4 text-center">Revisión</th>
                  <th className="py-3 px-4">Vigencia</th>
                  <th className="py-3 px-4">Integridad (SHA-256)</th>
                  <th className="py-3 px-4 text-center">Acción</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {documentosFiltrados.map((doc) => (
                  <tr key={doc.id_documento} className="hover:bg-slate-50 transition-colors">
                    <td className="py-3 px-4 font-mono font-medium text-blue-700">
                      {doc.codigo_formato}
                    </td>
                    <td className="py-3 px-4 font-medium text-slate-800">
                      <div className="flex items-center gap-2">
                        <FileText className="w-4 h-4 text-slate-400 flex-shrink-0" />
                        {doc.titulo}
                      </div>
                    </td>
                    <td className="py-3 px-4 text-center">
                      <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold bg-emerald-100 text-emerald-800">
                        Rev. {doc.numero_revision}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-slate-600 text-xs">
                      Hasta {doc.fecha_vigencia || 'N/A'}
                    </td>
                    <td className="py-3 px-4">
                      <code className="text-[11px] bg-slate-100 px-2 py-1 rounded text-slate-600 font-mono" title={doc.hash_sha256}>
                        {doc.hash_sha256.substring(0, 10)}...
                      </code>
                    </td>
                    <td className="py-3 px-4 text-center">
                      <a
                        href={`http://localhost:8000${doc.url_descarga}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white rounded text-xs font-medium transition-colors shadow-sm"
                      >
                        <Download className="w-3.5 h-3.5" />
                        Descargar
                      </a>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};