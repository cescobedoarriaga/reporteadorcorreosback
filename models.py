from pydantic import BaseModel

class correo (BaseModel):
    to: str
    subject: str
    mensaje: str
    attachment_base64: str
    file_name: str