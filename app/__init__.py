
from flask import Flask, jsonify
from .config import Config
from .models import petplanner
from .models.petplanner import db
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    print(f"{app.config}")

    from app.routes.user_route import users
    from app.routes.allergy_route import allergy
    from app.routes.pet_route import pets
    from app.routes.medical_event_route import medical_event
    app.register_blueprint(users, url_prefix="/users")
    app.register_blueprint(allergy, url_prefix="/allergy")
    app.register_blueprint(pets, url_prefix="/pets")
    app.register_blueprint(medical_event, url_prefix="/medical_event")


    @app.route("/")
    def index():
        return "PetPlanner"

    return app