from EAPP import db

class Product(db.Model):
    __tablename__ = 'Products'
    
    Product_Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Seller_Id = db.Column(db.Integer, db.ForeignKey('Users.User_Id', ondelete="CASCADE"), nullable=False)
    Category_Id = db.Column(db.Integer, db.ForeignKey('Categories.Category_Id', ondelete="CASCADE"), nullable=False)
    Product_Name = db.Column(db.String(50), nullable=False)
    Product_Price = db.Column(db.Integer, nullable=True)
    Product_Rating = db.Column(db.Float, nullable=True)
    Product_Details = db.Column(db.Text, nullable=True)

    #RELATIONSHIP;
    seller = db.relationship('User', backref=db.backref('products', lazy=True))
    category = db.relationship('Category', backref=db.backref('products', lazy=True))