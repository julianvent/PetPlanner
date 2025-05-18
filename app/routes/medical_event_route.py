from flask import Blueprint
from app.controllers.medical_event_controller import get_medical_events, create_medical_event, delete_medical_event, update_medical_event
from app.utils.auth import token_required

medical_event = Blueprint('medical_event', __name__)

@medical_event.route('/<int:pet_id>/events', methods=['POST'])
@token_required
def create_medical_event_route(current_user, pet_id):
    return create_medical_event(current_user, pet_id)

@medical_event.route('/<int:pet_id>/events', methods=['GET'])
@token_required
def get_medical_events_route(current_user, pet_id):
    return get_medical_events(current_user, pet_id)

@medical_event.route('/<int:event_id>/events', methods=['PUT'])
@token_required
def update_medical_event_route(current_user, event_id):
    return update_medical_event(current_user, event_id)

@medical_event.route('/<int:event_id>', methods=['DELETE'])
@token_required
def delete_medical_event_route(current_user, event_id):
    return delete_medical_event(current_user, event_id)