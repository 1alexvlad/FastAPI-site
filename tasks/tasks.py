from tasks.celery import celery
from pathlib import Path
from pydantic import EmailStr
from config import settings
from tasks.email_templates import create_booking_confirmation_template
import smtplib

@celery.task
def send_booking_confirmation_email(
    booking: dict,
    email_to: EmailStr
):  
    
    email_to_mock = settings.SMTP_USER 
    msg_content = create_booking_confirmation_template(booking, email_to_mock)
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)

