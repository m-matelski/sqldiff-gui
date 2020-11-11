import errno
import json
import os
import pathlib

import psycopg2
import teradatasql

from appdata import appdir

appdir.create_path_file(appdir.PATH_CONNECTIONS)


def read_connection_data():
    with open(appdir.PATH_CONNECTIONS, 'r') as f:
        connections_json = f.read()
        connections_dict = json.loads(connections_json or '{}')
        return connections_dict


def save_connection_data(connection_dict):
    with open(appdir.PATH_CONNECTIONS, 'w') as f:
        f.write(json.dumps(connection_dict))


connection_drivers = {
    'psycopg2': psycopg2.connect,
    'teradatasql': teradatasql.connect
}