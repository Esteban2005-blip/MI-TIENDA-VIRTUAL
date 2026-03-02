"""Archivo de inicialización para crear datos de muestra"""

from app import app
from inventario.bd import db
from inventario.productos import Producto
from inventario.inventario import GestorArchivos

def crear_datos_muestra():
    """Crear datos de muestra para probar la aplicación"""
    with app.app_context():
        # Verificar si hay productos existentes
        if Producto.query.count() == 0:
            # Crear productos de muestra
            gestor = GestorArchivos()
            
            productos = [
                Producto(
                    nombre='Laptop Dell XPS',
                    descripcion='Laptop de alto rendimiento para programación',
                    precio=1299.99,
                    cantidad=5,
                    categoria='Electrónica'
                ),
                Producto(
                    nombre='Mouse Logitech MX Master',
                    descripcion='Mouse profesional inalámbrico',
                    precio=99.99,
                    cantidad=15,
                    categoria='Electrónica'
                ),
                Producto(
                    nombre='Teclado Mecánico RGB',
                    descripcion='Teclado mecánico con retroiluminación RGB',
                    precio=149.99,
                    cantidad=8,
                    categoria='Electrónica'
                ),
                Producto(
                    nombre='Monitor LG 27"',
                    descripcion='Monitor 4K de 27 pulgadas',
                    precio=399.99,
                    cantidad=3,
                    categoria='Electrónica'
                ),
                Producto(
                    nombre='Headphones Sony WH-1000',
                    descripcion='Audífonos con cancelación de ruido',
                    precio=279.99,
                    cantidad=10,
                    categoria='Electrónica'
                ),
            ]
            
            for producto in productos:
                db.session.add(producto)
                db.session.commit()
                
                # Guardar en archivos
                producto_dict = producto.to_dict()
                gestor.guardar_en_json(producto_dict)
                gestor.guardar_en_csv(producto_dict)
                gestor.guardar_en_txt(f"Producto creado: {producto.nombre} - ${producto.precio}")
            
            print(f"[OK] {len(productos)} productos de muestra creados")
        else:
            print(f"[OK] Base de datos ya contiene {Producto.query.count()} productos")

if __name__ == '__main__':
    crear_datos_muestra()
    print("[OK] Datos inicializados correctamente")
