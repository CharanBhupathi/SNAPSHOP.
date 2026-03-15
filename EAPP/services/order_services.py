from EAPP import db
from models.order_models import Order
from werkzeug.exceptions import NotFound

class OrderService:
    @staticmethod
    def create_order(user_id, order_amount):
        new_order = Order(
            User_Id=user_id,
            Order_Amount=order_amount
        )
        db.session.add(new_order)
        db.session.commit()
        return new_order

    @staticmethod
    def get_order_by_id(order_id):
        order = Order.query.get(order_id)
        if not order:
            raise NotFound('Order not found')
        return order

    @staticmethod
    def get_all_orders():
        return Order.query.all()

    @staticmethod
    def update_order(order_id, order_amount=None):
        order = Order.query.get(order_id)
        if not order:
            raise NotFound('Order not found')

        order.Order_Amount = order_amount if order_amount is not None else order.Order_Amount
        
        db.session.commit()
        return order

    @staticmethod
    def delete_order(order_id):
        order = Order.query.get(order_id)
        if not order:
            raise NotFound('Order not found')

        db.session.delete(order)
        db.session.commit()
        return {'message': 'Order deleted successfully'}