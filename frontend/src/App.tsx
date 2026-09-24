import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { CatalogoPublico } from './components/CatalogoPublico';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-slate-50 flex flex-col">
        {/* Encabezado Institucional */}
        <header className="bg-slate-900 text-white shadow-md border-b-4 border-blue-600">
          <div className="max-w-6xl mx-auto px-4 py-5 flex justify-between items-center">
            <div>
              <h1 className="text-xl md:text-2xl font-bold tracking-tight">Sistema de Gestión de Calidad (SGC)</h1>
              <p className="text-slate-400 text-xs md:text-sm mt-0.5">Laboratorios de Ingeniería — Control Documental NMX-CC-9001-IMNC-2015</p>
            </div>
            <div className="hidden sm:block text-right">
              <span className="text-xs bg-slate-800 text-slate-300 border border-slate-700 px-2.5 py-1 rounded">
                Consulta Pública
              </span>
            </div>
          </div>
        </header>

        {/* Contenedor Principal */}
        <main className="flex-grow max-w-6xl w-full mx-auto p-4 md:p-6">
          <Routes>
            <Route path="/" element={<CatalogoPublico />} />
          </Routes>
        </main>

        {/* Pie de página de Calidad */}
        <footer className="bg-white border-t border-slate-200 py-4 text-center text-xs text-slate-500">
          Documentación controlada conforme a la cláusula 7.5 de la norma ISO 9001:2015. Prohibida su alteración.
        </footer>
      </div>
    </Router>
  );
}

export default App;