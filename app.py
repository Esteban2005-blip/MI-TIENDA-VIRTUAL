

# ===== INICIO DE IMPORTS Y CONFIGURACIÓN ========== 
import os
from fpdf import FPDF
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from models import User
from inventario.productos import (
    obtener_productos as obtener_productos_db,
    obtener_producto_por_id,
    crear_producto as crear_producto_db,
    actualizar_producto as actualizar_producto_db,
    eliminar_producto as eliminar_producto_db
)
from inventario.inventario import GestorArchivos
from forms.producto_form import ProductoForm

# Función de conexión MySQL
def get_mysql_connection():
    return mysql.connector.connect(
        host=os.environ.get('MYSQL_HOST', 'localhost'),
        user=os.environ.get('MYSQL_USER', 'root'),
        password=os.environ.get('MYSQL_PASSWORD', ''),
        database=os.environ.get('MYSQL_DATABASE', 'tienda_virtual'),
        port=int(os.environ.get('MYSQL_PORT', 3306))
    )

# ========== CONFIGURACIÓN FLASK Y EXTENSIONES ========== 
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = os.environ.get('SECRET_KEY', 'devkey')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

gestor_archivos = GestorArchivos()


# ========== FIN DE CONFIGURACIÓN INICIAL ========== 

# ===================== LOGIN =====================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.get_by_email(email)
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Inicio de sesión exitoso', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Credenciales incorrectas', 'danger')
    return render_template('login.html')

# ===================== FIN LOGIN =====================


# ===================== REPORTE PDF DE PRODUCTOS =====================
@app.route('/productos/reporte/pdf')
@login_required
def reporte_productos_pdf():
    productos = obtener_productos_db()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Reporte de Productos', ln=True, align='C')
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(20, 10, 'ID', 1)
    pdf.cell(50, 10, 'Nombre', 1)
    pdf.cell(30, 10, 'Precio', 1)
    pdf.cell(20, 10, 'Stock', 1)
    pdf.cell(40, 10, 'Categoría', 1)
    pdf.ln()
    pdf.set_font('Arial', '', 12)
    for p in productos:
        pdf.cell(20, 10, str(p['id']), 1)
        pdf.cell(50, 10, str(p['nombre']), 1)
        pdf.cell(30, 10, str(p['precio']), 1)
        pdf.cell(20, 10, str(p['cantidad']), 1)
        pdf.cell(40, 10, str(p['categoria']), 1)
        pdf.ln()
    response = app.response_class(pdf.output(dest='S').encode('latin1'), mimetype='application/pdf')
    response.headers['Content-Disposition'] = 'attachment; filename=reporte_productos.pdf'
    return response


# ...existing code...



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

# ===================== CRUD USUARIOS MYSQL =====================
@app.route('/usuarios')
def mostrar_usuarios():
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/usuarios/agregar', methods=['POST'])
def agregar_usuario():
    nombre = request.form['nombre']
    email = request.form['email']
    password = generate_password_hash(request.form['password'])
    conn = get_mysql_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)", (nombre, email, password))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Usuario agregado correctamente')
    return redirect(url_for('mostrar_usuarios'))

@app.route('/usuarios/eliminar/<int:id_usuario>')
def eliminar_usuario(id_usuario):
    conn = get_mysql_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_usuario,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Usuario eliminado')
    return redirect(url_for('mostrar_usuarios'))

@app.route('/usuarios/editar/<int:id_usuario>', methods=['POST'])
def editar_usuario(id_usuario):
    nombre = request.form['nombre']
    email = request.form['email']
    conn = get_mysql_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET nombre=%s, email=%s WHERE id_usuario=%s", (nombre, email, id_usuario))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Usuario actualizado')
    return redirect(url_for('mostrar_usuarios'))

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
        if not producto:
            return jsonify({'error': 'Producto no encontrado'}), 404
        eliminar_producto_db(id)
        return jsonify({'mensaje': 'Producto eliminado exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ===================== FORMULARIO PRODUCTO =====================
@app.route('/productos/formulario', methods=['GET', 'POST'])
@login_required
def formulario_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        crear_producto_db(
            form.nombre.data,
            form.descripcion.data,
            form.precio.data,
            form.cantidad.data,
            form.categoria.data,
            None
        )
        flash('Producto creado exitosamente', 'success')
        return redirect(url_for('productos'))
    return render_template('producto_form.html', form=form)


# ===================== LOGOUT =====================
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada', 'info')
    return redirect(url_for('login'))


# ===================== REGISTRO =====================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        conn = get_mysql_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
            (nombre, email, password)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash('Usuario registrado. Inicia sesión.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)


