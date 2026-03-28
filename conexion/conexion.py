import os
from urllib.parse import urlparse, unquote

import mysql.connector


def get_mysql_connection():
    """Conexión MySQL usando variables de entorno (local y producción/web)."""
    db_url = os.environ.get('MYSQL_URL') or os.environ.get('DATABASE_URL')
    if db_url:
        parsed = urlparse(db_url)
        if parsed.scheme.startswith('mysql'):
            return mysql.connector.connect(
                host=parsed.hostname or os.environ.get('MYSQL_HOST', 'localhost'),
                user=unquote(parsed.username) if parsed.username else os.environ.get('MYSQL_USER', 'root'),
                password=unquote(parsed.password) if parsed.password else os.environ.get('MYSQL_PASSWORD', ''),
                database=parsed.path.lstrip('/') or os.environ.get('MYSQL_DATABASE', 'tienda_virtual'),
                port=parsed.port or int(os.environ.get('MYSQL_PORT', 3306)),
                connection_timeout=int(os.environ.get('MYSQL_CONNECT_TIMEOUT', 10)),
            )

    return mysql.connector.connect(
        host=os.environ.get('MYSQL_HOST', 'yamabiko.proxy.rlwy.net'),
        user=os.environ.get('MYSQL_USER', 'root'),
        password=os.environ.get('MYSQL_PASSWORD', 'oUGAoHObQHXalQaJxoqFTdFjGxPTCdZO'),
        database=os.environ.get('MYSQL_DATABASE', 'railway'),
        port=int(os.environ.get('MYSQL_PORT', 23455)),
        connection_timeout=int(os.environ.get('MYSQL_CONNECT_TIMEOUT', 10)),
    )
