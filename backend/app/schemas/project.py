from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime

class ProjectBase(BaseModel):
    title: str
    description: str
    image_url: str
    project_url: str
    technologies: Optional[str] = None
    category: Optional[str] = None
    is_featured: bool = False
    order: int = 0

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    project_url: Optional[str] = None
    technologies: Optional[str] = None
    category: Optional[str] = None
    is_featured: Optional[bool] = None
    order: Optional[int] = None

class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True