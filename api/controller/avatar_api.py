from flask import Blueprint, jsonify, current_app

from api.service.giphy_service import GiphyService

avatar_api = Blueprint('avatar_api', __name__)


@avatar_api.route('/', methods=['GET'])
def get_avatars():
    try:
        giphy_service = GiphyService(current_app.config.giphy_api)
        gif_list = giphy_service.get_trending_gifs()

        response = jsonify({'data': {'avatars': gif_list}})
        response.status_code = 200
        return response

    except ValueError as e:
        response = jsonify({'error': {'error_code': 503, 'msg': str(e)}})
        response.status_code = 503
        return response
