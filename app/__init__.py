
from flask import Flask, jsonify
from .config import Config
from .models.petplanner import db
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    print(f"{app.config}")

    from .routes.user_route import users
    app.register_blueprint(users, url_prefix="/users")


    @app.route("/")
    def index():
        return "PetPlanner"

    return app