from flask import request, jsonify
from app.models.petplanner import db, Notification, Pet, MedicalEvent


def create_notification(current_user, event_id):
    try:
        medical_event = MedicalEvent.query.filter_by(id=event_id).first()

        if not medical_event:
            return jsonify({"message": "Pet not found"}), 404

        new_notification = Notification(
            event_id=medical_event.id,
            scheduled_at=medical_event.date + medical_event.recurrence,
            sent= False
        )

        db.session.add(new_notification)
        db.session.commit()

        return jsonify({"message": "Notification created", "data": new_notification.to_json()}), 201

    except Exception as e:
        return jsonify({"message": str(e)}), 500


def get_notifications(current_user):
    try:
        notifications = Notification.query \
            .join(MedicalEvent) \
            .join(Pet) \
            .filter(Pet.user_id == current_user.id) \
            .all()

        return jsonify({"message": "Successfully retrieved notifications", "notifications": [notification.to_json() for notification in notifications]}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500