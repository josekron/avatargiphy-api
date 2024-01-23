import logging
import os

from flask import Flask

from api.controller.avatar_api import avatar_api
from api.controller.user_api import user_api
from flask_caching import Cache
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)


def create_app(test_config=None):
    app = Flask(__name__)

    # Giphy API config
    app.config.giphy_api = {
        'BASE_URL': os.environ.get("GIPHY_BASE_URL"),
        'API_TOKEN': os.environ.get("GIPHY_API_TOKEN"),
        'LIMIT_RESULTS': os.environ.get("GIPHY_LIMIT_RESULTS"),
        'RATING': os.environ.get("GIPHY_RATING")
    }

    # Set up Cache
    config = {
        'DEBUG': True,
        'CACHE_TYPE': 'SimpleCache',
        'CACHE_DEFAULT_TIMEOUT': 300
    }

    app.config.from_mapping(config)
    cache = Cache(app)
    cache.init_app(app)

    app.config.db_cache = {
        'DB': cache
    }

    # Register endpoints
    app.register_blueprint(user_api, url_prefix='/users')
    app.register_blueprint(avatar_api, url_prefix='/avatars')

    return app


app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5005))
    app.run(debug=True, host='0.0.0.0', port=port)
