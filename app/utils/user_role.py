from app.models.petplanner import db, User
from app.models.role import Role
def get_role_from_user(current_user):
    try:
        user = User.query.filter_by(id=current_user.id).first()
        if not user:
            return None
        return Role(user.role)
    except:
        return None