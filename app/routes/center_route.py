from flask import Blueprint
from app.controllers.center_controller import get_center, get_my_centers, get_all_centers, create_center, delete_center, update_center
from app.utils.auth import token_required

center = Blueprint('center', __name__)


@center.route("/", methods=['GET'])
def get_centers_route():
    return get_all_centers()


@center.route("/me", methods=['GET'])
@token_required
def get_my_centers_route(current_user):
    return get_my_centers(current_user)

@center.route("/<int:center_id>", methods=['GET'])
@token_required
def get_center_route(current_user, center_id):
    return get_center(center_id)

@center.route("/", methods=['POST'])
@token_required
def create_center_route(current_user):
    return create_center(current_user)

@center.route("/<int:center_id>", methods=['PUT'])
@token_required
def update_center_route(current_user, center_id):
    return update_center(current_user, center_id)

@center.route("/<int:center_id>", methods=['DELETE'])
@token_required
def delete_center_route(current_user, center_id):
    return delete_center(current_user, center_id)

