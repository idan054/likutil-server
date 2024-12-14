from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from api.services.lionwheel_service import create_lionwheel_task
from api.utils.transformers import transform_woo_to_lionwheel

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return 'Hello, World X'

@app.route('/about')
def about():
    return 'About'


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'})


@app.route('/api/create-task', methods=['POST'])
def create_task():
    try:
        woo_order = request.get_json()
        if not woo_order:
            return jsonify({'error': 'No data provided'}), 400

        lionwheel_data = transform_woo_to_lionwheel(woo_order)
        response = create_lionwheel_task(lionwheel_data)

        return jsonify(response)
    except Exception as e:
        return jsonify({
            'error': 'Failed to create task',
            'details': str(e)
        }), 500