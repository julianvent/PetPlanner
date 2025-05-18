
from flask import request, jsonify
from datetime import datetime
from app.models.petplanner import db, Pet

def create_pet(current_user):

    data = request.get_json()
    name = data.get("name")
    breed = data.get("breed")
    birth_date = data.get("birth_date")
    physical_characteristics = data.get("physical_characteristics")
    health_conditions = data.get("health_conditions")

    try:
        birth_date_obj = datetime.strptime(birth_date, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return jsonify({"message": "Invalid birth_date format. Expected YYYY-MM-DD."}), 400

    if not name or not breed or not birth_date or not physical_characteristics or not health_conditions:
        return jsonify({"message": "No data provided"}), 400

    try:
        new_pet = Pet(
            user_id = current_user.id,
            name=name,
            breed=breed,
            birth_date=birth_date,
            physical_characteristics=physical_characteristics,
            health_conditions=health_conditions
        )

        db.session.add(new_pet)
        db.session.commit()
        return jsonify({"message": "Pet created successfully", "data": new_pet.to_json()}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 400

def get_pets(current_user):

    try:
        pets = Pet.query.filter_by(user_id=current_user.id).all()
        return jsonify({"message": "Successfully retrieved pets", "data": [pet.to_json() for pet in pets]}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400

def get_pet(current_user, pet_id):
    try:
        pet = Pet.query.filter_by(user_id=current_user.id, id=pet_id).first()
        if not pet:
            return jsonify({"message": "Pet not found"}), 404

        return jsonify({"message": "Successfully retrieved pet", "data": pet.to_json()})
    except Exception as e:
        return jsonify({"message": str(e)}), 400

def update_pet(current_user, pet_id):
    data = request.get_json()
    try:
        pet = Pet.query.filter_by(user_id=current_user.id, id=pet_id).first()

        if not pet:
            return jsonify({"message": "Pet not found"}), 404

        pet.name = data.get("name") or pet.name
        pet.breed = data.get("breed") or pet.breed
        pet.birth_date = data.get("birth_date") or pet.birth_date
        pet.physical_characteristics = data.get("physical_characteristics") or pet.physical_characteristics
        pet.health_conditions = data.get("health_conditions") or pet.health_conditions

        db.session.commit()
        return jsonify({ "message": "Pet successfully updated", "data": pet.to_json()}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 400


def delete_pet(current_user, pet_id):

    try:
        pet = Pet.query.filter_by(user_id=current_user.id, id=pet_id).first()

        if not pet:
            return jsonify({"message": "Pet not found"}), 404

        db.session.delete(pet)
        db.session.commit()

        return jsonify({"message": "Pet successfully deleted"}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 400