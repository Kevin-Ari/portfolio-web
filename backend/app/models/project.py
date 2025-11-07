from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from datetime import datetime
from ..database.connection import Base

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    image_url = Column(String(500), nullable=False)
    project_url = Column(String(500), nullable=False)  # URL del proyecto desplegado
    technologies = Column(String(500))  # JSON string: ["React", "FastAPI"]
    category = Column(String(100))  # "Web App", "Mobile", "API"
    is_featured = Column(Boolean, default=False)
    order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Project {self.title}>"