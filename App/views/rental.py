from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity

from App.controllers import (
    get_rentals_json,
    get_available_listing,
    create_rental_payment,
    get_customer,
    get_rental,
    get_staff,
    is_staff
)

rental_views = Blueprint('rental_views', __name__, template_folder='../templates')

@rental_views.route('/rentals', methods=['GET'])
@jwt_required()
def get_rentals_action():
    if is_staff(get_jwt_identity()):
        return jsonify(get_rentals_json())
    return jsonify({"error": "User not authorized to perform this action"}), 403

@rental_views.route('/rentals', methods=["POST"])
@jwt_required()
def rent_game_action():
    staff = get_staff(get_jwt_identity())
    if staff:
        renter = get_customer(request.json['renter'])
        listing = get_available_listing(request.json['listingId'])
        if renter and listing:
            rental = staff.confirm_rental(renter, listing)
            if rental:
                return jsonify({"message": f"rental created with id {rental.rentalId}, ${rental.listing.price} paid by user {renter.username}"}), 201
        return jsonify({"error": "rental not created bad renter/listing id"}), 404
    return jsonify({"error": "User not authorized to perform this action"}), 403


@rental_views.route('/rentals/<rentalId>', methods=["PUT"])
@jwt_required()
def return_rental_action(rentalId):
    staff = get_staff(get_jwt_identity())
    if staff:
        rental = get_rental(rentalId)
        if rental:
            payment = staff.confirm_return(rental)
            if payment != None:
                if payment > 0:
                    return jsonify({"message": f"rental returned payment of ${payment} created"})
                else:
                    return jsonify({"message": f"rental returned with no late fees"})
            return jsonify({"error": "rental not returned"})
        return jsonify({"error": f"Rental id {rentalId} not found"}), 404
    return jsonify({"error": "User not authorized to perform this action"}), 403