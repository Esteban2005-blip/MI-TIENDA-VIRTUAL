import mysql.connector

def get_mysql_connection():
    return mysql.connector.connect(
        host="localhost",         # Cambia si tu host es diferente
        user="root",              # Cambia por tu usuario de MySQL
        password="tu_contraseña", # Cambia por tu contraseña de MySQL
        database="tienda_virtual" # Cambia por el nombre de tu base de datos
    )
