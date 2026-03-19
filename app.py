


from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash, send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import User
from db import get_connection
from inventario.productos import (
    obtener_productos as obtener_productos_db, obtener_producto_por_id, crear_producto as crear_producto_db, actualizar_producto as actualizar_producto_db, eliminar_producto as eliminar_producto_db
)
from inventario.inventario import GestorArchivos
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

# Crear instancia de la aplicación Flask
app = Flask(__name__)

# Configuración de la aplicación
app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

# clave secreta para sesiones
app.secret_key = os.environ.get('SECRET_KEY', 'devkey')

# Inicializar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Función para cargar usuario
@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

# Crear instancia del gestor de archivos
gestor_archivos = GestorArchivos()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.get_by_email(email)
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Sesión iniciada correctamente.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Email o contraseña incorrectos.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada.', 'info')
    return redirect(url_for('login'))
    print('PRODUCTOS ENVIADOS AL FORMULARIO:', productos)

# Crear instancia de la aplicación Flask
app = Flask(__name__)



# Configuración de la aplicación
app.config['DEBUG'] = True


# clave secreta para sesiones
app.secret_key = os.environ.get('SECRET_KEY', 'devkey')




# Inicializar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Función para cargar usuario
@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

# Crear instancia del gestor de archivos
gestor_archivos = GestorArchivos()
 
    # ===================== CARGA AUTOMÁTICA DE PRODUCTOS DEMO =====================
    # ===================== AUTENTICACIÓN ADMIN (OBSOLETO, USAR FLASK-LOGIN) =====================
    # Las funciones de autenticación admin serán reemplazadas por Flask-Login
def cargar_productos_demo():
    # Cargar productos demo solo si la tabla está vacía
    if not obtener_productos_db():
        productos_demo = [
            {'nombre': 'Laptop Dell XPS', 'descripcion': 'Laptop premium de alto rendimiento.', 'precio': 1999.99, 'cantidad': 5, 'categoria': 'Computadoras', 'imagen': 'images/laptop_dell_xps.jpg'},
            {'nombre': 'Laptop Asus TUF', 'descripcion': 'Laptop gamer resistente.', 'precio': 1499.99, 'cantidad': 3, 'categoria': 'Computadoras', 'imagen': 'images/laptop_asus_tuf.jpg'},
            {'nombre': 'Monitor LG 27"', 'descripcion': 'Monitor IPS de 27 pulgadas.', 'precio': 399.99, 'cantidad': 7, 'categoria': 'Electrónica', 'imagen': 'images/monitor_lg_27.jpg'},
            {'nombre': 'Mouse Logitech MX Master', 'descripcion': 'Mouse inalámbrico ergonómico.', 'precio': 99.99, 'cantidad': 10, 'categoria': 'Accesorios', 'imagen': 'images/mouse_logitech_mx_master.jpg'},
            {'nombre': 'Teclado RGB', 'descripcion': 'Teclado mecánico con retroiluminación.', 'precio': 89.99, 'cantidad': 8, 'categoria': 'Accesorios', 'imagen': 'images/teclado_rgb.jpg'},
            {'nombre': 'Teléfono Samsung S24', 'descripcion': 'Smartphone de última generación.', 'precio': 1299.99, 'cantidad': 4, 'categoria': 'Móviles', 'imagen': 'images/telefono_samsung_s24.jpg'},
            {'nombre': 'Audífonos Sony WH1000', 'descripcion': 'Audífonos inalámbricos con cancelación de ruido.', 'precio': 349.99, 'cantidad': 6, 'categoria': 'Electrónica', 'imagen': 'images/headphones_sony_wh1000.jpg'}
        ]
        for prod in productos_demo:
            crear_producto_db(
                prod['nombre'], prod['descripcion'], prod['precio'], prod['cantidad'], prod['categoria'], prod['imagen']
            )

