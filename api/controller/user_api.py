from flask import jsonify, request, abort, current_app, Blueprint

from api.service.giphy_service import GiphyService
from api.repository.users_repository import UsersRepository

user_api = Blueprint('user_api', __name__)


@user_api.route('/search', methods=['GET'])
def search_users():
    name = request.args.get('name', default=None)
    username = request.args.get('username', default=None)

    if all(a is None for a in [name, username]):
        abort(400)

    try:
        users_repository = UsersRepository(current_app.config.db_cache['DB'])

        users = []
        if name is not None:
            users = users_repository.search_user_by_name(name)
        if username is not None:
            users.extend(users_repository.search_user_by_username(username))
            result = []
            [result.append(x) for x in users if x not in result]
            users = result

        if users is not None:
            response = jsonify({'users': users})
            response.status_code = 200
            return response
        else:
            response = jsonify({'meta': {'error_code': 404, 'msg': 'user not found'}})
            response.status_code = 404
            return response

    except ValueError as e:
        response = jsonify({'meta': {'error_code': 503, 'msg': str(e)}})
        response.status_code = 503
        return response


@user_api.route('/<int:user_id>/avatar', methods=['PUT'])
def update_user_avatar(user_id):
    body = request.get_json()
    avatar_id = body.get('avatar_id', None)
    if avatar_id is None:
        abort(400)

    try:
        # Fetch user from the DB to check that exists
        users_repository = UsersRepository(current_app.config.db_cache['DB'])
        user = users_repository.search_user_by_id(user_id)
        if user is None:
            abort(404)

        # Fetch gif from the Giphy API to check that exists
        giphy_service = GiphyService(current_app.config.giphy_api)
        gif = giphy_service.search_gif_by_id(avatar_id)
        if gif is None:
            """Returning 410 because the gif ID is not longer available in the Giphy API
            so we should not request for this gif ID again"""
            response = jsonify({'meta': {'error_code': 410, 'msg': 'avatar could not be found'}})
            response.status_code = 410
            return response

        # Update user avatar in the DB
        user = users_repository.update_user_avatar(user_id, gif['id'], gif['url'])
        response = jsonify({'user': user})
        response.status_code = 200
        return response

    except ValueError as e:
        response = jsonify({'meta': {'error_code': 503, 'msg': str(e)}})
        response.status_code = 503
        return response
