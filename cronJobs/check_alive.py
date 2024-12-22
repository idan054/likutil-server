import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../..')

import requests
from api.services.send_email import send_email

def check_server():
    try:
        response = requests.get("https://api.likutil.co.il")
        if response.status_code != 200:
            send_email(subject='SERVER IS DOWN', body='Please check the server.')
        else:
            send_email(subject='GREAT! SERVER ALIVE', body='The server is running fine.')
    except Exception as e:
        send_email(subject='SERVER IS DOWN', body=f'Error: {e}')

check_server()
