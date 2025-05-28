
from flask import Flask, jsonify, request
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
    from app.routes.notification_route import notification
    app.register_blueprint(users, url_prefix="/users")
    app.register_blueprint(allergy, url_prefix="/allergy")
    app.register_blueprint(pets, url_prefix="/pets")
    app.register_blueprint(medical_event, url_prefix="/medical_event")
    app.register_blueprint(notification, url_prefix="/notification")

    @app.route("/")
    def index():
        return "PetPlanner"

    @app.route("/reset-password", methods=["GET"])
    def reset_password_form():
        token = request.args.get("token")

        if not token:
            return "<h3>Token inválido o faltante.</h3>", 400

        return f"""\
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>Cambiar contraseña - PetPlanner</title>
            <style>
                body {{ font-family: Arial; background: #f4f4f4; padding: 30px; }}
                .container {{ max-width: 400px; margin: auto; background: #fff; padding: 20px; border-radius: 8px; }}
                input[type="password"] {{ width: 100%; padding: 10px; margin-top: 10px; }}
                button {{ margin-top: 15px; padding: 10px; width: 100%; background-color: #4CAF50; color: white; border: none; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Restablece tu contraseña</h2>
                <form method="POST" action="/users/reset-password">
                    <input type="hidden" name="token" value="{token}" />
                    <label for="password">Nueva contraseña:</label>
                    <input type="password" name="password" required />

                    <label for="confirm">Confirmar contraseña:</label>
                    <input type="password" name="confirm" required />

                    <button type="submit">Cambiar contraseña</button>
                </form>
            </div>
        </body>
        </html>
        """

    return app