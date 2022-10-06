from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_jwt import jwt_required

from App.controllers import (
  create_rental_payment
)

payment_views = Blueprint('payment_views', __name__, template_folder='../templates')

@payment_views.route('/payments', methods=['POST'])
def create_payment_action():
    platform = request.args.get('platform')
    listings = get_avaiable_listings_json(platform)
    return jsonify(listings)