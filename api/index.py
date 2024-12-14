from logging import log

from flask import Flask, request, jsonify
from flask_cors import CORS
import os

from api.services.baldar_service import transform_woo_to_baldar, create_baldar_task
from api.services.lionwheel_service import transform_woo_to_lionwheel, create_lionwheel_task

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return 'Hello, World V7'


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'})


@app.route('/api/create-delivery', methods=['POST'])
def create_task():
    try:
        woo_order = request.get_json()
        if not woo_order:
            return jsonify({'error': 'No data provided'}), 400

        company = request.args.get('Company')
        if not company:
            return jsonify({'error': 'Company parameter is required'}), 400

        if company == "MahirLi":
            lionwheel_data = transform_woo_to_lionwheel(woo_order)
            response = create_lionwheel_task(lionwheel_data)
            return jsonify(response)
        elif company == "Cargo":
            baldar_data = transform_woo_to_baldar(woo_order)
            response = create_baldar_task(baldar_data)
            print(response)
            return jsonify(response)
        else:
            return jsonify({'error': 'Invalid company parameter'}), 400
    except Exception as e:
        return jsonify({
            'error': 'Failed to create task',
            'details': str(e)
        }), 500
