from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...database.connection import get_db
from ...models.service import Service
from ...schemas.service import ServiceCreate, ServiceUpdate, ServiceResponse

router = APIRouter(prefix="/services", tags=["Services"])

@router.get("/", response_model=List[ServiceResponse])
def get_services(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtener todos los servicios"""
    services = db.query(Service).order_by(Service.order).offset(skip).limit(limit).all()
    return services

@router.post("/", response_model=ServiceResponse)
def create_service(service: ServiceCreate, db: Session = Depends(get_db)):
    """Crear un nuevo servicio"""
    db_service = Service(**service.model_dump())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service