from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
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

# Servir archivos estáticos del frontend
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.RELOAD
    )