from flask import Blueprint, render_template, request, jsonify
from ..controllers.cart_controllers import CartController
from ..models.cart_models import Cart
from EAPP import db

cart_bp = Blueprint('cart_bp', __name__)

#✅ Add product to cart (prevent duplicates)
@cart_bp.route('/api/carts', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    # Handle both lowercase and capitalized field names for compatibility
    user_id = data.get('user_id') or data.get('User_Id')
    product_id = data.get('product_id') or data.get('Product_Id')
    quantity = data.get('quantity') or data.get('Product_Quantity', 1)
    size = data.get('size') or data.get('Cart_Size', 0)
    price = data.get('price') or data.get('Product_Price')

    if not all([user_id, product_id, price]):
        return jsonify({'error': 'Missing required fields'}), 400

    # Convert size to appropriate format (handle string sizes like 'S', 'M', 'L', 'XL')
    if isinstance(size, str):
        # Map string sizes to numbers if needed, or keep as string
        # For now, we'll keep it as is since Cart_Size is Integer in model
        # If you need to store string sizes, you might need to change the model
        size_map = {'S': 1, 'M': 2, 'L': 3, 'XL': 4}
        size = size_map.get(size.upper(), 0) if size.upper() in size_map else 0
    elif size is None:
        size = 0

    # Check if already in cart based on product_id and size
    existing_item = Cart.query.filter_by(User_Id=user_id, Product_Id=product_id, Cart_Size=size).first()

    if existing_item:
        # Update quantity if item already exists
        existing_item.Product_Quantity += int(quantity)
        existing_item.Cart_Amount = float(price) * existing_item.Product_Quantity
        db.session.commit()
        return jsonify({'message': 'Product quantity updated in cart', 'Cart_Id': existing_item.Cart_Id}), 200

    new_item = Cart(
        User_Id=user_id,
        Product_Id=product_id,
        Product_Quantity=int(quantity),
        Cart_Size=int(size) if size else 0,
        Cart_Amount=float(price) * int(quantity)
    )
    db.session.add(new_item)
    db.session.commit()

    return jsonify({'message': 'Product added to cart', 'Cart_Id': new_item.Cart_Id}), 201

# ✅ Get all items in user's cart
@cart_bp.route('/api/users/<int:user_id>/carts', methods=['GET'])
def get_user_carts(user_id):
    return CartController.get_all_carts(user_id)

# ✅ Clear cart completely for user
@cart_bp.route('/api/users/<int:user_id>/carts', methods=['DELETE'])
def clear_user_cart(user_id):
    Cart.query.filter_by(User_Id=user_id).delete()
    db.session.commit()
    return jsonify({'message': 'Cart cleared successfully'}), 200

# ✅ Get single cart item by cart ID
@cart_bp.route('/api/carts/<int:cart_id>', methods=['GET'])
def get_cart(cart_id):
    return CartController.get_cart(cart_id)

# ✅ Update cart item by cart ID
@cart_bp.route('/api/carts/<int:cart_id>', methods=['PUT'])
def update_cart(cart_id):
    return CartController.update_cart(cart_id)

# ✅ Delete a specific cart item
@cart_bp.route('/api/carts/<int:cart_id>', methods=['DELETE'])
def delete_cart(cart_id):
    return CartController.delete_cart(cart_id)

# ✅ Sync cart (used in frontend sync logic)
@cart_bp.route('/api/carts/sync', methods=['POST'])
def sync_cart():
    data = request.get_json()
    user_id = data.get('user_id') or data.get('User_Id')
    cart_items = data.get('cart_items', [])

    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    # Clear old items
    existing_items = Cart.query.filter_by(User_Id=user_id).all()
    for item in existing_items:
        db.session.delete(item)
    db.session.commit()

    # Add new ones - handle both field name formats
    for item in cart_items:
        product_id = item.get('id') or item.get('Product_Id') or item.get('product_id')
        quantity = item.get('quantity') or item.get('Product_Quantity', 1)
        size = item.get('size') or item.get('Cart_Size', 0)
        price = item.get('price') or item.get('Product_Price') or item.get('Product_Price')
        
        if not product_id or not price:
            continue  # Skip invalid items
            
        # Convert string sizes to numbers if needed
        if isinstance(size, str):
            size_map = {'S': 1, 'M': 2, 'L': 3, 'XL': 4}
            size = size_map.get(size.upper(), 0) if size.upper() in size_map else 0
        elif size is None:
            size = 0
            
        new_cart = Cart(
            Product_Id=product_id,
            User_Id=user_id,
            Cart_Size=int(size) if size else 0,
            Product_Quantity=int(quantity),
            Cart_Amount=float(price) * int(quantity)
        )
        db.session.add(new_cart)

    db.session.commit()
    return jsonify({'message': 'Cart synced successfully'}), 200

# ✅ (Optional) Render cart page
@cart_bp.route('/cart', methods=['GET'])
def view_cart():
    return render_template('cart.html')