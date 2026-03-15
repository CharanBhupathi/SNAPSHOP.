from flask import request, jsonify
from ..models.cart_models import Cart
from EAPP import db

class CartController:
    @staticmethod
    def get_all_carts(user_id):
        carts = Cart.query.filter_by(User_Id=user_id).all()
        return jsonify([{
            'Cart_Id': cart.Cart_Id,
            'Product_Id': cart.Product_Id,
            'User_Id': cart.User_Id,
            'Cart_Size': cart.Cart_Size,
            'Product_Quantity': cart.Product_Quantity,
            'Cart_Amount': float(cart.Cart_Amount)
        } for cart in carts]), 200

    @staticmethod
    def get_cart(cart_id):
        cart = Cart.query.get(cart_id)
        if not cart:
            return jsonify({'error': 'Cart not found'}), 404
        return jsonify({
            'Cart_Id': cart.Cart_Id,
            'Product_Id': cart.Product_Id,
            'User_Id': cart.User_Id,
            'Cart_Size': cart.Cart_Size,
            'Product_Quantity': cart.Product_Quantity,
            'Cart_Amount': float(cart.Cart_Amount)
        }), 200

    @staticmethod
    def add_to_cart():
        data = request.get_json()
        product_id = data.get('Product_Id')
        user_id = data.get('User_Id')
        cart_size = data.get('Cart_Size')
        product_quantity = data.get('Product_Quantity', 1)
        product_price = data.get('Product_Price')

        if not all([product_id, user_id, product_price]):
            return jsonify({'error': 'Missing required fields'}), 400

        # Calculate cart amount
        cart_amount = float(product_price) * product_quantity

        # Check if the SAME product with SAME size is already in cart
        existing_cart = Cart.query.filter_by(
            Product_Id=product_id,
            User_Id=user_id,
            Cart_Size=cart_size
        ).first()
        
        if existing_cart:
            # If it's the same product with same size, update the quantity instead
            existing_cart.Product_Quantity += product_quantity
            existing_cart.Cart_Amount = float(product_price) * existing_cart.Product_Quantity
            db.session.commit()
            return jsonify({'message': 'Updated product quantity in cart', 'Cart_Id': existing_cart.Cart_Id}), 200

        # Create new cart item if product doesn't exist in cart
        new_cart = Cart(
            Product_Id=product_id,
            User_Id=user_id,
            Cart_Size=cart_size,
            Product_Quantity=product_quantity,
            Cart_Amount=cart_amount
        )
        
        db.session.add(new_cart)
        db.session.commit()
        return jsonify({'message': 'Added to cart successfully', 'Cart_Id': new_cart.Cart_Id}), 201

    @staticmethod
    def update_cart(cart_id):
        data = request.get_json()
        cart = Cart.query.get(cart_id)
        if not cart:
            return jsonify({'error': 'Cart not found'}), 404

        product_quantity = data.get('Product_Quantity')
        if product_quantity is not None:
            cart.Product_Quantity = product_quantity
            # Recalculate cart amount based on new quantity
            product_price = float(cart.product.Product_Price)
            cart.Cart_Amount = product_price * product_quantity

        cart.Cart_Size = data.get('Cart_Size', cart.Cart_Size)

        db.session.commit()
        return jsonify({'message': 'Cart updated successfully'}), 200

    @staticmethod
    def delete_cart(cart_id):
        cart = Cart.query.get(cart_id)
        if not cart:
            return jsonify({'error': 'Cart not found'}), 404

        db.session.delete(cart)
        db.session.commit()
        return jsonify({'message': 'Cart deleted successfully'}), 200