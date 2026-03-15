from EAPP import db
from models.payment_models import Payment
from werkzeug.exceptions import NotFound

class PaymentService:
    @staticmethod
    def create_payment(buyer_id, order_id, payment_amount, payment_type, payment_status='Pending', delivery_id=None, transaction_id=None):
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
        return new_payment

    @staticmethod
    def get_payment_by_id(payment_id):
        payment = Payment.query.get(payment_id)
        if not payment:
            raise NotFound('Payment not found')
        return payment

    @staticmethod
    def get_all_payments():
        return Payment.query.all()

    @staticmethod
    def update_payment(payment_id, buyer_id, order_id, payment_amount, payment_type, payment_status, delivery_id, transaction_id):
        payment = Payment.query.get(payment_id)
        if not payment:
            raise NotFound('Payment not found')

        payment.Buyer_Id = buyer_id
        payment.Order_Id = order_id
        payment.Payment_Amount = payment_amount
        payment.Payment_Type = payment_type
        payment.Payment_Status = payment_status
        payment.Delivery_Id = delivery_id
        payment.Transaction_Id = transaction_id

        db.session.commit()
        return payment

    @staticmethod
    def delete_payment(payment_id):
        payment = Payment.query.get(payment_id)
        if not payment:
            raise NotFound('Payment not found')

        db.session.delete(payment)
        db.session.commit()
        return {'message': 'Payment deleted successfully'}