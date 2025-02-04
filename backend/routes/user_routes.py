from .common_imports import *
from models.user import User

# Routes for Users
@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_data = [{"id": user.id, "username": user.username, "email": user.email, "role": user.role} for user in users]
    return jsonify(users_data), 200

@user_bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if user:
        return jsonify({"id": user.id, "username": user.username, "email": user.email, "role": user.role}), 200
    return jsonify({"message": "User not found"}), 404