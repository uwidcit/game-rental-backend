from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_jwt import jwt_required

from App.controllers import (
    create_game, 
    get_all_games_json,
    fetch_api_games,
    get_game
)

game_views = Blueprint('game_views', __name__, template_folder='../templates')

@game_views.route('/games', methods=['GET'])
def get_games_action():
    return jsonify(get_all_games_json())

@game_views.route('/games/<rawgId>', methods=['GET'])
def get_game_action(rawgId):
    game  = get_game(rawgId)
    if game:
        return jsonify(game.toJSON())
    return jsonify({"message": f'Game with id {rawgId} not found'}), 404
