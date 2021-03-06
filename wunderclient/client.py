
import json
import requests
from wunderclient.utils import namedtype, urlencode


# constants
API_PREFIX = 'https://a.wunderlist.com/api/v1/'


# types
User = namedtype('User', 'id, name, email, created_at, revision')
List = namedtype('List', 'id, title, created_at, revision')
Task = namedtype('Task', 'id, title, assignee_id, created_at, created_by_id, starred, due_date, list_id, revision')
ALL_TYPES = [User, List, Task]


class WunderClient(object):

    def __init__(self, client_id=None, access_token=None, requests=requests):
        self.requests = requests
        self.client_id = client_id
        self.access_token = access_token

    def _path(self, path=None, params=None):
        full_path = '{0}{1}'.format(API_PREFIX, path)
        if params is not None:
            full_path = '{0}?{1}'.format(full_path, urlencode(params))
        return full_path

    def _headers(self):
        return {
            'X-Client-ID': self.client_id,
            'X-Access-Token': self.access_token,
            'Accept': 'application/json'
        }

    def _get(self, path=None, params=None):
        resp = self.requests.get(self._path(path, params), headers=self._headers())
        resp.raise_for_status()
        return resp.json()

    def _post(self, path=None, params=None):
        headers = self._headers()
        headers['Content-Type'] = 'application/json'
        resp = self.requests.post(self._path(path), headers=headers, data=json.dumps(params))
        resp.raise_for_status()
        return resp.json()

    def _patch(self, path=None, params=None):
        headers = self._headers()
        headers['Content-Type'] = 'application/json'
        resp = self.requests.patch(self._path(path), headers=headers, data=json.dumps(params))
        resp.raise_for_status()
        return resp.json()

    def _delete(self, path=None, params=None):
        resp = self.requests.delete(self._path(path, params), headers=self._headers())
        resp.raise_for_status()

    def me(self):
        return User(**self._get('user'))

    def get_lists(self):
        return [List(**lst) for lst in self._get('lists')]

    def get_list(self, id):
        if id is None:
            raise ValidationError('id required')
        return List(**self._get('lists/{0}'.format(id)))

    def create_list(self, **lst):
        lst = List(**lst)
        if lst.title is None:
            raise ValidationError('A title is required.')

        return List(**self._post('lists', {'title': lst.title}))

    def update_list(self, **lst):
        lst = List(**lst)
        if lst.id is None or lst.revision is None:
            raise ValidationError('id and revision are required')
        return List(**self._patch('lists/{0}'.format(lst.id), params=lst))

    def delete_list(self, **lst):
        lst = List(**lst)
        if lst.id is None or lst.revision is None:
            raise ValidationError('id and revision are required')
        self._delete('lists/{0}'.format(lst.id), params={'revision': lst.revision})

    def get_tasks(self, list_id, completed=False):
        return [Task(**task) for task in self._get('tasks', params={'list_id': list_id, 'completed': completed})]

    def get_task(self, id):
        if id is None:
            raise ValidationError('id required')
        return Task(**self._get('tasks/{0}'.format(id)))

    def create_task(self, **task):
        task = Task(**task)
        if task.list_id is None or task.title is None:
            raise ValidationError('id and title are required.')
        return Task(**self._post('tasks', params=task))

    def update_task(self, **task):
        task = Task(**task)
        if task.id is None or task.revision is None:
            raise ValidationError('id and revision are required')
        return Task(**self._patch('tasks/{0}'.format(task.id), params=task))

    def delete_task(self, **task):
        task = Task(**task)
        if task.id is None or task.revision is None:
            raise ValidationError('id and revision are required')
        self._delete('tasks/{0}'.format(task.id), params={'revision': task.revision})


class ValidationError(Exception):
    pass
