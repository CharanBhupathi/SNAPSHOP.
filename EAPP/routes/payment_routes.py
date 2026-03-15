from flask import Blueprint
from ..controllers.payment_controllers import PaymentController

payment_bp = Blueprint('payment_bp', __name__)

@payment_bp.route('/api/payments', methods=['POST'])
def create_payment():
    return PaymentController.create_payment()

@payment_bp.route('/api/payments', methods=['GET'])
def get_all_payments():
    return PaymentController.get_all_payments()

@payment_bp.route('/api/payments/<int:payment_id>', methods=['GET'])
def get_payment(payment_id):
    return PaymentController.get_payment(payment_id)

@payment_bp.route('/api/payments/<int:payment_id>', methods=['PUT'])
def update_payment(payment_id):
    return PaymentController.update_payment(payment_id)

@payment_bp.route('/api/payments/<int:payment_id>', methods=['DELETE'])
def delete_payment(payment_id):
    return PaymentController.delete_payment(payment_id)