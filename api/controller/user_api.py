from flask import jsonify, request, abort, current_app, Blueprint

from api.service.user_service import UserService
from api.errors.giphy_exception import GiphyException

user_api = Blueprint('user_api', __name__)

@user_api.route('/', methods=['POST'])
def create_user():
    body = request.get_json()
    name = body.get('name', None)
    username = body.get('username', None)
    avatar_id = body.get('avatar_id', None)

    if name is None or username is None or avatar_id is None:
        abort(400)

    try:
        user_service = UserService(current_app.config)
        user = user_service.create_user(name, username, avatar_id)

        response = jsonify({'data': {'user': user}})
        response.status_code = 200
        return response
    
    except GiphyException as e:
        response = jsonify({'error': {'error_code': e.error_code, 'msg': str(e)}})
        response.status_code = 503
        return response
    
    except ValueError as e:
        response = jsonify({'error': {'error_code': 503, 'msg': str(e)}})
        response.status_code = 503
        return response

@user_api.route('/search', methods=['GET'])
def search_users():
    name = request.args.get('name', default=None)
    username = request.args.get('username', default=None)

    if all(a is None for a in [name, username]):
        abort(400)

    try:
        user_service = UserService(current_app.config)

        users = user_service.search_user(name, username)

        if users is not None:
            response = jsonify({'data': {'users': users}})
            response.status_code = 200
            return response
        else:
            response = jsonify({'error': {'error_code': 404, 'msg': 'user not found'}})
            response.status_code = 404
            return response

    except ValueError as e:
        response = jsonify({'error': {'error_code': 503, 'msg': str(e)}})
        response.status_code = 503
        return response


@user_api.route('/<int:user_id>/avatar', methods=['PUT'])
def update_user_avatar(user_id):
    body = request.get_json()
    avatar_id = body.get('avatar_id', None)
    if avatar_id is None:
        abort(400)

    try:
        user_service = UserService(current_app.config)
        user = user_service.update_user_avatar(user_id, avatar_id)

        if user is None:
            response = jsonify({'error': {'error_code': 404, 'msg': 'user not found'}})
            response.status_code = 404
            return response
        
        response = jsonify({'data': {'user': user}})
        response.status_code = 200
        return response
    
    except GiphyException as e:
        response = jsonify({'error': {'error_code': e.error_code, 'msg': str(e)}})
        response.status_code = 503
        return response

    except ValueError as e:
        response = jsonify({'error': {'error_code': 503, 'msg': str(e)}})
        response.status_code = 503
        return response
