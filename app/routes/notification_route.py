from flask import Blueprint
from app.controllers.notification_controller import get_notifications
from app.utils.auth import token_required

notification = Blueprint('notification', __name__)

@notification.route('/', methods=['GET'])
@token_required
def get_notifications_route(current_user):
    return get_notifications(current_user)