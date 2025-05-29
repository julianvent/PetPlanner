from flask import Blueprint

from app.controllers.allergy_controller import assign_allergy_to_pet, get_pet_allergies, remove_allergy_from_pet
from app.utils.auth import token_required
from app.controllers.pet_controller import get_pet, get_pets, delete_pet, update_pet, create_pet
pets = Blueprint('pets', __name__)

@pets.route("/", methods=['POST'])
@token_required
def create_pet_route(current_user):
    return create_pet(current_user)

@pets.route("/", methods=['GET'])
@token_required
def get_pets_route(current_user):
    return get_pets(current_user)

@pets.route("/<int:pet_id>", methods=['GET'])
@token_required
def get_pet_route(current_user, pet_id):
    return get_pet(current_user, pet_id)

@pets.route("/<int:pet_id>", methods=['PUT'])
@token_required
def edit_pet_route(current_user, pet_id):
    return update_pet(current_user, pet_id)

@pets.route("/<int:pet_id>", methods=['DELETE'])
@token_required
def delete_pet_route(current_user, pet_id):
    return delete_pet(current_user, pet_id)

@pets.route("/allergy/<int:pet_id>/<int:allergy_id>", methods=['POST'])
@token_required
def assign_allergy_to_pet_route(current_user, pet_id, allergy_id):
    return assign_allergy_to_pet(current_user, pet_id, allergy_id)

@pets.route("/allergy/<int:pet_id>", methods=['GET'])
@token_required
def get_pet_allergies_route(current_user, pet_id):
    return get_pet_allergies(current_user, pet_id)

@pets.route("/allergy/<int:pet_id>/<int:allergy_id>", methods=['DELETE'])
@token_required
def remove_allergy_from_pet_route(current_user, pet_id, allergy_id):
    return remove_allergy_from_pet(current_user, pet_id, allergy_id)
