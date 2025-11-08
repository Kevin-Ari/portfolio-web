from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from pathlib import Path
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

# === API ROUTES ===
app.include_router(projects.router, prefix="/api")
app.include_router(services.router, prefix="/api")
app.include_router(contact.router, prefix="/api")

@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "API is running"}

# === FRONTEND SETUP ===
BASE_DIR = Path(__file__).resolve().parent.parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

print(f"\n{'='*60}")
print(f"🔍 FRONTEND DEBUG INFO:")
print(f"📂 BASE_DIR: {BASE_DIR}")
print(f"📂 FRONTEND_DIR: {FRONTEND_DIR}")
print(f"✅ Frontend directory exists: {FRONTEND_DIR.exists()}")

if FRONTEND_DIR.exists():
    print(f"\n📁 Frontend structure:")
    for item in sorted(FRONTEND_DIR.rglob("*")):
        if item.is_file():
            rel_path = item.relative_to(FRONTEND_DIR)
            print(f"   📄 {rel_path}")
        elif item.is_dir() and item != FRONTEND_DIR:
            rel_path = item.relative_to(FRONTEND_DIR)
            print(f"   📁 {rel_path}/")
print(f"{'='*60}\n")

# Montar archivos estáticos ANTES de las rutas dinámicas
if FRONTEND_DIR.exists():
    # Montar carpetas específicas
    css_dir = FRONTEND_DIR / "css"
    js_dir = FRONTEND_DIR / "js"
    assets_dir = FRONTEND_DIR / "assets"
    
    if css_dir.exists():
        app.mount("/css", StaticFiles(directory=str(css_dir)), name="css")
        print("✅ Mounted /css")
    
    if js_dir.exists():
        app.mount("/js", StaticFiles(directory=str(js_dir)), name="js")
        print("✅ Mounted /js")
    
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")
        print("✅ Mounted /assets")
    
    print()

# Servir index.html en la ruta raíz
@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_path = FRONTEND_DIR / "index.html"
    
    if index_path.exists():
        print(f"✅ Serving index.html from: {index_path}")
        return FileResponse(index_path)
    else:
        print(f"⚠️ index.html not found at: {index_path}")
        # Debug page
        content = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Portfolio - Debug Mode</title>
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    padding: 40px 20px;
                }}
                .container {{
                    max-width: 900px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 12px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                    overflow: hidden;
                }}
                .header {{
                    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                }}
                .content {{
                    padding: 30px;
                }}
                h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
                h2 {{ color: #333; margin: 25px 0 15px; border-left: 4px solid #667eea; padding-left: 12px; }}
                .error {{ color: #e74c3c; font-weight: bold; }}
                .success {{ color: #27ae60; font-weight: bold; }}
                code {{
                    background: #f4f4f4;
                    padding: 2px 8px;
                    border-radius: 4px;
                    font-family: 'Courier New', monospace;
                    color: #e74c3c;
                }}
                ul {{ margin: 10px 0 20px 20px; line-height: 1.8; }}
                .api-links {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 15px;
                    margin: 20px 0;
                }}
                .api-link {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 15px;
                    border-radius: 8px;
                    text-decoration: none;
                    text-align: center;
                    transition: transform 0.2s;
                    font-weight: 500;
                }}
                .api-link:hover {{
                    transform: translateY(-3px);
                    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
                }}
                .steps {{
                    background: #f8f9fa;
                    padding: 20px;
                    border-radius: 8px;
                    border-left: 4px solid #27ae60;
                }}
                .steps ol {{
                    margin-left: 20px;
                }}
                .steps li {{
                    margin: 10px 0;
                    line-height: 1.6;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⚠️ Frontend Debug Mode</h1>
                    <p>La API está funcionando correctamente</p>
                </div>
                <div class="content">
                    <p class="error">❌ <strong>index.html no encontrado</strong></p>
                    
                    <h2>📂 Información de Rutas</h2>
                    <ul>
                        <li><strong>Buscando:</strong> <code>{index_path}</code></li>
                        <li><strong>Directorio frontend:</strong> <code>{FRONTEND_DIR}</code></li>
                        <li><strong>Existe:</strong> <span class="{'success' if FRONTEND_DIR.exists() else 'error'}">{FRONTEND_DIR.exists()}</span></li>
                    </ul>
                    
                    <h2>📁 Contenido del Directorio Frontend</h2>
                    <ul>
                        {''.join([f'<li>{"📄" if item.is_file() else "📁"} {item.relative_to(FRONTEND_DIR)}</li>' for item in sorted(FRONTEND_DIR.rglob("*")) if item != FRONTEND_DIR]) if FRONTEND_DIR.exists() else '<li class="error">El directorio no existe</li>'}
                    </ul>
                    
                    <h2>✅ Endpoints de la API Funcionando</h2>
                    <div class="api-links">
                        <a href="/docs" class="api-link">📚 Documentación</a>
                        <a href="/api/health" class="api-link">💚 Health Check</a>
                        <a href="/api/projects" class="api-link">📁 Proyectos</a>
                        <a href="/api/services" class="api-link">🛠️ Servicios</a>
                    </div>
                    
                    <h2>🔧 Cómo Solucionarlo</h2>
                    <div class="steps">
                        <ol>
                            <li>Crea el archivo <code>frontend/index.html</code> en tu proyecto</li>
                            <li>Asegúrate de hacer commit: <code>git add frontend/index.html</code></li>
                            <li>Sube los cambios: <code>git push origin main</code></li>
                            <li>Railway desplegará automáticamente</li>
                        </ol>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        return HTMLResponse(content=content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.RELOAD
    )