cargar_productos_demo()
@app.route('/agregar_productos_demo')
def agregar_productos_demo():
    productos_demo = [
        {
            'nombre': 'Laptop Dell XPS',
            'descripcion': 'Laptop premium de alto rendimiento.',
            'precio': 1999.99,
            'cantidad': 5,
            'categoria': 'Computadoras',
            'imagen': 'images/laptop_dell_xps.jpg'
        },
        {
            'nombre': 'Laptop Asus TUF',
            'descripcion': 'Laptop gamer resistente.',
            'precio': 1499.99,
            'cantidad': 3,
            'categoria': 'Computadoras',
            'imagen': 'images/laptop_asus_tuf.jpg'
        },
        {
            'nombre': 'Monitor LG 27"',
            'descripcion': 'Monitor IPS de 27 pulgadas.',
            'precio': 399.99,
            'cantidad': 7,
            'categoria': 'Electrónica',
            'imagen': 'images/monitor_lg_27.jpg'
        },
        {
            'nombre': 'Mouse Logitech MX Master',
            'descripcion': 'Mouse inalámbrico ergonómico.',
            'precio': 99.99,
            'cantidad': 10,
            'categoria': 'Accesorios',
            'imagen': 'images/mouse_logitech_mx_master.jpg'
        },
        {
            'nombre': 'Teclado RGB',
            'descripcion': 'Teclado mecánico con retroiluminación.',
            'precio': 89.99,
            'cantidad': 8,
            'categoria': 'Accesorios',
            'imagen': 'images/teclado_rgb.jpg'
        },
        {
            'nombre': 'Teléfono Samsung S24',
            'descripcion': 'Smartphone de última generación.',
            'precio': 1299.99,
            'cantidad': 4,
            'categoria': 'Móviles',
            'imagen': 'images/telefono_samsung_s24.jpg'
        },
        {
            'nombre': 'Audífonos Sony WH1000',
            'descripcion': 'Audífonos inalámbricos con cancelación de ruido.',
            'precio': 349.99,
            'cantidad': 6,
            'categoria': 'Electrónica',
            'imagen': 'images/headphones_sony_wh1000.jpg'
        }
    ]
    for prod in productos_demo:
        productos = obtener_productos()
        existe = any(p['nombre'] == prod['nombre'] for p in productos)
        if not existe:
            crear_producto_db(
                prod['nombre'], prod['descripcion'], prod['precio'], prod['cantidad'], prod['categoria'], prod['imagen']
            )
    flash('Productos demo agregados.', 'success')
    return redirect(url_for('productos'))

# Las rutas de login y logout serán reemplazadas más adelante por las de Flask-Login



# ===================== AUTENTICACIÓN DE USUARIOS =====================
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

# Ruta de registro de usuario
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE email = %s', (email,))
        existe = cursor.fetchone()
        if existe:
            flash('El email ya está registrado.', 'danger')
            cursor.close()
            conn.close()
            return redirect(url_for('register'))
        cursor.execute('INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)', (nombre, email, hashed_password))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Usuario registrado correctamente. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# Ruta de login de usuario
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.get_by_email(email)
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Sesión iniciada correctamente.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Email o contraseña incorrectos.', 'danger')
    return render_template('login.html')

# Ruta de logout de usuario
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada.', 'info')
    return redirect(url_for('login'))



@app.route('/')
@login_required
def index():
    # Página de inicio - Dashboard principal
    return render_template('index.html')




@app.route('/about')
@login_required
def about():
    # Página Acerca de - Información de la empresa
    return render_template('about.html')




@app.route('/productos')
@login_required
def productos():
    # Página de Productos - Catálogo de productos con búsqueda
    # parámetros de filtrado
    q = request.args.get('q', '').strip()
    categoria = request.args.get('categoria', '').strip()

    # construir consulta base
    productos = obtener_productos_db()
    if q:
        productos = [p for p in productos if q.lower() in p['nombre'].lower()]
    if categoria and categoria != '':
        productos = [p for p in productos if p['categoria'] == categoria]
    return render_template('productos.html', productos=productos, q=q, categoria=categoria)




