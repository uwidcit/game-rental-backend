from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_jwt import jwt_required, current_identity

from App.controllers import (
    create_rental,
    return_rental,
    get_rentals_json,
    get_available_listing,
    create_rental_payment,
    get_user
)

rental_views = Blueprint('rental_views', __name__, template_folder='../templates')

@rental_views.route('/rentals', methods=['GET'])
def get_rentals_action():
    return jsonify(get_rentals_json())

@rental_views.route('/rentals', methods=["POST"])
@jwt_required()
def rent_game_action():
    renter = get_user(request.json['renter'])
    listing = get_available_listing(request.json['listingId'])
    if renter and listing:
        rental = create_rental(renter.id, listing.listingId)
        payment = create_rental_payment(rental.rentalId, renter.id, rental.listing.price)
        if rental and payment:
            return jsonify({"message": f"rental created with id {rental.rentalId}, ${rental.listing.price} paid by user {renter.username}"}), 201
    return jsonify({"error": "rental not created"}), 400

@rental_views.route('/rentals/<rentalId>', methods=["PUT"])
@jwt_required()
def renturn_rental_action(rentalId):
    fees = return_rental(rentalId)
    if fees:
        if fees > 0:
            return jsonify({"message": f"rental returned payment of ${res} created"})
        else:
            return jsonify({"message": f"rental returned with no late fees"})
    return jsonify({"error": "rental not returned"})