
import requests

API_PREFIX = 'https://a.wunderlist.com/api/v1/'


class WunderClient(object):

    def __init__(self, client_id=None, access_token=None):
        self.client_id = client_id
        self.access_token = access_token

    def request(self, path=None, method='GET'):
        headers = {
            'X-Client-ID': self.client_id,
            'X-Access-Token': self.access_token
        }
        path = '{}{}'.format(API_PREFIX, path)

        if method == 'GET':
            resp = requests.get(path, headers=headers)
            resp.raise_for_status()
            return resp.json()

    def me(self):
        return self.request('user')

    def get_lists(self):
        return self.request('lists')

    def get_list(self, id):
        return self.request('lists/{}'.format(id))
