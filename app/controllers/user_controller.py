from flask import request, jsonify

from app.utils.auth import generate_token
from app.utils.validators import validate_email, validate_password
from app.models.petplanner import User, db
from werkzeug.security import generate_password_hash, check_password_hash

DEFAULT_ROLE = "GUEST"

def create_user():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")
    role = DEFAULT_ROLE


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

def edit_user(current_user):
    data = request.get_json()
    try:
        user = User.query.filter_by(email=current_user.email).first()

        if not user:
            return jsonify({"message": "User not found"}), 404

        user.name = data.get("name") or user.name
        # user.role = data.get("role") or user.role
        db.session.commit()

        return jsonify({"message": "user successfully updated", "data":user.to_json()}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

def change_password(current_user):
    data = request.get_json()
    password = data.get("password")

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
    "TODO"
