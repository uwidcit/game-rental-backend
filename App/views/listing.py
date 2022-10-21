from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_jwt import jwt_required, current_identity

from App.controllers import (
    get_avaiable_listings_json,
    list_game,
    is_staff,
    get_staff,
    get_game,
    get_customer,
    get_listing
)

listing_views = Blueprint('listing_views', __name__, template_folder='../templates')

@listing_views.route('/listings', methods=['GET'])
def get_listings_action():
    platform = request.args.get('platform')
    listings = get_avaiable_listings_json(platform)
    return jsonify(listings)

@listing_views.route('/listings', methods=['POST'])
@jwt_required()
def create_listing_action():
    data = request.json
    staff = get_staff(current_identity.id)
    game = get_game(data["gameId"])
    owner = get_customer(data['owner'])
    if staff and owner and game:
        listing = staff.list_game(owner, game, data['condition'], data['price'])
        print(staff, owner, game, listing)
        if listing:
            return jsonify({"message": f"listing created with id: {listing.listingId} by user: {listing.ownerId }"})
        return jsonify({"error": "listing not created bad id"}), 400
    return jsonify({"error": "User not authorized to perform this action"}), 403

@listing_views.route('/listings/<listingId>', methods=['PUT'])
@jwt_required()
def delist_action(listingId):
    staff = get_staff(current_identity.id)
    if staff:
        listing = get_listing(listingId)
        if listing:
            staff.delist_game(listing)
            return jsonify({"message": f"listing - {listing.listingId} delisted"})
        return jsonify({"error": "listing not created bad id"}), 400
    return jsonify({"error": "User not authorized to perform this action"}), 403