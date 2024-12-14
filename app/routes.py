from flask import Blueprint, request, jsonify
from app.services.lionwheel_service import create_lionwheel_task
from app.utils.transformers import transform_woo_to_lionwheel

api_bp = Blueprint('api', __name__)

@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'Version' : 2})

@api_bp.route('/api/create-task', methods=['POST'])
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