from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id=None, email=None, password=None, nombre=None):
        self.id = id
        self.email = email
        self.password = password
        self.nombre = nombre

    @staticmethod
    def get_by_id(user_id):
        import mysql.connector
        import os
        try:
            conn = mysql.connector.connect(
                host=os.environ.get('MYSQL_HOST', 'localhost'),
                user=os.environ.get('MYSQL_USER', 'root'),
                password=os.environ.get('MYSQL_PASSWORD', ''),
                database=os.environ.get('MYSQL_DATABASE', 'tienda_virtual'),
                port=int(os.environ.get('MYSQL_PORT', 3306))
            )
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (user_id,))
            row = cursor.fetchone()
            cursor.close()
            conn.close()
            if row:
                return User(
                    id=row.get('id_usuario'),
                    email=row.get('email'),
                    password=row.get('password'),
                    nombre=row.get('nombre')
                )
            return None
        except Exception as e:
            print(f"Error en get_by_id: {e}")
            return None

    @staticmethod
    def get_by_email(email):
        import mysql.connector
        import os
        try:
            conn = mysql.connector.connect(
                host=os.environ.get('MYSQL_HOST', 'localhost'),
                user=os.environ.get('MYSQL_USER', 'root'),
                password=os.environ.get('MYSQL_PASSWORD', ''),
                database=os.environ.get('MYSQL_DATABASE', 'tienda_virtual'),
                port=int(os.environ.get('MYSQL_PORT', 3306))
            )
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            row = cursor.fetchone()
            cursor.close()
            conn.close()
            if row:
                return User(
                    id=row.get('id_usuario'),
                    email=row.get('email'),
                    password=row.get('password'),
                    nombre=row.get('nombre')
                )
            return None
        except Exception as e:
            print(f"Error en get_by_email: {e}")
            return None
