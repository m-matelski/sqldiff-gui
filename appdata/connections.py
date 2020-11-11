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


def connect_psycopg2(params):
    connection_params = {k: v for k, v in params.items() if k not in ('name', 'driver') and v}
    return psycopg2.connect(**connection_params)

def connect_teradatasql(params):
    connection_params = {k: v for k, v in params.items() if k not in ('name', 'driver') and v}
    return teradatasql.connect(**connection_params)




connection_drivers = {
    'psycopg2': connect_psycopg2,
    'teradatasql': connect_teradatasql
}