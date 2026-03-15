from flask import request, jsonify
from ..models.user_models import User
from EAPP import db

class UserController:
    @staticmethod
    def get_all_users():
        users = User.query.all()
        return jsonify([
            {'User_Id': user.User_Id, 'User_Fullname': user.User_Fullname, 'User_Email': user.User_Email, 'User_Type': user.User_Type}
            for user in users
        ]), 200

    @staticmethod
    def get_user(user_id):
        user = User.query.get(user_id)
        if not user:  # if user is None
            return jsonify({'error': 'User not found'}), 404
        return jsonify({
            'User_Id': user.User_Id,
            'User_Fullname': user.User_Fullname,
            'User_Email': user.User_Email,
            'User_Type': user.User_Type
        }), 200

    @staticmethod
    def create_user():
        data = request.get_json()
        user_aid = data.get('User_AID')
        user_address = data.get('User_Address')
        user_type = data.get('User_Type')
        user_fullname = data.get('User_Fullname')
        user_email = data.get('User_Email')
        user_password_hash = data.get('User_Password_Hash')

                # Check if email already exists
        existing_user = User.query.filter_by(User_Email=user_email).first()
        if existing_user:
            return jsonify({'error': 'Email already registered'}), 409
        
        new_user = User(
            User_AID=user_aid,
            User_Address=user_address,
            User_Type=user_type,
            User_Fullname=user_fullname,
            User_Email=user_email,
            User_Password_Hash=user_password_hash
        )
        
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully', 'User_Id': new_user.User_Id}), 201

    @staticmethod
    def login_user():
        data = request.get_json()
        user_email = data.get('User_Email')
        user_password_hash = data.get('User_Password_Hash')  # This should typically be a hashed password

        # Check if the user exists
        user = User.query.filter_by(User_Email=user_email).first()

        if user:
            # Log the stored password and the provided password
            print(f"Stored password: {user.User_Password_Hash}")
            print(f"Provided password: {user_password_hash}")

            # Validate password
            if user.User_Password_Hash == user_password_hash:
                return jsonify({
                    'message': 'Login successful',
                    'User_Id': user.User_Id,
                    'User_Fullname': user.User_Fullname,
                    'User_Email': user.User_Email,
                    'User_Type': user.User_Type
                }), 200
            else:
                return jsonify({'error': 'Invalid password'}), 401
        else:
            # If email doesn't exist, inform user to register
            return jsonify({'error': 'Email not registered. Please register first.'}), 404

    @staticmethod
    def get_current_user():
        # Get the session token from the request
        session_token = request.headers.get('Authorization')
        if not session_token:
            return jsonify({'error': 'No session token provided'}), 401

        # In a real application, you would validate the session token here
        # For now, we'll just return the user ID from the token
        try:
            # This is a placeholder - in a real app, you would decode the JWT token
            # or look up the session in your database
            user_id = session_token.split(' ')[1]  # Assuming format "Bearer <user_id>"
            user = User.query.get(user_id)
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
                
            return jsonify({
                'User_Id': user.User_Id,
                'User_Fullname': user.User_Fullname,
                'User_Email': user.User_Email,
                'User_Type': user.User_Type
            }), 200
        except Exception as e:
            return jsonify({'error': 'Invalid session token'}), 401