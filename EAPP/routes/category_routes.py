from flask import Blueprint
from ..controllers.category_controllers import CategoryController

category_bp = Blueprint('category_bp', __name__)

@category_bp.route('/api/categories', methods=['GET'])
def get_all_categories():
    return CategoryController.get_all_categories()

@category_bp.route('/api/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    return CategoryController.get_category(category_id)

@category_bp.route('/api/categories', methods=['POST'])
def create_category():
    return CategoryController.create_category()

@category_bp.route('/api/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    return CategoryController.update_category(category_id)

@category_bp.route('/api/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    return CategoryController.delete_category(category_id)