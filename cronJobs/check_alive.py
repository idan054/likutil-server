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
            send_email('SERVER IS DOWN', 'Oops, Looks like api.likutil.co.il Not Availble Right now...', 'idanbit80@gmail.com')
        else:
            send_email('GREAT! SERVER ALIVE', 'Just Ignore this Email, C U Next time...','idanbit80@gmail.com')
    except Exception as e:
        send_email('SERVER IS DOWN', 'Oops, Looks like api.likutil.co.il Not Availble Right now...', 'idanbit80@gmail.com')


check_server()
