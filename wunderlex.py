
import requests

API_PREFIX = 'https://a.wunderlist.com/api/v1/'


class WunderLex(object):

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
            return requests.get(path, headers=headers)

    def me(self):
        resp = self.request('user')
        resp.raise_for_status()
        return resp.json()
