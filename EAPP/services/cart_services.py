from EAPP import db
from models.cart_models import Cart
from models.product_models import Product
from werkzeug.exceptions import NotFound

class CartService:
    @staticmethod
    def get_cart_items(user_id):
        return Cart.query.filter_by(User_Id=user_id).all()

    @staticmethod
    def add_to_cart(product_id, user_id, cart_size, quantity=1):
        # Get product price
        product = Product.query.get(product_id)
        if not product:
            raise ValueError("Product not found")

        # Check if product is already in cart
        existing_cart = Cart.query.filter_by(
            Product_Id=product_id,
            User_Id=user_id,
            Cart_Size=cart_size
        ).first()

        if existing_cart:
            # If it's the same product with same size, update the quantity instead
            existing_cart.Product_Quantity += quantity
            existing_cart.Cart_Amount = float(product.Product_Price) * existing_cart.Product_Quantity
            db.session.commit()
            return existing_cart

        # Calculate cart amount
        cart_amount = float(product.Product_Price) * quantity

        new_cart = Cart(
            Product_Id=product_id,
            User_Id=user_id,
            Cart_Size=cart_size,
            Product_Quantity=quantity,
            Cart_Amount=cart_amount
        )
        
        db.session.add(new_cart)
        db.session.commit()
        return new_cart

    @staticmethod
    def update_cart_item(cart_id, quantity=None, cart_size=None):
        cart = Cart.query.get(cart_id)
        if not cart:
            raise ValueError("Cart item not found")

        if quantity is not None:
            cart.Product_Quantity = quantity
            # Recalculate cart amount
            product_price = float(cart.product.Product_Price)
            cart.Cart_Amount = product_price * quantity

        if cart_size is not None:
            cart.Cart_Size = cart_size

        db.session.commit()
        return cart

    @staticmethod
    def remove_from_cart(cart_id):
        cart = Cart.query.get(cart_id)
        if not cart:
            raise ValueError("Cart item not found")

        db.session.delete(cart)
        db.session.commit()
        return True

    @staticmethod
    def clear_cart(user_id):
        Cart.query.filter_by(User_Id=user_id).delete()
        db.session.commit()
        return True

    @staticmethod
    def get_cart_total(user_id):
        cart_items = Cart.query.filter_by(User_Id=user_id).all()
        return sum(float(item.Cart_Amount) for item in cart_items)

    @staticmethod
    def sync_cart(user_id, cart_items):
        # Clear existing cart items
        Cart.query.filter_by(User_Id=user_id).delete()

        # Add new cart items
        for item in cart_items:
            product = Product.query.get(item['Product_Id'])
            if product:
                cart_amount = float(product.Product_Price) * item['Product_Quantity']
                new_cart = Cart(
                    Product_Id=item['Product_Id'],
                    User_Id=user_id,
                    Cart_Size=item['Cart_Size'],
                    Product_Quantity=item['Product_Quantity'],
                    Cart_Amount=cart_amount
                )
                db.session.add(new_cart)

        db.session.commit()
        return True

    @staticmethod
    def get_cart_by_id(cart_id):
        cart = Cart.query.get(cart_id)
        if not cart:
            raise NotFound('Cart item not found')
        return cart

    @staticmethod
    def get_all_carts():
        return Cart.query.all()

    @staticmethod
    def update_cart(cart_id, cart_size=None, product_quantity=None, cart_amount=None):
        cart = Cart.query.get(cart_id)
        if not cart:
            raise NotFound('Cart item not found')
        
        cart.Cart_Size = cart_size if cart_size is not None else cart.Cart_Size
        cart.Product_Quantity = product_quantity if product_quantity is not None else cart.Product_Quantity
        cart.Cart_Amount = cart_amount if cart_amount is not None else cart.Cart_Amount
        
        db.session.commit()
        return cart

    @staticmethod
    def delete_cart(cart_id):
        cart = Cart.query.get(cart_id)
        if not cart:
            raise NotFound('Cart item not found')
        
        db.session.delete(cart)
        db.session.commit()
        return {'message': 'Cart item deleted successfully'}