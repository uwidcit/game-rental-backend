from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_jwt import jwt_required

from App.controllers import (
    create_game, 
    get_all_games_json
)

game_views = Blueprint('game_views', __name__, template_folder='../templates')

@game_views.route('/api/games')
def get_games_action():
    games = get_all_games_json()
    return jsonify(games)