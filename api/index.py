from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from api.config import Config, DeliveryMethod
from api.services.baldar_service import transform_woo_to_baldar, create_baldar_task, create_baldar_kamatra_task
from api.services.lionwheel_service import transform_woo_to_lionwheel, create_lionwheel_task
from api.services.models import WooAuthData, EmailRequest, CreateDeliveryRequest
from api.services.send_email import send_email
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import requests
import logging


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
    ver = 31
    return {"status": "ok", f"version {ver}": ver}


# Endpoint to handle WooCommerce callback
@app.post("/woo-auth-callback", summary="WooCommerce Auth Callback Handler")
async def handle_auth(data: WooAuthData):
    # Log the received data
    print("XXXX")
    print("Received WooCommerce Auth Data:", data)

    # Example response
    return {"status": "success", "message": "Auth data received successfully"}


@app.post("/api/send-email", summary="Send Email", description="Send an email to a specified recipient")
def send_email_endpoint(email_request: EmailRequest):
    return send_email(email_request.subject, email_request.body, email_request.to_email)


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


            # THAN HANDLING BALDAR METHODS
        elif method in DeliveryMethod.__members__:
            baldar_data = transform_woo_to_baldar(woo_order_data, key)
            api_url = DeliveryMethod[method].value  # Access Needed host Based eNum Key & Value
            response = create_baldar_task(baldar_data, api_url)
            return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create task: {str(e)}")



# Set up logging
logging.basicConfig(level=logging.INFO, format='BITON %(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

@app.get("/liorWaBot")
async def handle_get(request: Request):
    query_params = dict(request.query_params)
    logger.info(f"GET request received with query params: {query_params}")
    return JSONResponse(content={"status": "GET received", "data": query_params})


@app.post("/liorWaBot")
async def handle_post(request: Request):
    body = await request.json()
    logger.info(f"POST request received with body: {body}")

    # Check conditions
    if (
            body.get("typeWebhook") == "incomingMessageReceived" and
            body.get("senderData", {}).get("chatId") == "972503219900@c.us"
    ):
        # Send the message
        url = "https://7103.api.greenapi.com/waInstance7103154645/sendMessage/625b05dd2a5a4301a53550e8bdbd51810336b4be984c491c96"
        payload = {
            "chatId": "120363360946946323@g.us",
            "message": "היי לי אור, אני סופי (:"
        }
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(url, json=payload, headers=headers)
        logger.info(f"Message sent, response: {response.text}")

    return JSONResponse(content={"status": "POST received", "data": body})


