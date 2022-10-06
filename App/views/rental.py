from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_jwt import jwt_required, current_identity

from App.controllers import (
    create_rental,
    return_rental,
    get_rentals_json
)

rental_views = Blueprint('rental_views', __name__, template_folder='../templates')

@rental_views.route('/rentals', methods=['GET'])
def get_rentals_action():
    return jsonify(get_rentals_json())

@rental_views.route('/rentals', methods=["POST"])
@jwt_required()
def rent_game_action():
    res = create_rental(current_identity.id, request.json['listingId'])
    if res:
        return jsonify({"message": f"rental created with id {res.rentalId}"})
    return jsonify({"error": "rental not created"})

@rental_views.route('/rentals/<rentalId>', methods=["PUT"])
@jwt_required()
def renturn_rental_action(rentalId):
    data = request.json
    res = return_rental(rentalId)
    if res:
        return jsonify({"message": f"rental returned payment of ${res} created"})
    return jsonify({"error": "rental not returned"})