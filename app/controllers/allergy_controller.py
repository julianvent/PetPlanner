from flask import request, jsonify
from sqlalchemy.exc import NoResultFound

from app.models.petplanner import db, Allergy, Pet, PetAllergy, User
from app.utils.user_role import get_role_from_user
from app.models.role import Role

def create_allergy(current_user):
    try:
        role = get_role_from_user(current_user)
        if Role(role) != Role.ADMIN:
            return jsonify({"message": "Unauthorized"}), 403
    except NoResultFound:
        return jsonify({"message": "No such user"}), 403

    data = request.get_json()
    name_allergy = data.get('name_allergy')

    if not name_allergy:
        return jsonify({"message": "No data provided"}), 400
    try:
        existing_allergy = Allergy.query.filter_by(name=name_allergy).first()
        if existing_allergy:
            return jsonify({"message": "Already exists"}), 400

        new_allergy = Allergy(name=name_allergy)

        db.session.add(new_allergy)
        db.session.commit()

        return jsonify({"message": "Successfully created allergy", "data": new_allergy.to_json()}), 201

    except Exception as e:
        return jsonify({"message": str(e)}), 500

def get_allergy(current_user):

    try:
        allergies = Allergy.query.all()
        return jsonify({"message": "Successfully retrieved allergies","data": [allergy.to_json() for allergy in allergies]}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

def edit_allergy(current_user, id_allergy):
    try:
        role = get_role_from_user(current_user)
        if Role(role) != Role.ADMIN:
            return jsonify({"message": "Unauthorized"}), 403
    except NoResultFound:
        return jsonify({"message": "No such user"}), 403
    data = request.get_json()
    try:
        allergy = Allergy.query.filter_by(id=id_allergy).first()

        if not allergy:
            return jsonify({"message": "Allergy not found"}), 404

        existing_allergy = Allergy.query.filter_by(name=data['name_allergy']).first()
        if existing_allergy:
            return jsonify({"message": "Already exists"}), 400

        allergy.name = data.get("name_allergy") or allergy.name
        db.session.commit()

        return jsonify({"message": "Successfully edited allergy", "data": allergy.to_json()}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500

def delete_allergy(current_user, id_allergy):
    try:
        role = get_role_from_user(current_user)
        if Role(role) != Role.ADMIN:
            return jsonify({"message": "Unauthorized"}), 403
    except NoResultFound:
        return jsonify({"message": "No such user"}), 403

    if not id_allergy:
        return jsonify({"message": "No data provided"}), 400

    try:
        allergy = Allergy.query.filter_by(id=id_allergy).first()

        if not allergy:
            return jsonify({"message": "Allergy not found"}), 404

        db.session.delete(allergy)
        db.session.commit()

        return jsonify({"message": "Successfully deleted allergy"}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500

def assign_allergy_to_pet(current_user, id_pet, id_allergy):

    if not id_allergy or not id_pet:
        return jsonify({"message": "No data provided"}), 400

    try:
        pet = Pet.query.filter_by(id=id_pet).first()
        if not pet:
            return jsonify({"message": "Pet not found"}), 404

        if pet.user_id != current_user.id:
            return jsonify({"message": "Not allowed"}), 403

        new_pet_allergy = PetAllergy(allergy_id=id_allergy, pet_id=pet.id)

        db.session.add(new_pet_allergy)
        db.session.commit()
        return jsonify({"message": "Successfully created allergy for pet", "data": new_pet_allergy.to_json()}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500

def get_pet_allergies(current_user, id_pet):
    if not id_pet:
        return jsonify({"message": "No data provided"}), 400
    try:
        pet = Pet.query.filter_by(id=id_pet).first()
        if not pet:
            return jsonify({"message": "Pet not found"}), 404

        if pet.user_id != current_user.id:
            return jsonify({"message": "Not allowed"}), 403

        allergies = Allergy.query.join(PetAllergy).filter(PetAllergy.pet_id == pet.id).all()

        return jsonify({"message": "Successfully retrieved allergies for pet", "data": [allergy.to_json() for allergy in allergies]}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500

def remove_allergy_from_pet(current_user, id_allergy, id_pet):
    if not id_allergy or not id_pet:
        return jsonify({"message": "No data provided"}), 400

    try:
        pet = Pet.query.filter_by(id=id_pet).first()

        if not pet:
            return jsonify({"message": "Pet not found"}), 404

        if pet.user_id != current_user.id:
            return jsonify({"message": "Not allowed"}), 403

        allergy = PetAllergy.query.filter_by(pet_id=pet.id, allergy_id=id_allergy).first()
        if not allergy:
            return jsonify({"message": "Allergy not found"}), 404

        db.session.delete(allergy)
        db.session.commit()

        return jsonify({"message":"Successfully deleted allergy for pet"}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500