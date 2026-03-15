from EAPP import db

class Order(db.Model):
    __tablename__ = 'Orders'

    Order_Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    User_Id = db.Column(db.Integer, db.ForeignKey('Users.User_Id', ondelete='CASCADE'), nullable=False)  
    Order_Amount = db.Column(db.Numeric(10, 2), default=0.00, nullable=False)

    user = db.relationship('User', backref=db.backref('orders', lazy=True))

    def __init__(self, User_Id, Order_Amount):
        self.User_Id = User_Id
        self.Order_Amount = Order_Amount

    def to_dict(self):
        return {
            'Order_Id': self.Order_Id,
            'User_Id': self.User_Id,
            'Order_Amount': str(self.Order_Amount)
        }