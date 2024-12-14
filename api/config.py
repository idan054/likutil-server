from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    PORT = int(os.getenv('PORT', 5005))
    API_KEY = 'c_key_3694a9a7-6993-4d4a-8016-cedf0759f9eb'
    LIONWHEEL_URL = 'https://members.lionwheel.com/api/v1/tasks/create'