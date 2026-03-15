from flask import Blueprint
from ..controllers.delivery_controllers import DeliveryController

delivery_bp = Blueprint('delivery_bp', __name__)

@delivery_bp.route('/api/deliveries', methods=['POST'])
def create_delivery():
    return DeliveryController.create_delivery()

@delivery_bp.route('/api/deliveries', methods=['GET'])
def get_all_deliveries():
    return DeliveryController.get_all_deliveries()

@delivery_bp.route('/api/deliveries/<int:delivery_id>', methods=['GET'])
def get_delivery(delivery_id):
    return DeliveryController.get_delivery(delivery_id)

@delivery_bp.route('/api/deliveries/<int:delivery_id>', methods=['PUT'])
def update_delivery(delivery_id):
    return DeliveryController.update_delivery(delivery_id)

@delivery_bp.route('/api/deliveries/<int:delivery_id>', methods=['DELETE'])
def delete_delivery(delivery_id):
    return DeliveryController.delete_delivery(delivery_id)