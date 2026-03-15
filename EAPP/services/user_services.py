from EAPP import db  
from ..models.user_models import User  

class UserService:
    @staticmethod
    def create_user(user_aid, user_address, user_type, user_fullname, user_email, user_password):

        new_user = User(
            User_AID=user_aid,
            User_Address=user_address,
            User_Type=user_type,
            User_Fullname=user_fullname,
            User_Email=user_email,
            User_Password_Hash=user_password
        )
        db.session.add(new_user)
        db.session.commit()

        return new_user

    @staticmethod
    def get_user_by_username(username):
        return User.query.filter_by(User_Fullname=username).first()  

    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def verify_user(username, password):
        user = User.query.filter_by(User_Fullname=username).first()  
        if user and user.User_Password_Hash == password:  
            return user
        return None
        