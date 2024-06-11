from flask import Flask
from app.extensions import db, migrate, bcrypt
from app.controllers.user_controller import user_bp
from app.controllers.teammember_controller import teammember_bp
from app.controllers.orderItem_controller import order_item_bp
from app.controllers.order_controller import order_bp
from app.controllers.merchandise_controller import merchandise_bp
from app.controllers.event_controller import event_bp
from app.controllers.donation_controller import donation_bp
from app.controllers.contact_controller import contact_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.config')
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)  
    #jwt.init_app(app)     

    # Importing and registering models
    from app.models.user import User
    from app.models.teammember import TeamMember
    from app.models.orderItem import OrderItem
    from app.models.order import Order
    from app.models.merchanise import Merchandise 
    from app.models.event import Event
    from app.models.donation import Donation
    from app.models.contact import Contact

    # Registering blueprints 
    app.register_blueprint(user_bp)
    app.register_blueprint(teammember_bp)
    app.register_blueprint(order_item_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(merchandise_bp)
    app.register_blueprint(event_bp)
    app.register_blueprint(donation_bp)
    app.register_blueprint(contact_bp)
    
    @app.route("/") 
    def home():
        return "Website Api"

    return app
