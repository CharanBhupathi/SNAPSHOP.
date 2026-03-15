from EAPP import db

class Category(db.Model):
    __tablename__ = 'Categories'

    Category_Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Category_Name = db.Column(db.String(50), nullable=False)

    #RELATIONSHIP;
    category = db.relationship('Product')