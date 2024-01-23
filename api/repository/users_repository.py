class UsersRepository:
    """UsersRepository contains the users
    It's using a Cache as 'database' which is initialized in the app.py"""
    def __init__(self, cache):
        self.cache = cache
        self._init_cache()

    def search_user_by_id(self, user_id):
        results = [self.cache.get(key) for key in self.cache.cache._cache
                   if key == user_id]

        if results:
            return results[0]
        else:
            return None

    def search_user_by_name(self, name):
        return [self.cache.get(key) for key in self.cache.cache._cache
                   if name in self.cache.get(key)['name']]

    def search_user_by_username(self, username):
        return [self.cache.get(key) for key in self.cache.cache._cache
                   if username in self.cache.get(key)['username']]

    def update_user_avatar(self, user_id, avatar_id, avatar):
        user = self.cache.get(user_id)
        user['avatar_id'] = avatar_id
        user['avatar'] = avatar
        self.cache.set(user_id, user)
        return user

    def _init_cache(self):
        """We use the key 'loader' to initialize the Cache only once when we run the app"""
        if self.cache.get('loaded') is None:
            self._dump_users()
            self.cache.set('loaded', {'id': 0, 'name': 'Loaded', 'username': 'loaded',
                               'avatar_id': 'wzzJHfPD1Sgc2HoZ9x',
                               'avatar': 'https://giphy.com/embed/sZ5CxgSUsRclBTQeGc'})

    def _dump_users(self):
        self.cache.set(1, {'id': 1, 'name': 'Jose', 'username': 'joseahp',
                           'avatar_id': 'wzzJHfPD1Sgc2HoZ9x',
                           'avatar': 'https://giphy.com/embed/sZ5CxgSUsRclBTQeGc'})
        self.cache.set(2, {'id': 2, 'name': 'Irina', 'username': 'irinaid',
                           'avatar_id': 'wzzJHfPD1Sgc2HoZ9x',
                           'avatar': 'https://giphy.com/embed/sZ5CxgSUsRclBTQeGc'})
        self.cache.set(3, {'id': 3, 'name': 'anosh', 'username': 'KingNoosh',
                           'avatar_id': 'wzzJHfPD1Sgc2HoZ9x',
                           'avatar': 'https://giphy.com/embed/sZ5CxgSUsRclBTQeGc'})
