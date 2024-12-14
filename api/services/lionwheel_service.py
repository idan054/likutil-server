import requests
from api.config import Config

def create_lionwheel_task(data):
    """
    Create a task in Lionwheel system
    """
    try:
        response = requests.post(
            f"{Config.LIONWHEEL_URL}?key={Config.API_KEY}",
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        # Collect detailed request and response information
        error_details = {
            "error": str(e),
            "request": {
                "url": response.request.url if response else None,
                "method": response.request.method if response else None,
                "headers": dict(response.request.headers) if response else None,
                "body": response.request.body.decode('utf-8') if response and response.request.body else None,
            },
            "response": {
                "status_code": response.status_code if response else None,
                "reason": response.reason if response else None,
                "headers": dict(response.headers) if response else None,
                "body": response.text if response else None,
            },
        }
        raise Exception(f"Lionwheel API error: {error_details}")
