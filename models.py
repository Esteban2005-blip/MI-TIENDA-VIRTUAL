from flask_login import UserMixin
from db import get_connection

class User(UserMixin):
    def __init__(self, id_usuario, nombre, email, password):
        self.id = id_usuario
        self.nombre = nombre
        self.email = email
        self.password = password

    @staticmethod
    def get_by_id(user_id):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM usuarios WHERE id_usuario = %s', (user_id,))
            user = cursor.fetchone()
            if user:
                return User(user['id_usuario'], user['nombre'], user['email'], user['password'])
            return None
        except Exception as e:
            print(f"Error en User.get_by_id: {e}")
            return None
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    @staticmethod
    def get_by_email(email):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM usuarios WHERE email = %s', (email,))
            user = cursor.fetchone()
            if user:
                return User(user['id_usuario'], user['nombre'], user['email'], user['password'])
            return None
        except Exception as e:
            print(f"Error en User.get_by_email: {e}")
            return None
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()
