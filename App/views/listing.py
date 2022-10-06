from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_jwt import jwt_required, current_identity

from App.controllers import (
    get_avaiable_listings_json,
    list_game
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
    res = list_game(current_identity.id, data["gameId"], data['condition'], data['price'])
    if res:
        return jsonify({"message": "listing created"})
    return jsonify({"message": "listing not created"})