from pydantic import BaseModel, Field
from pydantic import BaseModel
from typing import Optional, Dict, Any


# Model for handling received WooCommerce auth data
class WooAuthData(BaseModel):
    key_id: int
    user_id: int
    consumer_key: str
    consumer_secret: str
    key_permissions: str


# Pydantic Model for Email
class EmailRequest(BaseModel):
    subject: str = Field(..., example="Test Email")
    body: str = Field(..., example="This is a test email body.")
    to_email: str = Field(..., example="idanbit80@gmail.com")


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


# Define a generic model for request bodies
class RequestBodyModel(BaseModel):
    data: Optional[Dict[str, Any]] = None
