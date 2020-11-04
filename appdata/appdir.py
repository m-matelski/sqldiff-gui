import errno
import os

from appdirs import user_data_dir

_APPDATA = user_data_dir('sqldiff', 'sqrek')
_CONNECTIONS = 'connections.json'

PATH_CONNECTIONS = os.path.join(_APPDATA, _CONNECTIONS)


def create_path_file(filepath):
    """Create path and file if not exists"""
    if not os.path.exists(os.path.dirname(filepath)):
        try:
            os.makedirs(os.path.dirname(filepath))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    if not os.path.exists(filepath):
        with open(filepath, "w") as f:
            pass

