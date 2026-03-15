from flask import request, jsonify
from ..models.order_models import Order
from EAPP import db

class OrderController:
    @staticmethod
    def get_all_orders():
        orders = Order.query.all()
        return jsonify([{
            'Order_Id': order.Order_Id,
            'User_Id': order.User_Id,
            'Order_Amount': str(order.Order_Amount)
        } for order in orders]), 200

    @staticmethod
    def get_order(order_id):
        order = Order.query.get(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        return jsonify({
            'Order_Id': order.Order_Id,
            'User_Id': order.User_Id,
            'Order_Amount': str(order.Order_Amount)
        }), 200

    @staticmethod
    def create_order():
        data = request.get_json()
        user_id = data.get('User_Id')
        order_amount = data.get('Order_Amount')

        new_order = Order(
            User_Id=user_id,
            Order_Amount=order_amount
        )
        
        db.session.add(new_order)
        db.session.commit()
        return jsonify({'message': 'Order created successfully', 'Order_Id': new_order.Order_Id}), 201

    @staticmethod
    def update_order(order_id):
        data = request.get_json()
        order = Order.query.get(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404

        order.Order_Amount = data.get('Order_Amount', order.Order_Amount)

        db.session.commit()
        return jsonify({'message': 'Order updated successfully'}), 200

    @staticmethod
    def delete_order(order_id):
        order = Order.query.get(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404

        db.session.delete(order)
        db.session.commit()
        return jsonify({'message': 'Order deleted successfully'}), 200