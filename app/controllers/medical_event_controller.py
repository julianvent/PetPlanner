from flask import request, jsonify
from datetime import datetime

from app.models.petplanner import db, MedicalEvent, Pet


def create_medical_event(current_user, pet_id):
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    date = data.get('date')
    is_completed = data.get('is_completed')
    recurrence = data.get('recurrence') # 0,1

    if not pet_id or not title or not description or not date or recurrence is None or is_completed is None:
        return jsonify({"message": "No data provided"}), 400

    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return jsonify({"message": "Invalid date format. Expected YYYY-MM-DD."}), 400

    try:
        pet = Pet.query.filter_by(id=pet_id).first()

        if not pet:
            return jsonify({"message": "Pet not found"}), 404

        if current_user.id != pet.user_id:
            return jsonify({"message": "This pet does not belong to you"}), 403

        new_medical_event = MedicalEvent(
            pet_id=pet_id,
            title=title,
            description=description,
            date=date,
            is_completed=is_completed,
            recurrence=recurrence,
        )
        db.session.add(new_medical_event)
        db.session.commit()

        return jsonify({"message": "Medical event created", "data": new_medical_event.to_json()}), 201

    except Exception as e:
        return jsonify({"message": str(e)}), 500

def get_medical_events(current_user, pet_id):

    if not pet_id:
        return jsonify({"message": "No data provided"}), 400

    try:
        pet = Pet.query.filter_by(id=pet_id).first()

        if not pet:
            return jsonify({"message": "Pet not found"}), 404

        if current_user.id != pet.user_id:
            return jsonify({"message": "This pet does not belong to you"}), 403

        medical_events = MedicalEvent.query.filter_by(pet_id=pet_id).all()
        return jsonify({"message": "Successfully retrieved medical events", "data": [medical_event.to_json() for medical_event in medical_events]}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500

def update_medical_event(current_user, medical_event_id):

    data = request.get_json()
    if not medical_event_id:
        return jsonify({"message": "No data provided"}), 400

    try:
        medical_event = MedicalEvent.query.filter_by(id=medical_event_id).first()

        if not medical_event:
            return jsonify({"message": "Medical event not found"}), 404

        pet = Pet.query.filter_by(id=medical_event.pet_id).first()

        if not pet:
            return jsonify({"message": "Pet not found"}), 404

        if current_user.id != pet.user_id:
            return jsonify({"message": "This pet does not belong to you"}), 403

        medical_event.title = data.get('title') or medical_event.title
        medical_event.description = data.get('description') or medical_event.description
        medical_event.recurrence = data.get('recurrence')

        if 'is_completed' in data:
            medical_event.is_completed = data.get('is_completed')

        date_str = data.get('date')
        if date_str:
            try:
                medical_event.date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except (ValueError, TypeError):
                return jsonify({"message": "Invalid date format. Expected YYYY-MM-DD."}), 400

        db.session.commit()

        return jsonify({"message":"Successfully updated medical event", "data": medical_event.to_json()}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500

def delete_medical_event(current_user, medical_event_id):

    if not medical_event_id:
        return jsonify({"message": "No data provided"}), 400

    try:
        medical_event = MedicalEvent.query.filter_by(id=medical_event_id).first()

        if not medical_event:
            return jsonify({"message": "Medical event not found"}), 404

        pet = Pet.query.filter_by(id=medical_event.pet_id).first()
        if not pet:
            return jsonify({"message": "Pet not found"}), 404

        if current_user.id != pet.user_id:
            return jsonify({"message": "This pet does not belong to you"}), 403

        db.session.delete(medical_event)
        db.session.commit()
        return jsonify({"message": "Medical event successfully deleted"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

