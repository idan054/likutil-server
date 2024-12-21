from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from flask import Flask, request, jsonify
import logging
from google.cloud.firestore_v1 import SERVER_TIMESTAMP
from starlette.responses import JSONResponse

from api.config import Config, DeliveryMethod
from api.services.baldar_service import transform_woo_to_baldar, create_baldar_task, create_baldar_kamatra_task
from api.services.clean_url import sanitize_url
from api.services.lionwheel_service import transform_woo_to_lionwheel, create_lionwheel_task
from api.services.models import WooAuthData, EmailRequest, CreateDeliveryRequest
from api.services.send_email import send_email
import firebase_admin
from firebase_admin import firestore, credentials
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

import firebase_admin
from firebase_admin import credentials

code1 = './likutil-firebase-adminsdk'
code2 = '-bbpdy-adb99de0cf.json'
cred = credentials.Certificate(f"{code1}{code2}")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.post("/woo-auth-callback", summary="WooCommerce Auth Callback Handler")
async def handle_auth(data: WooAuthData, request: Request):
    try:
        # Extract store URL from the Referer header
        referer = request.headers.get("referer", "").strip()
        store_url = sanitize_url(referer)

        # Reference to the user's document
        user_ref = db.collection("users").document(str(data.user_id))
        user_doc = user_ref.get()

        # Prepare the user data
        user_data = {
            "lastLogin": datetime.utcnow(),
            "storeUrl": store_url,
            "consumerKey": data.consumer_key,
            "consumerSecret": data.consumer_secret,
            "userId": data.user_id,
            "key_permissions": data.key_permissions,
            "key_id": data.key_id,
        }

        # Set `createdAt` only if it doesn't exist
        if not user_doc.exists or "createdAt" not in user_doc.to_dict():
            user_data["createdAt"] = SERVER_TIMESTAMP

        # Save to Firestore
        user_ref.set(user_data, merge=True)

        return {"status": "success", "message": "User data saved to Firestore"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Root Endpoint
@app.get("/", summary="API Version Checker",
         description="Root endpoint with version status"
         )
def home():
    ver = 33
    return {"status": "ok", f"version {ver}": ver}


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


        # All BALDAR: cargo, sale4u, sDeliveries, negevExpress
        elif method in DeliveryMethod.__members__:
            baldar_data = transform_woo_to_baldar(woo_order_data, key)
            api_url = DeliveryMethod[method].value  # Access Needed host Based eNum Key & Value
            response = create_baldar_task(baldar_data, api_url)
            return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create task: {str(e)}")


# Configure logging to output to the console and to Nginx logs
logging.basicConfig(
    level=logging.INFO,
    format="Biton: %(asctime)s - %(levelname)s - %(message)s",
)


@app.api_route("/liorWaBot", methods=["GET", "POST"])
async def lior_wa_bot(request: Request):
    # Log request method and headers
    logging.info(f"Request Method: {request.method}")
    logging.info(f"Request Headers: {dict(request.headers)}")

    if request.method == "POST":
        body = await request.json()  # Get JSON body for POST request
        logging.info(f"POST Request Body: {body}")
        print(f"POST Request Body: {body}")
        return JSONResponse({"status": "POST received", "data": body})

    elif request.method == "GET":
        query_params = dict(request.query_params)  # Get query parameters for GET request
        logging.info(f"GET Request Query Params: {query_params}")
        print(f"GET Request Query Params: {query_params}")
        return JSONResponse({"status": "GET received", "params": query_params})

    return JSONResponse({"error": "Invalid method"}, status_code=405)
