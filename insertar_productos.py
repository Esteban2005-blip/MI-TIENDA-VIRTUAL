"""
Inserta los productos de muestra en la tabla productos de Railway.
Ejecutar una sola vez: python insertar_productos.py
"""
from db import get_connection

PRODUCTOS = [
    ('Laptop Dell XPS',           'Portátil premium de alto rendimiento',                 2500.00,  5, 'Electrónica', 'images/laptop_dell_xps.jpg'),
    ('Mouse Logitech MX Master',  'Mouse inalámbrico ergonómico',                          120.00, 10, 'Electrónica', 'images/mouse_logitech_mx_master.jpg'),
    ('Teclado Mecánico RGB',      'Teclado retroiluminado para gamers',                     80.00,  7, 'Electrónica', 'images/teclado_rgb.jpg'),
    ('Monitor LG 27"',            'Monitor IPS Full HD',                                   350.00,  4, 'Electrónica', 'images/monitor_lg_27.jpg'),
    ('Headphones Sony WH-1000',   'Auriculares inalámbricos con cancelación de ruido',     300.00,  6, 'Electrónica', 'images/headphones_sony_wh1000.jpg'),
    ('Laptop ASUS TUF Gaming A16','Laptop gamer de alto rendimiento',                     1800.00,  3, 'Electrónica', 'images/laptop_asus_tuf.jpg'),
    ('Teléfono Samsung S24',      'Smartphone de última generación',                      1200.00,  8, 'Electrónica', 'images/telefono_samsung_s24.jpg'),
]

def main():
    conn = get_connection()
    cursor = conn.cursor()
    insertados = 0
    for prod in PRODUCTOS:
        nombre = prod[0]
        cursor.execute("SELECT id FROM productos WHERE nombre = %s", (nombre,))
        if cursor.fetchone():
            print(f"  Ya existe: {nombre}")
            continue
        cursor.execute(
            "INSERT INTO productos (nombre, descripcion, precio, cantidad, categoria, imagen) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            prod
        )
        print(f"  Insertado: {nombre}")
        insertados += 1
    conn.commit()
    cursor.close()
    conn.close()
    print(f"\nListo. {insertados} productos nuevos agregados a Railway.")

if __name__ == "__main__":
    main()
