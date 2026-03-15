from flask import request, jsonify
from ..models.payment_models import Payment
from EAPP import db

class PaymentController:
    @staticmethod
    def get_all_payments():
        payments = Payment.query.all()
        return jsonify([{
            'Payment_Id': payment.Payment_Id,
            'Buyer_Id': payment.Buyer_Id,
            'Order_Id': payment.Order_Id,
            'Payment_Amount': payment.Payment_Amount,
            'Payment_Type': payment.Payment_Type,
            'Payment_Status': payment.Payment_Status,
            'Payment_Time': payment.Payment_Time,
            'Delivery_Id': payment.Delivery_Id,
            'Transaction_Id': payment.Transaction_Id
        } for payment in payments]), 200

    @staticmethod
    def get_payment(payment_id):
        payment = Payment.query.get(payment_id)
        if not payment:
            return jsonify({'error': 'Payment not found'}), 404
        return jsonify({
            'Payment_Id': payment.Payment_Id,
            'Buyer_Id': payment.Buyer_Id,
            'Order_Id': payment.Order_Id,
            'Payment_Amount': payment.Payment_Amount,
            'Payment_Type': payment.Payment_Type,
            'Payment_Status': payment.Payment_Status,
            'Payment_Time': payment.Payment_Time,
            'Delivery_Id': payment.Delivery_Id,
            'Transaction_Id': payment.Transaction_Id
        }), 200

    @staticmethod
    def create_payment():
        data = request.get_json()
        buyer_id = data.get('Buyer_Id')
        order_id = data.get('Order_Id')
        payment_amount = data.get('Payment_Amount')
        payment_type = data.get('Payment_Type')
        payment_status = data.get('Payment_Status', 'Pending')
        delivery_id = data.get('Delivery_Id')
        transaction_id = data.get('Transaction_Id')

        new_payment = Payment(
            Buyer_Id=buyer_id,
            Order_Id=order_id,
            Payment_Amount=payment_amount,
            Payment_Type=payment_type,
            Payment_Status=payment_status,
            Delivery_Id=delivery_id,
            Transaction_Id=transaction_id
        )

        db.session.add(new_payment)
        db.session.commit()
        return jsonify({'message': 'Payment created successfully', 'Payment_Id': new_payment.Payment_Id}), 201

    @staticmethod
    def update_payment(payment_id):
        data = request.get_json()
        payment = Payment.query.get(payment_id)
        if not payment:
            return jsonify({'error': 'Payment not found'}), 404

        payment.Payment_Amount = data.get('Payment_Amount', payment.Payment_Amount)
        payment.Payment_Type = data.get('Payment_Type', payment.Payment_Type)
        payment.Payment_Status = data.get('Payment_Status', payment.Payment_Status)
        payment.Delivery_Id = data.get('Delivery_Id', payment.Delivery_Id)
        payment.Transaction_Id = data.get('Transaction_Id', payment.Transaction_Id)

        db.session.commit()
        return jsonify({'message': 'Payment updated successfully'}), 200

    @staticmethod
    def delete_payment(payment_id):
        payment = Payment.query.get(payment_id)
        if not payment:
            return jsonify({'error': 'Payment not found'}), 404

        db.session.delete(payment)
        db.session.commit()
        return jsonify({'message': 'Payment deleted successfully'}), 200