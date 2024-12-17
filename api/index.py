from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional

from api.config import Config
from api.services.baldar_service import transform_woo_to_baldar, create_baldar_task
from api.services.lionwheel_service import transform_woo_to_lionwheel, create_lionwheel_task

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Single Pydantic Model for Request Body
class CreateDeliveryRequest(BaseModel):
    id: str = Field(..., example="320457")
    number: str = Field(..., example="320457")
    date_created: str = Field(..., example="2023-12-14")
    customer_note: Optional[str] = Field("", example="פילמנט כתום")
    shipping: dict = Field(
        ...,
        example={
            "first_name": "אח",
            "last_name": "חינו",
            "address_1": "ויצמן 90",
            "address_2": "",
            "city": "תל אביב"
        }
    )
    billing: dict = Field(
        ...,
        example={
            "phone": "0584770076",
            "email": "idanbit80@gmail.com"
        }
    )


# Root Endpoint
@app.get("/", summary="API Home",
         description="Root endpoint with version status"
         )
def home():
    ver = 13
    return {"status": "ok", f"version {ver}": ver}


# Task Creation Endpoint
@app.post("/api/create-delivery",
          summary="Create Delivery Task",
          description="Create a delivery task for the specified company"
          )
def create_task(
        woo_order: CreateDeliveryRequest,
        method: str = Query(..., description="method name (e.g., lionWheel, cargo, sale4u)"),
        key: Optional[str] = Query(None, description="Token or Client ID")
):
    try:
        if method == "lionWheel":
            lionwheel_data = transform_woo_to_lionwheel(woo_order.dict())
            response = create_lionwheel_task(lionwheel_data, key)
            return response
        elif method in ["cargo", "sale4u"]:
            baldar_data = transform_woo_to_baldar(woo_order.dict(), key)
            api_url = (
                Config.BALDAR_CARGO_URL if method == "cargo"
                else Config.SALE4U_CARGO_URL
            )
            response = create_baldar_task(baldar_data, api_url)
            return response
        else:
            raise HTTPException(status_code=400, detail="Invalid company parameter")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create task: {str(e)}")
