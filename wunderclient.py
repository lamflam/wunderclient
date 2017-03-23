
import json
from collections import namedtuple
from urllib import urlencode
import requests

# constants
API_PREFIX = 'https://a.wunderlist.com/api/v1/'


# types
List = namedtuple('List', ['id', 'created_at', 'title', 'list_type', 'type', 'revision'])


class WunderClient(object):

    def __init__(self, client_id=None, access_token=None):
        self.client_id = client_id
        self.access_token = access_token

    def _path(self, path=None, params=None):
        full_path = '{}{}'.format(API_PREFIX, path)
        if params is not None:
            full_path = '{}?{}'.format(full_path, urlencode(params))
        return full_path

    def _headers(self):
        return {
            'X-Client-ID': self.client_id,
            'X-Access-Token': self.access_token,
            'Accept': 'application/json'
        }

    def _json(self, data):
        if hasattr(data, '_asdict'):
            ret = json.dumps(data._asdict())
        else:
            ret = json.dumps(data)
        return ret

    def _get(self, path=None, params=None):
        resp = requests.get(self._path(path, params), headers=self._headers())
        resp.raise_for_status()
        return resp.json()

    def _post(self, path=None, params=None):
        headers = self._headers()
        headers['Content-Type'] = 'application/json'
        resp = requests.post(self._path(path), headers=headers, data=self._json(params))
        resp.raise_for_status()
        return resp.json()

    def _delete(self, path=None, params=None):
        resp = requests.delete(self._path(path, params), headers=self._headers())
        resp.raise_for_status()

    def me(self):
        return self._get('user')

    def get_lists(self):
        return self._get('lists')

    def get_list(self, id=None, title=None):
        if id is None and title is None:
            raise ValidationException('Must provide a `title` or `id`')

        if id is None:
            for l in self.get_lists():
                if l.get('title') == title:
                    id = l.get('id')
                    break
        if id is None:
            raise ValidationException('List with title=`{}` does not exist'.format(title))

        return self._get('lists/{}'.format(id))

    def create_list(self, title):
        if title is None:
            raise ValidationException('\'title\' is required.')
        elif not isinstance(title, basestring):
            raise ValidationException('\'title\' must be a string')

        return self._post('lists', {'title': title})

    def delete_list(self, id=None, title=None):
        if id is None:
            l = self.get_list(title=title)
            id = l['id']
        self._delete('lists/{}'.format(id), params={'revision': l['revision']})


class ValidationException(Exception):
    pass
