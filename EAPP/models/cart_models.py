from EAPP import db

class Cart(db.Model):
    __tablename__ = 'Cart'
    
    Cart_Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Product_Id = db.Column(db.Integer, db.ForeignKey('Products.Product_Id', ondelete="CASCADE"), nullable=False)
    Cart_Size = db.Column(db.Integer)
    Product_Quantity = db.Column(db.Integer)
    Cart_Amount = db.Column(db.Float)
    User_Id = db.Column(db.Integer, db.ForeignKey('Users.User_Id', ondelete="CASCADE"), nullable=False)

    #RELATIONSHIP;
    product = db.relationship('Product', backref=db.backref('carts', lazy=True))
    user = db.relationship('User', backref=db.backref('carts', lazy=True))