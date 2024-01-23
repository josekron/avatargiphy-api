import requests
import logging


class GiphyService:
    """GiphyService contains the Giphy API implementation
    We get the settings (url, API key, limit results, rating) from .env,
    and we pass them in the constructor"""

    def __init__(self, config):
        self.config = config

    def get_trending_gifs(self):
        giphy_url = self.config['BASE_URL'] + 'trending?api_key=' + self.config['API_TOKEN'] + \
                    '&limit=' + str(self.config['LIMIT_RESULTS']) + '&rating=' + self.config['RATING']

        logging.info('giphy url: {}'.format(giphy_url))

        response = requests.get(giphy_url)

        if response.status_code != 200:
            logging.error('Giphy returned status code {}: {}'.format(
                response.status_code, response.text))
            raise ValueError('Gyphy is unavailable')

        return list({'id': i['id'], 'url': i['embed_url']} for i in response.json()['data'])

    def search_gif_by_id(self, gif_id):
        giphy_url = self.config['BASE_URL'] + gif_id + '?api_key=' + self.config['API_TOKEN']

        logging.info('giphy url: {}'.format(giphy_url))

        response = requests.get(giphy_url)

        if response.status_code != 200:
            logging.error('Giphy returned status code {}: {}'.format(
                response.status_code, response.text))
            if response.status_code == 404:
                return None
            else:
                raise ValueError('Gyphy is unavailable')

        if response.json()['data']:
            return {'id': response.json()['data']['id'], 'url': response.json()['data']['embed_url']}
        else:
            return None
