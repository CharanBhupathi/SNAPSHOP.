from EAPP import db

class User(db.Model):
    __tablename__ = 'Users'
    
    User_Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    User_AID = db.Column(db.Integer, unique=True)
    User_Address = db.Column(db.String(255), nullable=False)
    User_Type = db.Column(db.Enum('Seller', 'Buyer'), nullable=False)
    User_Fullname = db.Column(db.String(50), nullable=False)
    User_Email = db.Column(db.String(50), unique=True, nullable=False)
    User_Password_Hash = db.Column(db.String(255), nullable=False)