from EAPP import db
from datetime import datetime

class Delivery(db.Model):
    __tablename__ = 'Delivery'
    
    Delivery_Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Buyer_Id = db.Column(db.Integer, db.ForeignKey('Users.User_Id', ondelete="CASCADE"), nullable=False)
    Delivery_AID = db.Column(db.String(50), db.ForeignKey('Users.User_AID', ondelete="CASCADE"), nullable=False)
    Delivery_Address = db.Column(db.String(255), nullable=False)
    Delivery_Date = db.Column(db.Date)
    Delivery_Time = db.Column(db.Time)
    Delivery_Price = db.Column(db.Integer, nullable=False)

    #RELATIONSHIP;
    buyer = db.relationship('User', foreign_keys=[Buyer_Id], backref=db.backref('deliveries_as_buyer', lazy=True))
    aid_user = db.relationship('User', foreign_keys=[Delivery_AID], backref=db.backref('deliveries_as_aid', lazy=True))

    def to_dict(self):

        return {
            'Delivery_Id': self.Delivery_Id,
            'Buyer_Id': self.Buyer_Id,
            'Delivery_AID': self.Delivery_AID,
            'Delivery_Address': self.Delivery_Address,
            'Delivery_Date': self.Delivery_Date.strftime('%Y-%m-%d') if self.Delivery_Date else None,
            'Delivery_Time': self.Delivery_Time.strftime('%H:%M:%S') if self.Delivery_Time else None,
            'Delivery_Price': self.Delivery_Price
        }