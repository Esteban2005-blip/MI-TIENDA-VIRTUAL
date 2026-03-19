"""
Modelo de Productos para la base de datos MySQL (conexión directa)
"""

from db import get_connection
from datetime import datetime

# Funciones CRUD para productos usando MySQL directo
def obtener_productos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    from datetime import datetime
    for p in productos:
        p.setdefault('id', None)
        p.setdefault('nombre', '')
        p.setdefault('descripcion', '')
        p.setdefault('precio', 0.0)
        p.setdefault('cantidad', 0)
        p.setdefault('categoria', '')
        p.setdefault('imagen', None)
        fecha = p.get('fecha_creacion')
        if fecha and not isinstance(fecha, datetime):
            try:
                # Maneja string con o sin microsegundos
                if '.' in str(fecha):
                    p['fecha_creacion'] = datetime.strptime(str(fecha), '%Y-%m-%d %H:%M:%S.%f')
                else:
                    p['fecha_creacion'] = datetime.strptime(str(fecha), '%Y-%m-%d %H:%M:%S')
            except Exception:
                p['fecha_creacion'] = None
        elif not fecha:
            p['fecha_creacion'] = None
    cursor.close()
    conn.close()
    return productos

def obtener_producto_por_id(producto_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE id = %s", (producto_id,))
    producto = cursor.fetchone()
    cursor.close()
    conn.close()
    return producto

def crear_producto(nombre, descripcion, precio, cantidad, categoria, imagen=None):
    conn = get_connection()
    cursor = conn.cursor()
    fecha_creacion = datetime.utcnow()
    cursor.execute(
        "INSERT INTO productos (nombre, descripcion, precio, cantidad, categoria, imagen, fecha_creacion) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (nombre, descripcion, precio, cantidad, categoria, imagen, fecha_creacion)
    )
    conn.commit()
    cursor.close()
    conn.close()

def actualizar_producto(producto_id, nombre, descripcion, precio, cantidad, categoria, imagen=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE productos SET nombre=%s, descripcion=%s, precio=%s, cantidad=%s, categoria=%s, imagen=%s WHERE id=%s",
        (nombre, descripcion, precio, cantidad, categoria, imagen, producto_id)
    )
    conn.commit()
    cursor.close()
    conn.close()

def eliminar_producto(producto_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id = %s", (producto_id,))
    conn.commit()
    cursor.close()
    conn.close()