@app.route('/clientes')
@login_required
def clientes():
    # Página de Clientes - Gestión de clientes
    return render_template('clientes.html')


# ===================== CARRITO =====================


@app.route('/carrito')
def ver_carrito():
    # Mostrar los productos agregados al carrito
    items = session.get('carrito', [])
    productos = []
    for prod_id in items:
        p = obtener_producto_por_id(prod_id)
        if p:
            productos.append(p)
    total = sum(p['precio'] for p in productos)
    return render_template('carrito.html', productos=productos, total=total)


@app.route('/carrito/agregar/<int:prod_id>')
def agregar_carrito(prod_id):
    # Agregar un producto al carrito en sesión
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
@login_required
def facturas():
    # Página de Facturas - Gestión de facturas
    return render_template('facturas.html')



@app.route('/contacto')
def contacto():
    # Página de Contacto - Información de contacto y formulario
    return render_template('contacto.html')


# ===================== RUTAS DE PERSISTENCIA DE DATOS =====================

@app.route('/datos')
def datos():
    # Página que muestra datos en diferentes formatos
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
    # Obtener todos los productos de la base de datos
    try:
        productos = obtener_productos_db()
        return jsonify(productos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/productos/<int:id>', methods=['GET'])
def obtener_producto(id):
    # Obtener un producto específico
    try:
        producto = obtener_producto_por_id(id)
        if not producto:
            return jsonify({'error': 'Producto no encontrado'}), 404
        return jsonify(producto)
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/api/productos/crear', methods=['POST'])
@login_required
def crear_producto():
    try:
        datos = request.get_json() if request.is_json else request.form.to_dict()
        nombre = datos.get('nombre')
        descripcion = datos.get('descripcion')
        precio = datos.get('precio')
        cantidad = datos.get('cantidad')
        categoria = datos.get('categoria')
        imagen = datos.get('imagen')
        crear_producto_db(nombre, descripcion, precio, cantidad, categoria, imagen)
        return jsonify({'mensaje': 'Producto creado exitosamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/productos/<int:id>/actualizar', methods=['PUT', 'POST'])
def actualizar_producto(id):
    # Actualizar un producto existente
    try:
        datos = request.get_json() if request.is_json else request.form.to_dict()
        nombre = datos.get('nombre')
        descripcion = datos.get('descripcion')
        precio = datos.get('precio')
        cantidad = datos.get('cantidad')
        categoria = datos.get('categoria')
        imagen = datos.get('imagen')
        actualizar_producto_db(id, nombre, descripcion, precio, cantidad, categoria, imagen)
        gestor_archivos.guardar_en_txt(f"Producto actualizado: {nombre}")
        return jsonify({'mensaje': 'Producto actualizado exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/productos/<int:id>/eliminar', methods=['DELETE', 'POST'])
def eliminar_producto(id):
    # Eliminar un producto
    try:
        producto = obtener_producto_por_id(id)
        # Aquí va la lógica para eliminar el producto
        # ...
    except Exception as e:
        return jsonify({'error': str(e)}), 500
"""
"""

import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from db import get_connection
from inventario.productos import (
    obtener_productos as obtener_productos_db,
    obtener_producto_por_id,
    crear_producto as crear_producto_db,
    actualizar_producto as actualizar_producto_db,
    eliminar_producto as eliminar_producto_db
)
from inventario.inventario import GestorArchivos

# Configuración Flask
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = os.environ.get('SECRET_KEY', 'devkey')

# Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

gestor_archivos = GestorArchivos()

# ===================== AUTENTICACIÓN DE USUARIOS =====================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE email = %s', (email,))
        existe = cursor.fetchone()
        if existe:
            flash('El email ya está registrado.', 'danger')
            cursor.close()
            conn.close()
            return redirect(url_for('register'))
        cursor.execute('INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)', (nombre, email, hashed_password))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Usuario registrado correctamente. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.get_by_email(email)
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Sesión iniciada correctamente.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Email o contraseña incorrectos.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada.', 'info')
    return redirect(url_for('login'))

# ===================== CARGA AUTOMÁTICA DE PRODUCTOS DEMO =====================
def cargar_productos_demo():
    if not obtener_productos_db():
        productos_demo = [
            {'nombre': 'Laptop Dell XPS', 'descripcion': 'Laptop premium de alto rendimiento.', 'precio': 1999.99, 'cantidad': 5, 'categoria': 'Computadoras', 'imagen': 'images/laptop_dell_xps.jpg'},
            {'nombre': 'Laptop Asus TUF', 'descripcion': 'Laptop gamer resistente.', 'precio': 1499.99, 'cantidad': 3, 'categoria': 'Computadoras', 'imagen': 'images/laptop_asus_tuf.jpg'},
            {'nombre': 'Monitor LG 27"', 'descripcion': 'Monitor IPS de 27 pulgadas.', 'precio': 399.99, 'cantidad': 7, 'categoria': 'Electrónica', 'imagen': 'images/monitor_lg_27.jpg'},
            {'nombre': 'Mouse Logitech MX Master', 'descripcion': 'Mouse inalámbrico ergonómico.', 'precio': 99.99, 'cantidad': 10, 'categoria': 'Accesorios', 'imagen': 'images/mouse_logitech_mx_master.jpg'},
            {'nombre': 'Teclado RGB', 'descripcion': 'Teclado mecánico con retroiluminación.', 'precio': 89.99, 'cantidad': 8, 'categoria': 'Accesorios', 'imagen': 'images/teclado_rgb.jpg'},
            {'nombre': 'Teléfono Samsung S24', 'descripcion': 'Smartphone de última generación.', 'precio': 1299.99, 'cantidad': 4, 'categoria': 'Móviles', 'imagen': 'images/telefono_samsung_s24.jpg'},
            {'nombre': 'Audífonos Sony WH1000', 'descripcion': 'Audífonos inalámbricos con cancelación de ruido.', 'precio': 349.99, 'cantidad': 6, 'categoria': 'Electrónica', 'imagen': 'images/headphones_sony_wh1000.jpg'}
        ]
        for prod in productos_demo:
            crear_producto_db(
                prod['nombre'], prod['descripcion'], prod['precio'], prod['cantidad'], prod['categoria'], prod['imagen']
            )

cargar_productos_demo()

# ===================== RUTAS PRINCIPALES =====================
@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/about')
@login_required
def about():
    return render_template('about.html')

@app.route('/productos')
@login_required
def productos():
    q = request.args.get('q', '').strip()
    categoria = request.args.get('categoria', '').strip()
    productos = obtener_productos_db()
    if q:
        productos = [p for p in productos if q.lower() in p['nombre'].lower()]
    if categoria:
        productos = [p for p in productos if p['categoria'] == categoria]
    return render_template('productos.html', productos=productos, q=q, categoria=categoria)

@app.route('/clientes')
@login_required
def clientes():
    return render_template('clientes.html')

@app.route('/facturas')
@login_required
def facturas():
    return render_template('facturas.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

# ===================== CARRITO =====================
@app.route('/carrito')
def ver_carrito():
    items = session.get('carrito', [])
    productos = []
    for prod_id in items:
        p = obtener_producto_por_id(prod_id)
        if p:
            productos.append(p)
    total = sum(p['precio'] for p in productos)
    return render_template('carrito.html', productos=productos, total=total)

@app.route('/carrito/agregar/<int:prod_id>')
def agregar_carrito(prod_id):
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

# ===================== RUTAS DE PERSISTENCIA DE DATOS =====================
@app.route('/datos')
def datos():
    datos_txt = gestor_archivos.leer_txt()
    datos_json = gestor_archivos.leer_json()
    datos_csv = gestor_archivos.leer_csv()
    return render_template('datos.html', datos_txt=datos_txt, datos_json=datos_json, datos_csv=datos_csv)

# ===================== CRUD PRODUCTOS API =====================
@app.route('/api/productos', methods=['GET'])
def obtener_productos():
    try:
        productos = obtener_productos_db()
        return jsonify(productos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/productos/<int:id>', methods=['GET'])
def obtener_producto(id):
    try:
        producto = obtener_producto_por_id(id)
        if not producto:
            return jsonify({'error': 'Producto no encontrado'}), 404
        return jsonify(producto)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/productos/crear', methods=['POST'])
@login_required
def crear_producto():
    try:
        datos = request.get_json() if request.is_json else request.form.to_dict()
        nombre = datos.get('nombre')
        descripcion = datos.get('descripcion')
        precio = datos.get('precio')
        cantidad = datos.get('cantidad')
        categoria = datos.get('categoria')
        imagen = datos.get('imagen')
        crear_producto_db(nombre, descripcion, precio, cantidad, categoria, imagen)
        return jsonify({'mensaje': 'Producto creado exitosamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/productos/<int:id>/actualizar', methods=['PUT', 'POST'])
def actualizar_producto(id):
    try:
        datos = request.get_json() if request.is_json else request.form.to_dict()
        nombre = datos.get('nombre')
        descripcion = datos.get('descripcion')
        precio = datos.get('precio')
        cantidad = datos.get('cantidad')
        categoria = datos.get('categoria')
        imagen = datos.get('imagen')
        actualizar_producto_db(id, nombre, descripcion, precio, cantidad, categoria, imagen)
        gestor_archivos.guardar_en_txt(f"Producto actualizado: {nombre}")
        return jsonify({'mensaje': 'Producto actualizado exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/productos/<int:id>/eliminar', methods=['DELETE', 'POST'])
def eliminar_producto(id):
    try:
        producto = obtener_producto_por_id(id)
        if not producto:
            return jsonify({'error': 'Producto no encontrado'}), 404
        nombre_producto = producto['nombre']
        eliminar_producto_db(id)
        gestor_archivos.guardar_en_txt(f"Producto eliminado: {nombre_producto}")
        return jsonify({'mensaje': 'Producto eliminado exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/producto/form', methods=['GET', 'POST'])
def formulario_producto():
    if request.method == 'POST':
        try:
            nombre = request.form.get('nombre')
            descripcion = request.form.get('descripcion')
            precio = request.form.get('precio')
            cantidad = request.form.get('cantidad')
            categoria = request.form.get('categoria')
            imagen_path = None
            if 'imagen' in request.files:
                file = request.files['imagen']
                if file.filename != '':
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.root_path, 'static', 'images', filename)
                    file.save(file_path)
                    imagen_path = f'images/{filename}'
            crear_producto_db(nombre, descripcion, precio, cantidad, categoria, imagen_path)
            producto_dict = {
                'nombre': nombre,
                'descripcion': descripcion,
                'precio': float(precio),
                'cantidad': int(cantidad),
                'categoria': categoria,
                'imagen': imagen_path
            }
            gestor_archivos.guardar_en_json(producto_dict)
            gestor_archivos.guardar_en_csv(producto_dict)
            gestor_archivos.guardar_en_txt(f"Nuevo producto: {nombre} - ${precio}")
            return redirect(url_for('formulario_producto'))
        except Exception as e:
            print(f"Error al crear producto: {e}")
            return redirect(url_for('formulario_producto'))
    productos = obtener_productos_db()
    return render_template('producto_form.html', productos=productos)

# ===================== MANEJO DE ERRORES =====================
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    import traceback
    print("==== ERROR 500 ====")
    print(error)
    traceback.print_exc()
    return render_template('500.html'), 500

# ===================== PUNTO DE ENTRADA =====================
if __name__ == '__main__':
    print("=" * 50)
    print("[INICIO] Tienda Virtual Flask")
    print("=" * 50)
    print("[INFO] Accede a: http://localhost:5000")
    print("=" * 50)
    app.run(host='localhost', port=5000, debug=True)
