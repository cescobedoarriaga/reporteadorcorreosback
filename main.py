import base64
import email
from fastapi import FastAPI
import smtplib
from email.message import EmailMessage
from jproperties import Properties
from models import correo

app = FastAPI(openapi_url="/messengerws/openapi.json", docs_url="/messengerws/docs", redoc_url="/messengerws/redoc")

configs = Properties()
with open('email.properties', 'rb') as read_prop:
        configs.load(read_prop, "utf-8")

@app.post("/messengerws/send-email")
async def send_email(correo: correo):
    try:
        # Crear un mensaje de correo electrónico
        email_message = EmailMessage()
        email_message["From"] = configs.get("EMAIL_USERNAME").data 
        email_message["To"] = correo.to
        email_message["Subject"] = correo.subject
        email_message.set_content(correo.mensaje)
        
        # Decodificar la cadena Base64 y adjuntarla si se proporciona
        if correo.attachment_base64:
            attachment_data = base64.b64decode(correo.attachment_base64)

            # Especificar el nombre del archivo y el tipo MIME
            attachment_filename = f'{correo.file_name}.xlsx'  # Nombre del archivo Excel
            attachment_mimetype = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            email_message.add_attachment(
                attachment_data,
                filename=attachment_filename,
                maintype="application",
                subtype=attachment_mimetype
            )

        # Establecer una conexión con el servidor de correo electrónico
        with smtplib.SMTP(configs.get("EMAIL_HOST").data, configs.get("EMAIL_PORT").data) as server:
            server.starttls()
            server.login(configs.get("EMAIL_USERNAME").data, configs.get("EMAIL_PASSWORD").data)

            # Enviar el correo electrónico
            server.send_message(email_message)

        return {"message": "Correo electrónico enviado exitosamente"}
    except Exception as e:
        return {"message": f"Error al enviar el correo electrónico: {str(e)}"}