from flask import request, jsonify
import smtplib
from email.message import EmailMessage
import os
from app.utils.auth import generate_token
from app.utils.validators import validate_email, validate_password
from app.models.petplanner import User, db
from app.models.role import Role
from werkzeug.security import generate_password_hash, check_password_hash


def create_user():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")
    role = Role.DEFAULT_ROLE.value


    if not email or not password or not name or not role:
        return jsonify({"message": "No data provided"}), 400

    is_valid_email, email_msg = validate_email(email)
    if not is_valid_email:
        return jsonify({"message": email_msg}), 400

    is_valid_password, password_msg = validate_password(password)
    if not is_valid_password:
        return jsonify({"message": password_msg}), 400

    try:
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"message": "User already exists"}), 400

        new_user = User(
            name=name,
            email=email,
            password = generate_password_hash(password),
            role=role,
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "Successfully created user", "data": new_user.to_json()}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def get_token():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "No data provided"}), 400
    try:
        user = User.query.filter_by(email=email).first()

        if not user:
            return jsonify({"message": "User not found"}), 404

        if check_password_hash(user.password, password):
            return jsonify({"message": "Successfully logged", "token": generate_token(user)}), 200
        else:
            return jsonify({"message": "Wrong password"}), 401
    except Exception as e:
        return jsonify({"message": str(e)}), 500

def get_reset_token(email):

    try:
        user = User.query.filter_by(email=email).first()

        if not user:
            return None

        return generate_token(user)

    except Exception as e:
        print(str(e))
        return None

def edit_user(current_user):
    data = request.get_json()
    try:
        user = User.query.filter_by(email=current_user.email).first()

        if not user:
            return jsonify({"message": "User not found"}), 404

        user.name = data.get("name") or user.name
        db.session.commit()

        return jsonify({"message": "user successfully updated", "data":user.to_json()}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

def change_password(current_user):
    password = request.form.get("password")

    if not password:
        return jsonify({"message": "No data provided"}), 400

    is_valid_password, password_msg = validate_password(password)
    if not is_valid_password:
        return jsonify({"message": password_msg}), 400

    try:
        current_user.password = generate_password_hash(password)
        db.session.commit()

        return jsonify({"message": "Password changed"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def forgot_password():
    data = request.get_json()
    email = data.get("email")
    if not email:
        return jsonify({"message": "No email provided"}), 400

    token = get_reset_token(email)
    if not token:
        return jsonify({"message": "There is no account with this email address"}), 400

    reset_url = f"{request.host_url}reset-password?token={token}"
    html_body = get_reset_password_email_html(reset_url)

    success, error = send_email(email, "Recupera tu contraseña - PetPlanner", html_body)
    if success:
        return jsonify({"message": "Email sent"}), 200
    else:
        return jsonify({"message": f"Failed to send email: {error}"}), 500

def send_email(to_email, subject, html_body):
    from_email = os.getenv("EMAIL_USER")
    app_password = os.getenv("EMAIL_PASSWORD")

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    msg.set_content("Este correo contiene un enlace para restablecer tu contraseña.")
    msg.add_alternative(html_body, subtype='html')

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(from_email, app_password)
            smtp.send_message(msg)
            return True, None
    except Exception as e:
        return False, str(e)

def assign_role_to_user(current_user, user_id):
    data = request.get_json()
    new_role_str = data.get("new_role")

    try:
        user_role = Role(current_user.role)
    except ValueError:
        return jsonify({"message": "Invalid current user role"}), 400

    if user_role != Role.ADMIN:
        return jsonify({"message": "You are not allowed to do this"}), 403

    if not new_role_str:
        return jsonify({"message": "No role provided"}), 400

    try:
        new_role = Role(new_role_str)
    except ValueError:
        return jsonify({"message": f"Invalid role '{new_role_str}'"}), 400

    user = User.query.filter_by(id=user_id).first()
    user.role = new_role.value
    db.session.commit()

    return jsonify({"message": f"Role updated to {new_role.value}", "data": user.to_json()}), 200



def get_reset_password_email_html(reset_url: str) -> str:
    html = f"""\
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Restablece tu contraseña - PetPlanner</title>
    </head>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; color: #333;">
        <table width="100%" style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 20px; border-radius: 8px;">
            <tr>
                <td style="text-align: center;">
                    <h2 style="color: #4CAF50;">PetPlanner</h2>
                    <p>Hola,</p>
                    <p>Recibimos una solicitud para restablecer tu contraseña.</p>
                    <p>Haz clic en el siguiente botón para continuar:</p>

                    <p style="margin: 20px 0;">
                        <a href="{reset_url}" style="padding: 12px 24px; background-color: #4CAF50; color: #ffffff; text-decoration: none; border-radius: 5px;">
                            Restablecer contraseña
                        </a>
                    </p>

                    <p>Este enlace expirará en 24 horas por razones de seguridad.</p>
                    <p>Si el botón no funciona, copia y pega el siguiente enlace en tu navegador:</p>
                    <p><a href="{reset_url}">{reset_url}</a></p>

                    <p style="margin-top: 30px;">Si no solicitaste recuperar tu cuenta en PetPlanner, puedes ignorar este correo.</p>                    
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    return html
