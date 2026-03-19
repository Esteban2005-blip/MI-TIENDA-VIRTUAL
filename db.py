

# Conexión MySQL para Flask
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',  # Sin contraseña
        database='tienda_virtual'  # Nombre real de la base de datos
    )
