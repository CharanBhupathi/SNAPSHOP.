from EAPP import db
from models.delivery_models import Delivery
from werkzeug.exceptions import NotFound

class DeliveryService:
    @staticmethod
    def create_delivery(buyer_id, delivery_aid, delivery_address, delivery_date, delivery_time, delivery_price):
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
        return new_delivery

    @staticmethod
    def get_delivery_by_id(delivery_id):
        delivery = Delivery.query.get(delivery_id)
        if not delivery:
            raise NotFound('Delivery not found')
        return delivery

    @staticmethod
    def get_all_deliveries():
        return Delivery.query.all()

    @staticmethod
    def update_delivery(delivery_id, delivery_address=None, delivery_date=None, delivery_time=None, delivery_price=None):
        delivery = Delivery.query.get(delivery_id)
        if not delivery:
            raise NotFound('Delivery not found')

        delivery.Delivery_Address = delivery_address if delivery_address is not None else delivery.Delivery_Address
        delivery.Delivery_Date = delivery_date if delivery_date is not None else delivery.Delivery_Date
        delivery.Delivery_Time = delivery_time if delivery_time is not None else delivery.Delivery_Time
        delivery.Delivery_Price = delivery_price if delivery_price is not None else delivery.Delivery_Price

        db.session.commit()
        return delivery

    @staticmethod
    def delete_delivery(delivery_id):
        delivery = Delivery.query.get(delivery_id)
        if not delivery:
            raise NotFound('Delivery not found')

        db.session.delete(delivery)
        db.session.commit()
        return {'message': 'Delivery deleted successfully'}