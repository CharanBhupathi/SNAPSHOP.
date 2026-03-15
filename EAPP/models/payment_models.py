from EAPP import db

class Payment(db.Model):
    __tablename__ = 'Payments'

    Payment_Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Buyer_Id = db.Column(db.Integer, db.ForeignKey('Users.User_Id', ondelete="CASCADE"), nullable=False)
    Order_Id = db.Column(db.Integer, db.ForeignKey('Orders.Order_Id', ondelete="CASCADE"), nullable=False)
    Payment_Amount = db.Column(db.Numeric(10, 2))
    Payment_Type = db.Column(db.Enum('Credit_Card', 'Debit_Card', 'COD', 'UPI'), nullable=False)
    Payment_Status = db.Column(db.Enum('Pending', 'Successful', 'Failed'), nullable=False, default='Pending')
    Payment_Time = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    Delivery_Id = db.Column(db.Integer, db.ForeignKey('Delivery.Delivery_Id', ondelete="CASCADE"))
    Transaction_Id = db.Column(db.String(255), unique=True)

    # Relationships
    buyer = db.relationship('User', backref=db.backref('payments', lazy=True))
    order = db.relationship('Order', backref=db.backref('payments', lazy=True))
    delivery = db.relationship('Delivery', backref=db.backref('payments', lazy=True))