import json
import pkgutil

class Language:
    def __init__(self, fpath):
        self._inner = {}
        self._fpath = fpath

        data = pkgutil.get_data(__name__, fpath).decode('utf-8')
        self._inner = json.loads(data)

    def __getattr__(self, key):
        return self._inner
