import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

# Настройка SMTP (замените на свои данные)
conf = ConnectionConfig(
    MAIL_USERNAME="siterate272026@mail.ru",
    MAIL_PASSWORD="oUj9xeJyMN8w1qeahpfI",  # Пароль приложения
    MAIL_FROM="siterate272026@mail.ru",
    MAIL_PORT=465,  
    MAIL_SERVER="smtp.mail.ru",
    MAIL_SSL_TLS=True,  
    MAIL_STARTTLS=False,
    USE_CREDENTIALS=True,
)

async def send_simple_email(email_to: str, subject: str, body: str):
    """Просто отправляет письмо на указанный email"""
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=body,
        subtype="plain" 
    )
    
    fm = FastMail(conf)
    await fm.send_message(message)