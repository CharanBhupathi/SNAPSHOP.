from EAPP import db
from models.category_models import Category

class CategoryService:
    @staticmethod
    def create_category(category_name):
        new_category = Category(
            Category_Name=category_name
        )
        db.session.add(new_category)
        db.session.commit()
        return new_category

    @staticmethod
    def get_all_categories():
        return Category.query.all()

    @staticmethod
    def get_category_by_id(category_id):
        return Category.query.get(category_id)

    @staticmethod
    def update_category(category_id, category_name):
        category = Category.query.get(category_id)
        if category:
            category.Category_Name = category_name
            db.session.commit()
            return category
        return None

    @staticmethod
    def delete_category(category_id):
        category = Category.query.get(category_id)
        if category:
            db.session.delete(category)
            db.session.commit()
            return category
        return None