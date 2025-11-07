from fastapi import APIRouter
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/contact", tags=["Contact"])

class ContactForm(BaseModel):
    name: str
    email: EmailStr
    message: str

@router.post("/")
async def send_contact_form(form: ContactForm):
    """Procesar formulario de contacto"""
    # Aquí puedes implementar envío de email
    # Por ahora solo retorna confirmación
    return {
        "message": "Mensaje recibido correctamente",
        "data": form.model_dump()
    }