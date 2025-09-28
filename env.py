from os import environ

host = environ.get("ONU_HOST") or '192.168.1.1'
username = environ.get("ONU_USERNAME") or 'admin'
password = environ.get("ONU_PASSWORD") or 'admin'

listen_host = environ.get("APP_HOST") or '0.0.0.0'
listen_port = int(environ.get("APP_PORT") or 8080)