"""
Aplicación Flask - Tienda Virtual
Semana 13: Persistencia de datos (TXT, JSON, CSV, SQLite)
"""

from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash, send_from_directory
from inventario.bd import init_db, db
from inventario.productos import Producto
from inventario.inventario import GestorArchivos
import os
from werkzeug.utils import secure_filename

# Crear instancia de la aplicación Flask
app = Flask(__name__)

# Configuración de la aplicación
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventario.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# clave secreta para sesiones
app.secret_key = os.environ.get('SECRET_KEY', 'devkey')

# Inicializar base de datos
init_db(app)

# Crear instancia del gestor de archivos
gestor_archivos = GestorArchivos()


# ===================== RUTAS PRINCIPALES =====================

@app.route('/')
def index():
    """Página de inicio - Dashboard principal"""
    return render_template('index.html')


@app.route('/about')
def about():
    """Página Acerca de - Información de la empresa"""
    return render_template('about.html')


@app.route('/productos')
def productos():
    """Página de Productos - Catálogo de productos con búsqueda"""
    # parámetros de filtrado
    q = request.args.get('q', '').strip()
    categoria = request.args.get('categoria', '').strip()

    # construir consulta base
    consulta = Producto.query
    if q:
        consulta = consulta.filter(Producto.nombre.ilike(f"%{q}%"))
    if categoria and categoria != '':
        consulta = consulta.filter_by(categoria=categoria)

    productos = consulta.all()
    return render_template('productos.html', productos=productos, q=q, categoria=categoria)


@app.route('/clientes')
def clientes():
    """Página de Clientes - Gestión de clientes"""
    return render_template('clientes.html')


# ===================== CARRITO =====================

@app.route('/carrito')
def ver_carrito():
    """Mostrar los productos agregados al carrito"""
    items = session.get('carrito', [])
    productos = []
    for prod_id in items:
        p = Producto.query.get(prod_id)
        if p:
            productos.append(p)
    total = sum(p.precio for p in productos)
    return render_template('carrito.html', productos=productos, total=total)

@app.route('/carrito/agregar/<int:prod_id>')
def agregar_carrito(prod_id):
    """Agregar un producto al carrito en sesión"""
    carrito = session.get('carrito', [])
    carrito.append(prod_id)
    session['carrito'] = carrito
    flash('Producto agregado al carrito', 'success')
    return redirect(request.referrer or url_for('productos'))

@app.route('/carrito/vaciar')
def vaciar_carrito():
    session.pop('carrito', None)
    flash('Carrito vaciado', 'info')
    return redirect(url_for('productos'))


@app.route('/facturas')
def facturas():
    """Página de Facturas - Gestión de facturas"""
    return render_template('facturas.html')


@app.route('/contacto')
def contacto():
    """Página de Contacto - Información de contacto y formulario"""
    return render_template('contacto.html')


# ===================== RUTAS DE PERSISTENCIA DE DATOS =====================

@app.route('/datos')
def datos():
    """Página que muestra datos en diferentes formatos"""
    datos_txt = gestor_archivos.leer_txt()
    datos_json = gestor_archivos.leer_json()
    datos_csv = gestor_archivos.leer_csv()
    
    return render_template('datos.html', 
                         datos_txt=datos_txt,
                         datos_json=datos_json,
                         datos_csv=datos_csv)


# ===================== RUTAS CRUD DE PRODUCTOS (SQLite) =====================

@app.route('/api/productos', methods=['GET'])
def obtener_productos():
    """Obtener todos los productos de la base de datos"""
    try:
        productos = Producto.query.all()
        return jsonify([p.to_dict() for p in productos])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/productos/<int:id>', methods=['GET'])
