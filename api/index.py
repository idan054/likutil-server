from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from api.config import Config, DeliveryMethod
from api.services.baldar_service import transform_woo_to_baldar, create_baldar_task, create_baldar_kamatra_task
from api.services.lionwheel_service import transform_woo_to_lionwheel, create_lionwheel_task
from api.services.models import WooAuthData, EmailRequest, CreateDeliveryRequest
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
    ver = 30
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
