from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...database.connection import get_db
from ...models.project import Project
from ...schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.get("/", response_model=List[ProjectResponse])
def get_projects(
    skip: int = 0,
    limit: int = 100,
    featured: bool = None,
    db: Session = Depends(get_db)
):
    """Obtener todos los proyectos"""
    query = db.query(Project)
    
    if featured is not None:
        query = query.filter(Project.is_featured == featured)
    
    projects = query.order_by(Project.order).offset(skip).limit(limit).all()
    return projects

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    """Obtener un proyecto específico"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return project

@router.post("/", response_model=ProjectResponse)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    """Crear un nuevo proyecto"""
    db_project = Project(**project.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project: ProjectUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar un proyecto"""
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    
    for key, value in project.model_dump(exclude_unset=True).items():
        setattr(db_project, key, value)
    
    db.commit()
    db.refresh(db_project)
    return db_project

@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    """Eliminar un proyecto"""
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    
    db.delete(db_project)
    db.commit()
    return {"message": "Proyecto eliminado exitosamente"}

