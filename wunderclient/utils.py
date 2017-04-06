
# Compatibility
try: from urllib import urlencode  # noqa
except: from urllib.parse import urlencode  # noqa

try: basestring  # noqa
except: basestring = str  # noqa

try: from nose.tools import assert_is_instance  # noqa
except:
    from nose.tools import assert_true
    def assert_is_instance(obj, types, msg=None):
        assert_true(isinstance(obj, types), msg)


def namedtype(typename, fields):
    if isinstance(fields, basestring):
        fields = [f.strip() for f in fields.split(',')]
    else:
        fields = list(fields)
    return type(typename, (_namedtype,), {'_fields': fields})


class _namedtype(dict):

    @property
    def _fields(self):
        return self.__class__._fields

    def __init__(self, *args, **kwargs):
        for k in kwargs.keys():
            if k not in self._fields:
                kwargs.pop(k)
        for f in self._fields:
            if f not in kwargs:
                kwargs[f] = None
        super(_namedtype, self).__init__(*args, **kwargs)

    def __getattr__(self, name):
        if name in self._fields:
            return self.get(name)
        else:
            raise AttributeError('No such attribute: ' + name)

    def __setattr__(self, name, value):
        if name in self._fields:
            self[name] = value
        else:
            raise AttributeError('No such attribute: ' + name)

    def __delattr__(self, name):
        if name in self._fields:
            del self[name]
        else:
            raise AttributeError('No such attribute: ' + name)

    def __repr__(self):
        field_str = ', '.join(['{}={}'.format(f, self[f]) for f in self._fields])
        return '{}({})'.format(self.__class__.__name__, field_str)
