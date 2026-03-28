"""
Script para crear las tablas en la base de datos de Railway.
Ejecutar una sola vez: python crear_tablas.py
"""
from db import get_connection

SQL_TABLAS = [
    """
    CREATE TABLE IF NOT EXISTS usuarios (
        id_usuario  INT AUTO_INCREMENT PRIMARY KEY,
        nombre      VARCHAR(100)  NOT NULL,
        email       VARCHAR(150)  NOT NULL UNIQUE,
        password    VARCHAR(255)  NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS productos (
        id              INT AUTO_INCREMENT PRIMARY KEY,
        nombre          VARCHAR(150)    NOT NULL,
        descripcion     TEXT,
        precio          DECIMAL(10, 2)  NOT NULL DEFAULT 0.00,
        cantidad        INT             NOT NULL DEFAULT 0,
        categoria       VARCHAR(100),
        imagen          VARCHAR(255),
        fecha_creacion  DATETIME        DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS clientes (
        id_cliente      INT AUTO_INCREMENT PRIMARY KEY,
        nombre          VARCHAR(100)  NOT NULL,
        email           VARCHAR(150)  NOT NULL UNIQUE,
        telefono        VARCHAR(30),
        ciudad          VARCHAR(100),
        direccion       VARCHAR(255),
        total_compras   INT           NOT NULL DEFAULT 0,
        fecha_registro  DATETIME      DEFAULT CURRENT_TIMESTAMP
    )
    """,
]

def main():
    conn = get_connection()
    cursor = conn.cursor()
    for sql in SQL_TABLAS:
        cursor.execute(sql)
        print("Tabla creada (o ya existía).")
    conn.commit()
    cursor.close()
    conn.close()
    print("Listo. Tablas listas en Railway.")

if __name__ == "__main__":
    main()
