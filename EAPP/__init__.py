from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    #REGISTER BLUEPRINTS;
    from .routes.user_routes import user_bp
    app.register_blueprint(user_bp)

    from .routes.product_routes import product_bp
    app.register_blueprint(product_bp)

    from .routes.category_routes import category_bp
    app.register_blueprint(category_bp) 

    from .routes.cart_routes import cart_bp
    app.register_blueprint(cart_bp) 

    from .routes.order_routes import order_bp
    app.register_blueprint(order_bp) 

    from .routes.delivery_routes import delivery_bp
    app.register_blueprint(delivery_bp) 

    from .routes.payment_routes import payment_bp
    app.register_blueprint(payment_bp) 

    #ROUTES TO RENDER HTML CODES;
    @app.route('/')
    def home():
        return render_template('snapshop.html')  

    @app.route('/register')
    def index():
        return render_template('register.html')

    @app.route('/categories')
    def categories():
        return render_template('categories.html')
    
    @app.route('/login')
    def login():
        return render_template('login.html')  
     
    @app.route('/products')
    def products():
        from .models.product_models import Product
        from .models.category_models import Category
        from flask import url_for
        
        products = Product.query.all()
        return render_template('products.html', products=[{
            'Product_Id': product.Product_Id,
            'Product_Name': product.Product_Name,
            'Product_Price': product.Product_Price,
            'Product_Rating': product.Product_Rating,
            'Product_Details': product.Product_Details,
            'Category_Name': Category.query.get(product.Category_Id).Category_Name if product.Category_Id else '',
            'image_url': url_for('static', filename=f'images/{product.Product_Id}.jpg')
        } for product in products])
    
    @app.route('/carts')
    def carts():
        return render_template('cart.html') 
    

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)