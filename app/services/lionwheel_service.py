import requests
from config import Config

def create_lionwheel_task(data):
    """
    Create a task in Lionwheel system
    """
    response = requests.post(
        f"{Config.LIONWHEEL_URL}?key={Config.API_KEY}",
        json=data,
        headers={'Content-Type': 'application/json'}
    )
    response.raise_for_status()
    return response.json()