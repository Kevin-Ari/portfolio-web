from sqlalchemy import Column, Integer, String, Text
from ..database.connection import Base

class Service(Base):
    __tablename__ = "services"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    icon = Column(String(100))  # Nombre del icono (ej: "code", "design")
    order = Column(Integer, default=0)
    
    def __repr__(self):
        return f"<Service {self.title}>"