from flask import Blueprint

from app.utils.auth import token_required
from app.controllers.pet_controller import get_pet, get_pets, delete_pet, update_pet, create_pet
pets = Blueprint('pets', __name__)

@pets.route("/pet", methods=['POST'])
@token_required
def create_pet_route(current_user):
    return create_pet(current_user)

@pets.route("/pets", methods=['GET'])
@token_required
def get_pets_route(current_user):
    return get_pets(current_user)

@pets.route("/pet/<int:pet_id>", methods=['GET'])
@token_required
def get_pet_route(current_user, pet_id):
    return get_pet(current_user, pet_id)

@pets.route("/pet/<int:pet_id>", methods=['PUT'])
@token_required
def edit_pet_route(current_user, pet_id):
    return update_pet(current_user, pet_id)

@pets.route("/pet/<int:pet_id>", methods=['DELETE'])
@token_required
def delete_pet_route(current_user, pet_id):
    return delete_pet(current_user, pet_id)