from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..config import settings

# Crear engine para PostgreSQL
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Verifica conexión antes de usar
    echo=False  # Cambia a True para ver queries SQL
)

# Crear sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos
Base = declarative_base()

# Dependency para obtener DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()