def obtener_producto(id):
    """Obtener un producto específico"""
    try:
        producto = Producto.query.get(id)
        if not producto:
            return jsonify({'error': 'Producto no encontrado'}), 404
        return jsonify(producto.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/productos/crear', methods=['POST'])
def crear_producto():
    """Crear un nuevo producto"""
    try:
        datos = request.get_json() if request.is_json else request.form.to_dict()
        
        # Validar datos necesarios
        if not datos.get('nombre') or not datos.get('precio') or not datos.get('categoria'):
            return jsonify({'error': 'Faltan campos requeridos'}), 400
        
        # Crear producto en SQLite
        nuevo_producto = Producto(
            nombre=datos.get('nombre'),
            descripcion=datos.get('descripcion', ''),
            precio=float(datos.get('precio', 0)),
            cantidad=int(datos.get('cantidad', 0)),
            categoria=datos.get('categoria', '')
        )
        
        db.session.add(nuevo_producto)
        db.session.commit()
        
        # Guardar también en archivos
        producto_dict = nuevo_producto.to_dict()
        gestor_archivos.guardar_en_json(producto_dict)
        gestor_archivos.guardar_en_csv(producto_dict)
        gestor_archivos.guardar_en_txt(f"Producto creado: {nuevo_producto.nombre}")
        
        return jsonify({
            'mensaje': 'Producto creado exitosamente',
            'producto': producto_dict
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/productos/<int:id>/actualizar', methods=['PUT', 'POST'])
def actualizar_producto(id):
    """Actualizar un producto existente"""
    try:
        producto = Producto.query.get(id)
        if not producto:
            return jsonify({'error': 'Producto no encontrado'}), 404
        
        datos = request.get_json() if request.is_json else request.form.to_dict()
        
        # Actualizar campos
        if 'nombre' in datos:
            producto.nombre = datos['nombre']
        if 'descripcion' in datos:
            producto.descripcion = datos['descripcion']
        if 'precio' in datos:
            producto.precio = float(datos['precio'])
        if 'cantidad' in datos:
            producto.cantidad = int(datos['cantidad'])
        if 'categoria' in datos:
            producto.categoria = datos['categoria']
        
        db.session.commit()
        
        # Registrar en archivos
        gestor_archivos.guardar_en_txt(f"Producto actualizado: {producto.nombre}")
        
        return jsonify({
            'mensaje': 'Producto actualizado exitosamente',
            'producto': producto.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/productos/<int:id>/eliminar', methods=['DELETE', 'POST'])
def eliminar_producto(id):
    """Eliminar un producto"""
    try:
        producto = Producto.query.get(id)
        if not producto:
            return jsonify({'error': 'Producto no encontrado'}), 404
        
        nombre_producto = producto.nombre
        db.session.delete(producto)
        db.session.commit()
        
        # Registrar en archivos
        gestor_archivos.guardar_en_txt(f"Producto eliminado: {nombre_producto}")
        
        return jsonify({'mensaje': 'Producto eliminado exitosamente'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/producto/form', methods=['GET', 'POST'])
def formulario_producto():
    """Formulario para crear/editar productos"""
    if request.method == 'POST':
        try:
            nombre = request.form.get('nombre')
            descripcion = request.form.get('descripcion')
            precio = request.form.get('precio')
            cantidad = request.form.get('cantidad')
            categoria = request.form.get('categoria')
            
            # Manejar imagen
            imagen_path = None
            if 'imagen' in request.files:
                file = request.files['imagen']
                if file.filename != '':
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.root_path, 'static', 'images', filename)
                    file.save(file_path)
                    imagen_path = f'images/{filename}'
            
            nuevo_producto = Producto(
                nombre=nombre,
                descripcion=descripcion,
                precio=float(precio),
                cantidad=int(cantidad),
                categoria=categoria,
                imagen=imagen_path
            )
            
            db.session.add(nuevo_producto)
            db.session.commit()
            
            # Guardar en archivos
            producto_dict = nuevo_producto.to_dict()
            gestor_archivos.guardar_en_json(producto_dict)
            gestor_archivos.guardar_en_csv(producto_dict)
            gestor_archivos.guardar_en_txt(f"Nuevo producto: {nombre} - ${precio}")
            
            return redirect(url_for('formulario_producto'))
        except Exception as e:
            print(f"Error al crear producto: {e}")
            return redirect(url_for('formulario_producto'))
    
    productos = Producto.query.all()
    return render_template('producto_form.html', productos=productos)


# ===================== MANEJO DE ERRORES =====================

@app.errorhandler(404)
def page_not_found(error):
    """Página de error 404 - No encontrado"""
    return f"""
    <html>
        <head>
            <title>Error 404</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background: linear-gradient(135deg, #2c3e50, #3498db);
                    color: white;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }}
                .error-container {{
                    text-align: center;
                    padding: 40px;
                }}
                h1 {{
                    font-size: 4em;
                    margin: 0 0 20px 0;
                }}
                p {{
                    font-size: 1.2em;
                    margin: 10px 0;
                }}
                a {{
                    display: inline-block;
                    margin-top: 30px;
                    padding: 12px 30px;
                    background-color: #e74c3c;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                    font-weight: bold;
                    transition: background-color 0.3s;
                }}
                a:hover {{
                    background-color: #c0392b;
                }}
            </style>
        </head>
        <body>
            <div class="error-container">
                <h1>404</h1>
                <p>Página No Encontrada</p>
                <p>Lo sentimos, la página que buscas no existe.</p>
                <a href="/">Volver al Inicio</a>
            </div>
        </body>
    </html>
    """, 404


@app.errorhandler(500)
def internal_server_error(error):
    """Página de error 500 - Error interno del servidor"""
    return f"""
    <html>
        <head>
            <title>Error 500</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background: linear-gradient(135deg, #2c3e50, #e74c3c);
                    color: white;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }}
                .error-container {{
                    text-align: center;
                    padding: 40px;
                }}
                h1 {{
                    font-size: 4em;
                    margin: 0 0 20px 0;
                }}
                p {{
                    font-size: 1.2em;
                    margin: 10px 0;
                }}
                a {{
                    display: inline-block;
                    margin-top: 30px;
                    padding: 12px 30px;
                    background-color: #3498db;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                    font-weight: bold;
                    transition: background-color 0.3s;
                }}
                a:hover {{
                    background-color: #2980b9;
                }}
            </style>
        </head>
        <body>
            <div class="error-container">
                <h1>500</h1>
                <p>Error Interno del Servidor</p>
                <p>Algo salió mal. Por favor, intenta más tarde.</p>
                <a href="/">Volver al Inicio</a>
            </div>
        </body>
    </html>
    """, 500


# ===================== RUTAS DE ARCHIVOS ESTÁTICOS =====================

@app.route('/static/<path:filename>')
def static_files(filename):
    # Forzar el tipo MIME correcto para CSS
    if filename.endswith('.css'):
        return send_from_directory('static', filename, mimetype='text/css')
    return send_from_directory('static', filename)


# ===================== PUNTO DE ENTRADA =====================

if __name__ == '__main__':
    # Ejecutar la aplicación
    print("=" * 50)
    print("[INICIO] Tienda Virtual Flask")
    print("=" * 50)
    print("[INFO] Accede a: http://localhost:5000")
    print("=" * 50)
    app.run(
        host='localhost',
        port=5000,
        debug=True
    )
