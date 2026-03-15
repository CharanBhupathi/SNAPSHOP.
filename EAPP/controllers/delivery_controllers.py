from flask import request, jsonify
from ..models.delivery_models import Delivery
from EAPP import db

class DeliveryController:
    @staticmethod
    def get_all_deliveries():
        deliveries = Delivery.query.all()
        return jsonify([delivery.to_dict() for delivery in deliveries]), 200
    
    @staticmethod
    def get_delivery(delivery_id):
        delivery = Delivery.query.get(delivery_id)
        if not delivery:
            return jsonify({'error': 'Delivery not found'}), 404
        return jsonify({
            'Delivery_Id': delivery.Delivery_Id,
            'Buyer_Id': delivery.Buyer_Id,
            'Delivery_AID': delivery.Delivery_AID,
            'Delivery_Address': delivery.Delivery_Address,
            'Delivery_Date': delivery.Delivery_Date,
            'Delivery_Time': delivery.Delivery_Time,
            'Delivery_Price': delivery.Delivery_Price
        }), 200

    @staticmethod
    def create_delivery():
        data = request.get_json()
        buyer_id = data.get('Buyer_Id')
        delivery_aid = data.get('Delivery_AID')
        delivery_address = data.get('Delivery_Address')
        delivery_date = data.get('Delivery_Date')
        delivery_time = data.get('Delivery_Time')
        delivery_price = data.get('Delivery_Price')

        new_delivery = Delivery(
            Buyer_Id=buyer_id,
            Delivery_AID=delivery_aid,
            Delivery_Address=delivery_address,
            Delivery_Date=delivery_date,
            Delivery_Time=delivery_time,
            Delivery_Price=delivery_price
        )
        
        db.session.add(new_delivery)
        db.session.commit()
        return jsonify({
            'message': 'Delivery created successfully',
            'Delivery_Id': new_delivery.Delivery_Id
        }), 201

    @staticmethod
    def update_delivery(delivery_id):
        data = request.get_json()
        delivery = Delivery.query.get(delivery_id)
        if not delivery:
            return jsonify({'error': 'Delivery not found'}), 404

        delivery.Delivery_Address = data.get('Delivery_Address', delivery.Delivery_Address)
        delivery.Delivery_Date = data.get('Delivery_Date', delivery.Delivery_Date)
        delivery.Delivery_Time = data.get('Delivery_Time', delivery.Delivery_Time)
        delivery.Delivery_Price = data.get('Delivery_Price', delivery.Delivery_Price)

        db.session.commit()
        return jsonify({'message': 'Delivery updated successfully'}), 200

    @staticmethod
    def delete_delivery(delivery_id):
        delivery = Delivery.query.get(delivery_id)
        if not delivery:
            return jsonify({'error': 'Delivery not found'}), 404

        db.session.delete(delivery)
        db.session.commit()
        return jsonify({'message': 'Delivery deleted successfully'}), 200