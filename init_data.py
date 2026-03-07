"""Archivo de inicialización para crear datos de muestra"""

from app import app
from inventario.bd import db
from inventario.productos import Producto
from inventario.inventario import GestorArchivos

def crear_datos_muestra():
    """Crear datos de muestra para probar la aplicación"""
    with app.app_context():
        # Eliminar todos los productos existentes
        Producto.query.delete()
        db.session.commit()
        # Crear productos de muestra
        productos = [
            Producto(
                nombre='Laptop Dell XPS',
                descripcion='Portátil premium de alto rendimiento',
                precio=2500.00,
                cantidad=5,
                categoria='Electrónica',
                imagen='images/laptop_dell_xps.jpg'
            ),
            Producto(
                nombre='Mouse Logitech MX Master',
                descripcion='Mouse inalámbrico ergonómico',
                precio=120.00,
                cantidad=10,
                categoria='Electrónica',
                imagen='images/mouse_logitech_mx_master.jpg'
            ),
            Producto(
                nombre='Teclado Mecánico RGB',
                descripcion='Teclado retroiluminado para gamers',
                precio=80.00,
                cantidad=7,
                categoria='Electrónica',
                imagen='images/teclado_rgb.jpg'
            ),
            Producto(
                nombre='Monitor LG 27"',
                descripcion='Monitor IPS Full HD',
                precio=350.00,
                cantidad=4,
                categoria='Electrónica',
                imagen='images/monitor_lg_27.jpg'
            ),
            Producto(
                nombre='Headphones Sony WH-1000',
                descripcion='Auriculares inalámbricos con cancelación de ruido',
                precio=300.00,
                cantidad=6,
                categoria='Electrónica',
                imagen='images/headphones_sony_wh1000.jpg'
            ),
            Producto(
                nombre='LAPTO ASUS TUF GAMING A16',
                descripcion='Laptop gamer de alto rendimiento',
                precio=1800.00,
                cantidad=3,
                categoria='Electrónica',
                imagen='images/laptop_asus_tuf.jpg'
            ),
            Producto(
                nombre='TELEFONO SAMGUNG S24',
                descripcion='Smartphone de última generación',
                precio=1200.00,
                cantidad=8,
                categoria='Electrónica',
                imagen='images/telefono_samsung_s24.jpg'
            )
        ]
        for prod in productos:
            db.session.add(prod)
            print(f"Agregado: {prod.nombre} -> {prod.imagen}")
        db.session.commit()
        print('Productos iniciales agregados.')

if __name__ == '__main__':
    crear_datos_muestra()
    print("[OK] Datos inicializados correctamente")
