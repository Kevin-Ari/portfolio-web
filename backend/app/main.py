from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
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


# === Servir Frontend ===
try:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    FRONTEND_DIR = BASE_DIR / "frontend"

    print(f"📂 FRONTEND_DIR = {FRONTEND_DIR}")

    if FRONTEND_DIR.exists() and FRONTEND_DIR.is_dir():
        index_path = FRONTEND_DIR / "index.html"

        if index_path.exists():
            # Rutas estáticas separadas para evitar conflictos con /api
            app.mount("/css", StaticFiles(directory=FRONTEND_DIR / "css"), name="css")
            app.mount("/js", StaticFiles(directory=FRONTEND_DIR / "js"), name="js")

            @app.get("/")
            async def serve_index():
                return FileResponse(index_path)

            print(f"✅ Frontend mounted successfully from: {FRONTEND_DIR}")
        else:
            raise FileNotFoundError("index.html not found in frontend directory")
    else:
        raise FileNotFoundError("Frontend directory does not exist")

except Exception as e:
    print(f"⚠️ Could not mount frontend: {e}")
    print("📡 Running in API-only mode")

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


# === Run ===
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8080)),  # ✅ Usa el puerto dinámico de Railway
        reload=settings.RELOAD
    )
