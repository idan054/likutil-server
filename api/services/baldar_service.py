import requests
from api.config import Config
from datetime import datetime
import random

def transform_woo_to_baldar(woo_order, clientId):
    """
    Transform WooCommerce order data to BALDAR format.
    """
    try:
        business_name = woo_order['business']['name']
        business_city = woo_order['business']['city']
        business_address = woo_order['business']['address']
        buyer_street = woo_order['shipping']['address_1']
        clean_address = woo_order['shipping']['address_1'] or ""
        buyer_city = woo_order['shipping']['city']
        buyer_name = f"{woo_order['shipping']['first_name']} {woo_order['shipping']['last_name']}"
        buyer_notes = woo_order.get('customer_note', '')
        pack_num = woo_order['pack_num']
        order_num = woo_order['number']
        buyer_phone = woo_order['billing']['phone']
        buyer_email = woo_order['billing']['email']

        p_param = (
            f"1;{business_address};{business_address};{business_city} ;{buyer_street};{clean_address};{buyer_city} ;"
            f"{business_name};{buyer_name} ; - {buyer_notes};1;1;1;"
            f"{pack_num};1;0;Woo #{order_num};{clientId};0;;0;עיר-מוצא-2;;"
            f"{buyer_email} - {buyer_phone};;0"
        )

        return p_param
    except KeyError as e:
        raise Exception(f"Missing required field in WooCommerce order: {str(e)}")
    except ValueError as e:
        raise Exception(f"Invalid date format in WooCommerce order: {str(e)}")

def create_baldar_task(p_param, host):
    """
    Create a task in BALDAR system.
    """
    try:
        print("host:", host)
        print("p_param:", p_param)
        response = requests.post(
            f"{host}/Baldarp/service.asmx/SaveData",
            data={"pParam": p_param},
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )

        # Ensure the request was successful
        response.raise_for_status()

        # Print and return the raw response text (XML or plain text)
        print("Response text:", response.text)
        return response.text
    except requests.exceptions.RequestException as e:
        raise Exception(f"Baldar API error: {str(e)}")


def create_baldar_kamatra_task(p_param, host):
    """
    Create a task in BALDAR system.
    """
    try:
        print("host:", host)
        print("p_param:", p_param)
        # THIS IS ACTUALLY JUST run_flask_kamertra_proxy.py BUT AS ISRAEL SERVER
        response = requests.post(
            f"{host}/negevKametraProxy",
            data=f"pParam={p_param}",
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )

        # Ensure the request was successful
        response.raise_for_status()

        # Print and return the raw response text (XML or plain text)
        print("Response text:", response.text)
        return response.text
    except requests.exceptions.RequestException as e:
        raise Exception(f"Baldar API error: {str(e)}")

