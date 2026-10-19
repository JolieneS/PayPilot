import os
import base64

from email.message import EmailMessage
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/gmail.send"
]

BASE_DIR = Path(__file__).parent.parent
CREDENTIALS_FILE = BASE_DIR / "credentials.json"
TOKEN_FILE = BASE_DIR / "token.json"


def get_gmail_service():

    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(
            TOKEN_FILE,
            SCOPES
        )

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE,
                SCOPES
            )

            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    return build(
        "gmail",
        "v1",
        credentials=creds
    )


def send_payslip_email(
    employee_name: str,
    employee_email: str,
    month: str,
    net_salary: float,
    payslip_path: str,
):

    service = get_gmail_service()

    message = EmailMessage()

    message["To"] = employee_email
    message["Subject"] = f"Salary Payslip – {month}"

    body = f"""
Dear {employee_name},

Please find attached your salary payslip for {month}.

Net Salary: ₹{net_salary:,.2f}

Kindly review the details in the attached payslip.

Regards,
AI Payroll Assistant
"""

    message.set_content(body)

    with open(payslip_path, "rb") as file:
        pdf_data = file.read()

    message.add_attachment(
        pdf_data,
        maintype="application",
        subtype="pdf",
        filename=os.path.basename(payslip_path),
    )

    encoded_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    result = service.users().messages().send(
        userId="me",
        body={
            "raw": encoded_message
        }
    ).execute()

    return {
        "status": "sent",
        "recipient": employee_email,
        "payslip": payslip_path,
        "message_id": result["id"]
    }