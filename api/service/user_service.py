from api.repository.users_repository import UsersRepository
from api.service.giphy_service import GiphyService
from api.errors.giphy_exception import GiphyException

class UserService:

    def __init__(self, config):
        self.config = config
        self.users_repository = UsersRepository(self.config.db_cache['DB'])

    def create_user(self, name, username, avatar_id):
        giphy_service = GiphyService(self.config.giphy_api)
        gif = giphy_service.search_gif_by_id(avatar_id)

        if gif is None:
            raise GiphyException('avatar could not be found', 410)
    
        user = self.users_repository.create_user(name, username, gif['id'], gif['url'])
        return user

    def search_user(self, name, username):
        users = []
        if name is not None:
            users = self.users_repository.search_user_by_name(name)
        if username is not None:
            users.extend(self.users_repository.search_user_by_username(username))
            result = []
            [result.append(x) for x in users if x not in result]
            users = result

        return users
    
    def update_user_avatar(self, user_id, avatar_id):
        user = self.users_repository.search_user_by_id(user_id)
        if user is None:
            return None
        
        giphy_service = GiphyService(self.config.giphy_api)
        gif = giphy_service.search_gif_by_id(avatar_id)

        if gif is None:
            raise GiphyException('avatar could not be found', 410)
        
        user = self.users_repository.update_user_avatar(user_id, gif['id'], gif['url'])

        return user


