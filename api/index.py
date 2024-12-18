from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from api.config import Config, DeliveryMethod
from api.services.baldar_service import transform_woo_to_baldar, create_baldar_task, create_baldar_kamatra_task
from api.services.lionwheel_service import transform_woo_to_lionwheel, create_lionwheel_task
from api.services.send_email import send_email

app = FastAPI()


# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root Endpoint
@app.get("/", summary="API Version Checker",
         description="Root endpoint with version status"
         )
def home():
    ver = 28
    return {"status": "ok", f"version {ver}": ver}


# Pydantic Model for Email
class EmailRequest(BaseModel):
    subject: str = Field(..., example="Test Email")
    body: str = Field(..., example="This is a test email body.")
    to_email: str = Field(..., example="idanbit80@gmail.com")


@app.post("/api/send-email", summary="Send Email", description="Send an email to a specified recipient")
def send_email_endpoint(email_request: EmailRequest):
    return send_email(email_request.subject, email_request.body, email_request.to_email)


# Single Pydantic Model for Request Body
class CreateDeliveryRequest(BaseModel):
    pack_num: str = Field(..., example="1")
    id: str = Field(..., example="000000")
    number: str = Field(..., example="000000")
    date_created: str = Field(..., example="2003-01-03")
    customer_note: Optional[str] = Field("", example="יש לבטל! בדיקת חיבור לחברת משלוחים בלבד!")
    shipping: Dict[str, str] = Field(
        ...,
        example={
            "first_name": "לא",
            "last_name": "לשלוח",
            "address_1": "ויצמן 90",
            "address_2": "",
            "city": "תל אביב"
        }
    )
    billing: Dict[str, str] = Field(
        ...,
        example={
            "phone": "0584770076",
            "email": "idanbit80@gmail.com"
        }
    )
    business: Dict[str, str] = Field(
        ...,
        example={
            "name": "בדיקת בלבד!",
            "city": "תל אביב",
            "address": "ויצמן 91"
        }
    )



@app.post("/api/create-delivery", summary="Create Delivery Task",
          description="Create a delivery task for the specified company")
def create_task(
        woo_order: Optional[CreateDeliveryRequest] = None,
        method: str = Query(..., description="", enum=list(DeliveryMethod.__members__.keys())),
        key: Optional[str] = Query(None, description="Token or Client ID"),
        isConnectionTest: bool = Query(False, description="Use predefined test data (true/false)")
):
    try:
        # If isConnectionTest is True, use test data
        if isConnectionTest:
            woo_order_data = Config.TEST_WOO_ORDER
        else:
            if woo_order is None:
                raise HTTPException(status_code=400, detail="woo_order data is required")
            woo_order_data = woo_order.dict()

            # HANDLING ANY NON CUSTOM NON-BALDAR METHOD
        if method == "lionWheel":
            lionwheel_data = transform_woo_to_lionwheel(woo_order_data)
            response = create_lionwheel_task(lionwheel_data, key)
            return response

        if method == "negevExpressMyKametra":
            baldar_data = transform_woo_to_baldar(woo_order_data, key)
            response = create_baldar_kamatra_task(baldar_data, DeliveryMethod.negevExpressMyKametra.value)
            return response

            # THAN HANDLING BALDAR METHODS
        elif method in DeliveryMethod.__members__:
            baldar_data = transform_woo_to_baldar(woo_order_data, key)
            api_url = DeliveryMethod[method].value  # Access Needed host Based eNum Key & Value
            response = create_baldar_task(baldar_data, api_url)
            return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create task: {str(e)}")
