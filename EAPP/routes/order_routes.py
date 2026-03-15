from flask import Blueprint
from ..controllers.order_controllers import OrderController

order_bp = Blueprint('order_bp', __name__)

@order_bp.route('/api/orders', methods=['POST'])
def create_order():
    return OrderController.create_order()

@order_bp.route('/api/orders', methods=['GET'])
def get_all_orders():
    return OrderController.get_all_orders()

@order_bp.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    return OrderController.get_order(order_id)

@order_bp.route('/api/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    return OrderController.update_order(order_id)

@order_bp.route('/api/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    return OrderController.delete_order(order_id)