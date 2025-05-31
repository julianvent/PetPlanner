from flask import request, jsonify

from app.models.petplanner import db, Center
from app.models.role import Role
from app.utils.user_role import get_role_from_user

def create_center(current_user):
    data = request.get_json()
    name = data.get('name')
    address = data.get('address')
    hours = data.get('hours')
    services = data.get('services')
    type = data.get('type')

    if not name or not address or not hours or not services or not type:
        return jsonify({"message": "No data provided"}), 400

    role = get_role_from_user(current_user)

    if Role(role) != Role.CENTER:
        return jsonify({"message": "You are not authorized to perform this action"}), 403

    try:
        new_center = Center(user_id=current_user.id, name=name, address=address, hours=hours, services=services, type=type)

        db.session.add(new_center)
        db.session.commit()

        return jsonify({"message": "Center created successfully", "data": new_center.to_json()}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 400

def  get_all_centers():
    try:
        centers = db.session.query(Center).all()
        return jsonify({"message": "List of all centers", "data": [center.to_json() for center in centers]}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400

def get_my_centers(current_user):

    try:
        centers = Center.query.filter_by(user_id=current_user.id).all()
        return jsonify({"message": "List of centers", "data": [center.to_json() for center in centers]}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400

def get_center(id_center):
    try:

        center = Center.query.filter_by(id=id_center).first()
        if not center:
            return jsonify({"message": "Center not found"}), 404

        return jsonify({"message": "Center found successfully", "data": center.to_json()}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 400

def update_center(current_user, id_center):
    data = request.get_json()
    name = data.get('name')
    address = data.get('address')
    hours = data.get('hours')
    services = data.get('services')
    type = data.get('type')

    try:
        center = Center.query.filter_by(id=id_center).first()
        if not center:
            return jsonify({"message": "Center not found"}), 404

        if center.user_id != current_user.id:
            return jsonify({"message": "You are not authorized to perform this action"}), 401

        center.name = name or center.name
        center.address = address or center.address
        center.hours = hours or center.hours
        center.services = services or center.services
        center.type = type or center.type
        db.session.commit()
        return jsonify({"message": "Center updated successfully", "data": center.to_json()}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 400


def delete_center(current_user, id_center):

    try:
        center = Center.query.filter_by(id=id_center).first()
        if not center:
            return jsonify({"message": "Center not found"}), 404

        if center.user_id != current_user.id:
            return jsonify({"message": "You are not authorized to perform this action"}), 401

        db.session.delete(center)
        db.session.commit()
        return jsonify({"message": "Center deleted successfully"}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 400
