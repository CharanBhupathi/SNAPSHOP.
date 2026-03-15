from flask import request, jsonify
from ..models.category_models import Category
from EAPP import db

class CategoryController:
    @staticmethod
    def get_all_categories():
        categories = Category.query.all()
        return jsonify([{'Category_Id': category.Category_Id, 'Category_Name': category.Category_Name} for category in categories]), 200

    @staticmethod
    def get_category(category_id):
        category = Category.query.get(category_id)
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        return jsonify({'Category_Id': category.Category_Id, 'Category_Name': category.Category_Name}), 200

    @staticmethod
    def create_category():
        data = request.get_json()
        category_name = data.get('Category_Name')

        new_category = Category(
            Category_Name=category_name
        )

        db.session.add(new_category)
        db.session.commit()
        return jsonify({'message': 'Category created successfully', 'Category_Id': new_category.Category_Id}), 201

    @staticmethod
    def update_category(category_id):
        category = Category.query.get(category_id)
        if not category:
            return jsonify({'error': 'Category not found'}), 404

        data = request.get_json()
        category_name = data.get('Category_Name', category.Category_Name)

        category.Category_Name = category_name
        db.session.commit()

        return jsonify({'message': 'Category updated successfully'}), 200

    @staticmethod
    def delete_category(category_id):
        category = Category.query.get(category_id)
        if not category:
            return jsonify({'error': 'Category not found'}), 404

        db.session.delete(category)
        db.session.commit()

        return jsonify({'message': 'Category deleted successfully'}), 200