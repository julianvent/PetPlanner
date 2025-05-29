from flask import Blueprint

from app.controllers.allergy_controller import get_allergy, edit_allergy, create_allergy, delete_allergy
from app.utils.auth import token_required

allergy = Blueprint('allergy', __name__)


@allergy.route('/', methods=['GET'])
@token_required
def get_allergy_route(current_user):
    return get_allergy(current_user)

@allergy.route('/', methods=['POST'])
@token_required
def create_allergy_route(current_user):
    return create_allergy(current_user)

@allergy.route('/<int:id_allergy>', methods=['PUT'])
@token_required
def edit_allergy_route(current_user, id_allergy):
    return edit_allergy(current_user, id_allergy)

@allergy.route('/<int:id_allergy>', methods=['DELETE'])
@token_required
def delete_allergy_route(current_user, id_allergy):
    return delete_allergy(current_user, id_allergy) 