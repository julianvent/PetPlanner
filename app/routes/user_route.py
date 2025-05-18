from flask import Blueprint, jsonify

from app.controllers.user_controller import create_user, get_token, change_password, edit_user
from app.utils.auth import token_required
users = Blueprint('users', __name__)

@users.route('/register', methods=['POST'])
def register():
    return create_user()

@users.route('/login', methods=['POST'])
def login():
    return get_token()

@users.route('/forgot-password', methods=['POST'])
def forgot_password():
    pass

@users.route('/reset-password', methods=['POST'])
@token_required
def reset_password(current_user):
    return change_password(current_user)

@users.route('/me', methods=['GET'])
@token_required
def me(current_user):
    return jsonify(current_user.to_json())

@users.route('/me', methods=['PUT'])
@token_required
def update_profile(current_user):
    return edit_user(current_user)

@users.route('/users/<int:user_id>/role', methods=['PUT'])
@token_required
def change_role(current_user):
    pass

