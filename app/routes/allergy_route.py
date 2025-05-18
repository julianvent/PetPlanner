from flask import Blueprint
from app.controllers.allergy_controller import create_allergy, edit_allergy, delete_allergy, get_allergy
from app.utils.auth import token_required

allergy = Blueprint('allergy', __name__)

@allergy.route('/allergies', methods=['GET'])
@token_required
def get_all_allergies(current_user):
    return get_allergy(current_user)

#@allergy.route('/allergy/<int:allergy_id>', methods=['GET'])

@allergy.route('/allergies', methods=['POST'])
@token_required
def create_allergy_route(current_user):
    return create_allergy(current_user)

@allergy.route('/allergies/<int:id_allergy>', methods=['PUT'])
@token_required
def edit_allergy_route(current_user, id_allergy):
    return edit_allergy(current_user, id_allergy)

@allergy.route('/allergies/<int:id_allergy>', methods=['DELETE'])
@token_required
def delete_allergy_route(current_user, id_allergy):
    return delete_allergy(current_user, id_allergy)