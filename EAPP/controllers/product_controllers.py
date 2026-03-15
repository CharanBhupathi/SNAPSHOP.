from flask import request, jsonify
from ..models.product_models import Product
from EAPP import db
from ..models.category_models import Category  # Import Category model

class ProductController:
    @staticmethod
    def get_all_products():
        products = Product.query.all()
        return jsonify([{
            'Product_Id': product.Product_Id,
            'Seller_Id': product.Seller_Id,
            'Category_Id': product.Category_Id,
            'Product_Name': product.Product_Name,
            'Product_Price': product.Product_Price,
            'Product_Rating': product.Product_Rating,
            'Product_Details': product.Product_Details
        } for product in products]), 200

    @staticmethod
    def get_product(product_id):
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        return jsonify({
            'Product_Id': product.Product_Id,
            'Seller_Id': product.Seller_Id,
            'Category_Id': product.Category_Id,
            'Product_Name': product.Product_Name,
            'Product_Price': product.Product_Price,
            'Product_Rating': product.Product_Rating,
            'Product_Details': product.Product_Details

        }), 200

    @staticmethod
    def create_product():
        data = request.get_json()
        seller_id = data.get('Seller_Id')
        category_id = data.get('Category_Id')
        product_name = data.get('Product_Name')
        product_price = data.get('Product_Price')
        product_rating = data.get('Product_Rating')
        product_details = data.get('Product_Details')

        # Check if the category exists
        category = Category.query.get(category_id)
        if not category:
            return jsonify({'error': 'Category not found'}), 404

        new_product = Product(
            Seller_Id=seller_id,
            Category_Id=category_id,
            Product_Name=product_name,
            Product_Price=product_price,
            Product_Rating=product_rating,
            Product_Details=product_details
        )
        
        db.session.add(new_product)
        db.session.commit()
        return jsonify({'message': 'Product created successfully', 'Product_Id': new_product.Product_Id}), 201

    @staticmethod
    def update_product(product_id):
        data = request.get_json()
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404

        # Check if the category exists before updating
        category_id = data.get('Category_Id')
        if category_id:
            category = Category.query.get(category_id)
            if not category:
                return jsonify({'error': 'Category not found'}), 404

        product.Product_Name = data.get('Product_Name', product.Product_Name)
        product.Product_Price = data.get('Product_Price', product.Product_Price)
        product.Product_Rating = data.get('Product_Rating', product.Product_Rating)
        product.Product_Details = data.get('Product_Details', product.Product_Details)

        product.Category_Id = data.get('Category_Id', product.Category_Id)

        db.session.commit()
        return jsonify({'message': 'Product updated successfully'}), 200

    @staticmethod
    def delete_product(product_id):
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404

        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully'}), 200

    # New method to get products by category
    @staticmethod
    def get_products_by_category():
        # Get category from request args
        category_name = request.args.get('category')
        if not category_name:
            return jsonify({'error': 'Category is required'}), 400
        
        # Fetch the products by category
        category = Category.query.filter_by(Category_Name=category_name).first()
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        
        products = Product.query.filter_by(Category_Id=category.Category_Id).all()

        return jsonify([{
            'Product_Id': product.Product_Id,
            'Product_Name': product.Product_Name,
            'Product_Price': product.Product_Price,
            'Product_Rating': product.Product_Rating,
            'Product_Details': product.Product_Details,
        } for product in products]), 200
    