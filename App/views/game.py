from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_jwt import jwt_required

from App.controllers import (
    create_game, 
    get_all_games_json,
    fetch_api_games
)

game_views = Blueprint('game_views', __name__, template_folder='../templates')

@game_views.route('/games', methods=['GET'])
def get_games_action():
    return fetch_api_games()


@game_views.route('/games', methods=['POST'])
@jwt_required()
def create_game_action():
    data = request.json
    game = create_game(data['title'], data['rating'], data['platform'], data['boxart'], data['genre'])
    return jsonify({'message':f'Game {game.gameId} - {game.title} created'})