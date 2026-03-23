# services/producto_service.py
from conexion.conexion import get_mysql_connection
from models.producto import Producto

def obtener_todos():
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM productos')
    productos = [Producto(**row) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return productos

def obtener_por_id(id_producto):
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM productos WHERE id_producto = %s', (id_producto,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return Producto(**row) if row else None

def crear(producto):
    conn = get_mysql_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO productos (nombre, precio, stock, descripcion, categoria, imagen) VALUES (%s, %s, %s, %s, %s, %s)',
                   (producto.nombre, producto.precio, producto.stock, producto.descripcion, producto.categoria, producto.imagen))
    conn.commit()
    cursor.close()
    conn.close()

def actualizar(producto):
    conn = get_mysql_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE productos SET nombre=%s, precio=%s, stock=%s, descripcion=%s, categoria=%s, imagen=%s WHERE id_producto=%s',
                   (producto.nombre, producto.precio, producto.stock, producto.descripcion, producto.categoria, producto.imagen, producto.id_producto))
    conn.commit()
    cursor.close()
    conn.close()

def eliminar(id_producto):
    conn = get_mysql_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM productos WHERE id_producto = %s', (id_producto,))
    conn.commit()
    cursor.close()
    conn.close()
