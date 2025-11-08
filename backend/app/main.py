from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os
from .config import settings
from .database.connection import engine, Base
from .api.routes import projects, services, contact

# Crear tablas
Base.metadata.create_all(bind=engine)

# Inicializar FastAPI
app = FastAPI(
    title="Portfolio API",
    description="API para portfolio personal",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(projects.router, prefix="/api")
app.include_router(services.router, prefix="/api")
app.include_router(contact.router, prefix="/api")

# Health check (debe estar ANTES del mount de frontend)
@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "API is running"}

# Intentar montar frontend solo si existe
try:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    FRONTEND_DIR = BASE_DIR / "frontend"
    
    if FRONTEND_DIR.exists() and FRONTEND_DIR.is_dir():
        # Verificar que tenga archivos
        if any(FRONTEND_DIR.iterdir()):
            app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
            print(f"✅ Frontend mounted from: {FRONTEND_DIR}")
        else:
            print(f"⚠️ Frontend directory exists but is empty: {FRONTEND_DIR}")
            raise FileNotFoundError("Frontend directory is empty")
    else:
        print(f"⚠️ Frontend directory not found: {FRONTEND_DIR}")
        raise FileNotFoundError("Frontend directory does not exist")
        
except Exception as e:
    print(f"⚠️ Could not mount frontend: {e}")
    print("📡 Running in API-only mode")
    
    # Ruta raíz alternativa si no hay frontend
    @app.get("/")
    def read_root():
        return {
            "message": "Portfolio API - Running in API-only mode",
            "status": "ok",
            "endpoints": {
                "docs": "/docs",
                "redoc": "/redoc",
                "health": "/api/health",
                "projects": "/api/projects",
                "services": "/api/services",
                "contact": "/api/contact"
            }
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.RELOAD
    )