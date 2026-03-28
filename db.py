
# Conexión MySQL para Flask (local y producción)
import os
from urllib.parse import urlparse, unquote

import mysql.connector


def _build_mysql_config():
    # Permite usar URLs completas en despliegues (por ejemplo, Render).
    db_url = os.environ.get('MYSQL_URL') or os.environ.get('DATABASE_URL')
    if db_url:
        parsed = urlparse(db_url)
        if parsed.scheme.startswith('mysql'):
            database = parsed.path.lstrip('/') if parsed.path else os.environ.get('MYSQL_DATABASE', 'tienda_virtual')
            return {
                'host': parsed.hostname or os.environ.get('MYSQL_HOST', 'localhost'),
                'user': unquote(parsed.username) if parsed.username else os.environ.get('MYSQL_USER', 'root'),
                'password': unquote(parsed.password) if parsed.password else os.environ.get('MYSQL_PASSWORD', ''),
                'database': database,
                'port': parsed.port or int(os.environ.get('MYSQL_PORT', 3306)),
                'connection_timeout': int(os.environ.get('MYSQL_CONNECT_TIMEOUT', 10)),
            }

    return {
        'host': os.environ.get('MYSQL_HOST', 'yamabiko.proxy.rlwy.net'),
        'user': os.environ.get('MYSQL_USER', 'root'),
        'password': os.environ.get('MYSQL_PASSWORD', 'oUGAoHObQHXalQaJxoqFTdFjGxPTCdZO'),
        'database': os.environ.get('MYSQL_DATABASE', 'railway'),
        'port': int(os.environ.get('MYSQL_PORT', 23455)),
        'connection_timeout': int(os.environ.get('MYSQL_CONNECT_TIMEOUT', 10)),
    }


def get_connection():
    return mysql.connector.connect(**_build_mysql_config())
