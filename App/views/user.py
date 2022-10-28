from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_jwt import jwt_required, current_identity


from App.controllers import (
    create_customer,
    create_staff, 
    get_all_users,
    get_all_users_json,
    is_staff
)

user_views = Blueprint('user_views', __name__, template_folder='../templates')


@user_views.route('/users', methods=['GET'])
@jwt_required()
def client_app():
    if is_staff(current_identity.id):
        users = get_all_users_json()
        return jsonify(users)
    return jsonify({"error": "User not authorized to perform this action"}), 403

@user_views.route('/customer', methods=['POST'])
def create_customer_action():
    data = request.json
    result = create_customer(username=data['username'], password=data['password'])
    if result:
        return jsonify({"message": f"Customer created with id {result.id}"}), 201
    return jsonify({"error": f"Username {data['username']} already exists "}), 500

@user_views.route('/staff', methods=['POST'])
def create_staff_action():
    data = request.json
    result = create_staff(username=data['username'], password=data['password'])
    if result:
        return jsonify({"message": f"Staff created with id {result.id}"}), 201
    return jsonify({"error": f"Username {data['username']} already exists "}), 500

@user_views.route('/identify', methods=['GET'])
@jwt_required()
def identify_user_action():
    return jsonify({'message': f"username: {current_identity.username}, id : {current_identity.id}, type: {current_identity.user_type}"})