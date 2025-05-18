from flask import request, jsonify
from app.models.petplanner import db, Allergy

ALLOWED_ROLES = ["ADMIN", "GUEST"]

def create_allergy(current_user):

    if current_user.role not in ALLOWED_ROLES:
        return jsonify({"message": "Unauthorized"}), 403

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
    if current_user.role not in ALLOWED_ROLES:
        return jsonify({"message": "Unauthorized"}), 403

    try:
        allergies = Allergy.query.all()
        return jsonify({"message": "Successfully retrieved allergies","data": [allergy.to_json() for allergy in allergies]}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

def edit_allergy(current_user, id_allergy):

    if current_user.role not in ALLOWED_ROLES:
        return jsonify({"message": "Unauthorized"}), 403
    data = request.get_json()
    try:
        allergy = Allergy.query.filter_by(id=id_allergy).first()

        if not allergy:
            return jsonify({"message": "Allergy not found"}), 404

        allergy.name = data.get("name") or allergy.name
        db.session.commit()

        return jsonify({"message": "Successfully edited allergy", "data": allergy.to_json()}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500

def delete_allergy(current_user, id_allergy):

    if current_user.role not in ALLOWED_ROLES:
        return jsonify({"message": "Unauthorized"}), 403

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