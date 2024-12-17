import requests
from api.config import Config


from datetime import datetime
import random

def transform_woo_to_lionwheel(woo_order):
    """
    Transform WooCommerce order data to Lionwheel format
    """
    try:
        return {
            'pickup_at': datetime.strptime(woo_order['date_created'], '%Y-%m-%d').strftime('%d/%m/%Y'),
            'original_order_id': f"{woo_order['id']}-{random.randint(1000, 9999)}",
            'notes': f"Order #{woo_order['number']}",
            'packages_quantity': "1",
            'destination_city': woo_order['shipping']['city'],
            'destination_street': woo_order['shipping']['address_1'],
            'destination_number': woo_order['shipping']['address_2'] or "",
            'destination_floor': "",
            'destination_apartment': "",
            'destination_notes': f"Order #{woo_order['number']}\n{woo_order.get('customer_note', '')}",
            'destination_recipient_name': f"{woo_order['shipping']['first_name']} {woo_order['shipping']['last_name']}",
            'destination_phone': woo_order['billing']['phone'],
            'destination_email': woo_order['billing']['email']
        }
    except KeyError as e:
        raise Exception(f"Missing required field in WooCommerce order: {str(e)}")
    except ValueError as e:
        raise Exception(f"Invalid date format in WooCommerce order: {str(e)}")

def create_lionwheel_task(data, apiKey):
    """
    Create a task in Lionwheel system
    """
    try:
        response = requests.post(
            f"{Config.LIONWHEEL_URL}?key={apiKey}",
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Lionwheel API error: {str(e)}")