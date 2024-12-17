from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    PORT = int(os.getenv('PORT', 5005))
    LIONWHEEL_URL = 'https://members.lionwheel.com/api/v1/tasks/create'

    # Baldar HOSTS:
    BALDAR_CARGO_URL = 'http://45.83.40.28'
    SALE4U_CARGO_URL = 'http://185.108.80.50:8050'
