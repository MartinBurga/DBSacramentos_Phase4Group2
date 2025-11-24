# db.py
import pyodbc
import json
import os

def get_connection():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, 'config.json')

    with open(config_path, 'r') as archivo_config:
        config = json.load(archivo_config)

    server = config['server']
    database = config['database']
    username = config['user']
    password = config['password']
    odbc_driver = config['odbc_driver']

    connection_string = (
        f"DRIVER={{{odbc_driver}}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password}"
    )

    return pyodbc.connect(connection_string)
