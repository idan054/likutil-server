from fastapi import FastAPI, HTTPException
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



# Email Configuration
EMAIL_USERNAME = "eyalspider3d@gmail.com"
EMAIL_PASSWORD = "urxb beml qwha ooma"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Function to send an email
def send_email(subject: str, body: str, to_email: str):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USERNAME
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.send_message(msg)
        return {"message": f"Email sent successfully to {to_email}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")