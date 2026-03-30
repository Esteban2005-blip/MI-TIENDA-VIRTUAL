"""
Modelo de Productos para la base de datos MySQL (conexión directa)
"""

from db import get_connection
from datetime import datetime


def _has_column(cursor, table_name, column_name):
    cursor.execute(f"SHOW COLUMNS FROM {table_name} LIKE %s", (column_name,))
    return cursor.fetchone() is not None

# Funciones CRUD para productos usando MySQL directo
def obtener_productos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    from datetime import datetime
    for p in productos:
        if 'cantidad' not in p and 'stock' in p:
            p['cantidad'] = p.get('stock')
        if 'stock' not in p and 'cantidad' in p:
            p['stock'] = p.get('cantidad')
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
    cantidad_col = 'cantidad' if _has_column(cursor, 'productos', 'cantidad') else ('stock' if _has_column(cursor, 'productos', 'stock') else None)
    has_fecha_creacion = _has_column(cursor, 'productos', 'fecha_creacion')

    columns = ['nombre', 'descripcion', 'precio']
    values = [nombre, descripcion, precio]

    if cantidad_col:
        columns.append(cantidad_col)
        values.append(int(cantidad or 0))

    columns.extend(['categoria', 'imagen'])
    values.extend([categoria, imagen])

    if has_fecha_creacion:
        columns.append('fecha_creacion')
        values.append(datetime.utcnow())

    placeholders = ', '.join(['%s'] * len(columns))
    cols_sql = ', '.join(columns)
    cursor.execute(
        f"INSERT INTO productos ({cols_sql}) VALUES ({placeholders})",
        tuple(values)
    )
    conn.commit()
    cursor.close()
    conn.close()

def actualizar_producto(producto_id, nombre, descripcion, precio, cantidad, categoria, imagen=None):
    conn = get_connection()
    cursor = conn.cursor()
    cantidad_col = 'cantidad' if _has_column(cursor, 'productos', 'cantidad') else ('stock' if _has_column(cursor, 'productos', 'stock') else None)

    set_parts = ['nombre=%s', 'descripcion=%s', 'precio=%s', 'categoria=%s', 'imagen=%s']
    values = [nombre, descripcion, precio, categoria, imagen]

    if cantidad_col:
        set_parts.append(f"{cantidad_col}=%s")
        values.append(int(cantidad or 0))

    values.append(producto_id)
    set_sql = ', '.join(set_parts)
    cursor.execute(
        f"UPDATE productos SET {set_sql} WHERE id=%s",
        tuple(values)
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
