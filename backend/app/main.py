from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.catalogo import router as catalogo_router

app = FastAPI(
    title="SGC Laboratorios API",
    description="Plataforma de Control Documental ISO 9001 y Evaluación In Situ",
    version="1.0.0"
)

# Configuración básica de CORS para permitir peticiones desde el frontend y PWA
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rutas bajo el prefijo institucional /api/v1
app.include_router(catalogo_router, prefix="/api/v1")

@app.get("/", tags=["Health Check"])
def read_root():
    return {
        "sistema": "Gestión de Calidad ISO 9001 - Laboratorios de Ingeniería",
        "estado": "Operativo",
        "version_api": "1.0.0"
    }