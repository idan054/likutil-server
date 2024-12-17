from enum import Enum
from dotenv import load_dotenv
import os

load_dotenv()


class DeliveryMethod(str, Enum):
    lionWheel = "lionWheel"

    # BALDAR
    cargo = 'http://45.83.40.28'
    sale4u = 'http://185.108.80.50:8050'
    sDeliveries = 'https://sdelivery.xsyspro.net:8022'
    negevExpress = 'http://crm.negevdelivery.co.il'
    whatever = 'http://not-gonna-work.co.il'


class Config:
    PORT = int(os.getenv('PORT', 5005))
    LIONWHEEL_URL = 'https://members.lionwheel.com/api/v1/tasks/create'

    # Default Test Data
    TEST_WOO_ORDER = {
        "pack_num": "1",
        "id": "000000",
        "number": "000000",
        "date_created": "2003-01-03",
        "customer_note": "יש לבטל! בדיקת חיבור לחברת משלוחים בלבד!",
        "shipping": {
            "first_name": "לא",
            "last_name": "לשלוח",
            "address_1": "ויצמן 90",
            "address_2": "",
            "city": "תל אביב"
        },
        "billing": {
            "phone": "0584770076",
            "email": "idanbit80@gmail.com"
        },
        "business": {
            "name": "בדיקת בלבד!",
            "city": "תל אביב",
            "address": "ויצמן 91"
        }
    }
