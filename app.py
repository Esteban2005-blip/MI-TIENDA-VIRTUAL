

# ===== INICIO DE IMPORTS Y CONFIGURACIÓN ========== 
import os
import traceback
from collections import Counter
from fpdf import FPDF
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
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
from forms.producto_form import ProductoForm

# Función de conexión MySQL
def get_mysql_connection():
    return get_connection()


def ensure_facturas_table(cursor):
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS facturas (
            id_factura      INT AUTO_INCREMENT PRIMARY KEY,
            id_cliente      INT NOT NULL,
            fecha_emision   DATETIME      DEFAULT CURRENT_TIMESTAMP,
            total           DECIMAL(10,2) NOT NULL DEFAULT 0.00,
            metodo_pago     VARCHAR(50),
            estado          VARCHAR(30)   NOT NULL DEFAULT 'Pagada',
            direccion_envio VARCHAR(255),
            nota            VARCHAR(255),
            items_resumen   TEXT
        )
        """
    )


def pdf_safe_text(value):
    text = str(value or '')
    return text.encode('latin-1', errors='replace').decode('latin-1')

# ========== CONFIGURACIÓN FLASK Y EXTENSIONES ========== 
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = os.environ.get('SECRET_KEY', 'devkey')

# Render usa proxy reverso; esto preserva esquema/host real para sesión y CSRF.
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

is_production = os.environ.get('RENDER') == 'true' or os.environ.get('FLASK_ENV') == 'production'
app.config['SESSION_COOKIE_SECURE'] = is_production
app.config['REMEMBER_COOKIE_SECURE'] = is_production
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

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


@app.route('/clientes/reporte/pdf')
@login_required
def reporte_clientes_pdf():
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_cliente, nombre, email, telefono, ciudad, total_compras FROM clientes ORDER BY fecha_registro DESC")
    clientes = cursor.fetchall()
    cursor.close()
    conn.close()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Reporte de Clientes', ln=True, align='C')
    pdf.ln(6)
    pdf.set_font('Arial', 'B', 9)
    pdf.cell(15, 8, 'ID', 1)
    pdf.cell(35, 8, 'Nombre', 1)
    pdf.cell(45, 8, 'Email', 1)
    pdf.cell(28, 8, 'Telefono', 1)
    pdf.cell(35, 8, 'Ciudad', 1)
    pdf.cell(25, 8, 'Compras', 1)
    pdf.ln()

    pdf.set_font('Arial', '', 8)
    for c in clientes:
        pdf.cell(15, 8, str(c.get('id_cliente', '')), 1)
        pdf.cell(35, 8, str(c.get('nombre', ''))[:20], 1)
        pdf.cell(45, 8, str(c.get('email', ''))[:28], 1)
        pdf.cell(28, 8, str(c.get('telefono') or '-')[:16], 1)
        pdf.cell(35, 8, str(c.get('ciudad') or '-')[:20], 1)
        pdf.cell(25, 8, str(c.get('total_compras') or 0), 1)
        pdf.ln()

    response = app.response_class(pdf.output(dest='S').encode('latin1'), mimetype='application/pdf')
    response.headers['Content-Disposition'] = 'attachment; filename=reporte_clientes.pdf'
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
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clientes ORDER BY fecha_registro DESC")
    clientes_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('clientes.html', clientes=clientes_list)

@app.route('/clientes/agregar', methods=['POST'])
@login_required
def agregar_cliente():
    nombre   = request.form['nombre']
    email    = request.form['email']
    telefono = request.form.get('telefono', '')
    ciudad   = request.form.get('ciudad', '')
    conn = get_mysql_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO clientes (nombre, email, telefono, ciudad) VALUES (%s, %s, %s, %s)",
        (nombre, email, telefono, ciudad)
    )
    conn.commit()
    cursor.close()
    conn.close()
    flash('Cliente agregado correctamente', 'success')
    return redirect(url_for('clientes'))

@app.route('/clientes/eliminar/<int:id_cliente>')
@login_required
def eliminar_cliente(id_cliente):
    conn = get_mysql_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id_cliente = %s", (id_cliente,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Cliente eliminado', 'info')
    return redirect(url_for('clientes'))


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


@app.route('/carrito/finalizar', methods=['POST'])
@login_required
def finalizar_compra():
    items = session.get('carrito', [])
    if not items:
        flash('Tu carrito esta vacio.', 'warning')
        return redirect(url_for('ver_carrito'))

    nombre = request.form.get('nombre', '').strip() or current_user.nombre
    email = request.form.get('email', '').strip() or current_user.email
    telefono = request.form.get('telefono', '').strip()
    ciudad = request.form.get('ciudad', '').strip()
    direccion = request.form.get('direccion', '').strip()
    metodo_pago = request.form.get('metodo_pago', '').strip()
    nota = request.form.get('nota', '').strip()

    if not all([nombre, email, telefono, ciudad, direccion, metodo_pago]):
        flash('Completa todos los datos obligatorios para finalizar la compra.', 'warning')
        return redirect(url_for('ver_carrito'))

    productos_compra = []
    for prod_id in items:
        producto = obtener_producto_por_id(prod_id)
        if producto:
            productos_compra.append(producto)

    if not productos_compra:
        flash('No se encontraron productos validos para generar la factura.', 'warning')
        return redirect(url_for('ver_carrito'))

    total_compra = sum(float(p.get('precio') or 0) for p in productos_compra)
    conteo_ids = Counter(p.get('id') for p in productos_compra if p.get('id') is not None)
    resumen_items = []
    for producto_id, cantidad in conteo_ids.items():
        prod = next((p for p in productos_compra if p.get('id') == producto_id), None)
        if prod:
            resumen_items.append(f"{prod.get('nombre', 'Producto')} x{cantidad}")
    items_resumen = ' | '.join(resumen_items)

    conn = None
    cursor = None
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        ensure_facturas_table(cursor)

        # Mantiene compatibilidad con bases que todavia no tienen la columna direccion.
        cursor.execute("SHOW COLUMNS FROM clientes LIKE 'direccion'")
        tiene_direccion = cursor.fetchone() is not None

        # Registra o actualiza al cliente asociado al usuario autenticado.
        cursor.execute(
            "SELECT id_cliente, total_compras FROM clientes WHERE email = %s",
            (email,)
        )
        cliente = cursor.fetchone()
        id_cliente = None

        if cliente:
            id_cliente = cliente['id_cliente']
            total_actual = int(cliente.get('total_compras') or 0)
            if tiene_direccion:
                cursor.execute(
                    "UPDATE clientes SET nombre = %s, telefono = %s, ciudad = %s, direccion = %s, total_compras = %s WHERE id_cliente = %s",
                    (nombre, telefono, ciudad, direccion, total_actual + 1, cliente['id_cliente'])
                )
            else:
                cursor.execute(
                    "UPDATE clientes SET nombre = %s, telefono = %s, ciudad = %s, total_compras = %s WHERE id_cliente = %s",
                    (nombre, telefono, ciudad, total_actual + 1, cliente['id_cliente'])
                )
        else:
            if tiene_direccion:
                cursor.execute(
                    "INSERT INTO clientes (nombre, email, telefono, ciudad, direccion, total_compras) VALUES (%s, %s, %s, %s, %s, %s)",
                    (nombre, email, telefono, ciudad, direccion, 1)
                )
            else:
                cursor.execute(
                    "INSERT INTO clientes (nombre, email, telefono, ciudad, total_compras) VALUES (%s, %s, %s, %s, %s)",
                    (nombre, email, telefono, ciudad, 1)
                )
            id_cliente = cursor.lastrowid

        cursor.execute(
            """
            INSERT INTO facturas (
                id_cliente, total, metodo_pago, estado, direccion_envio, nota, items_resumen
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (id_cliente, total_compra, metodo_pago, 'Pagada', direccion, nota or None, items_resumen)
        )

        conn.commit()
        session.pop('carrito', None)
        flash(f'Compra finalizada con exito. Factura #{cursor.lastrowid} generada. Metodo de pago: {metodo_pago}.', 'success')
        if nota:
            flash(f'Nota registrada: {nota}', 'info')
        return redirect(url_for('facturas'))
    except mysql.connector.Error as e:
        if conn is not None:
            conn.rollback()
        print(f"Error al finalizar compra: {e}")
        flash('No se pudo finalizar la compra por un error de base de datos.', 'danger')
        return redirect(url_for('ver_carrito'))
    except Exception as e:
        if conn is not None:
            conn.rollback()
        print(f"Error inesperado al finalizar compra: {e}")
        traceback.print_exc()
        flash('Ocurrio un error inesperado al generar la factura.', 'danger')
        return redirect(url_for('ver_carrito'))
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()



@app.route('/facturas')
@login_required
def facturas():
    conn = None
    cursor = None
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        ensure_facturas_table(cursor)
        cursor.execute(
            """
            SELECT
                f.id_factura,
                f.fecha_emision,
                f.total,
                f.estado,
                f.metodo_pago,
                c.nombre AS cliente_nombre
            FROM facturas f
            LEFT JOIN clientes c ON c.id_cliente = f.id_cliente
            ORDER BY f.fecha_emision DESC
            """
        )
        facturas_list = cursor.fetchall()
        total_facturas = len(facturas_list)
        ingresos_totales = sum(float(f.get('total') or 0) for f in facturas_list)
        pendientes = sum(1 for f in facturas_list if str(f.get('estado') or '').lower() != 'pagada')
        return render_template(
            'facturas.html',
            facturas=facturas_list,
            total_facturas=total_facturas,
            ingresos_totales=ingresos_totales,
            pendientes=pendientes
        )
    except mysql.connector.Error as e:
        print(f"Error al consultar facturas: {e}")
        flash('No se pudo cargar la lista de facturas.', 'danger')
        return render_template('facturas.html', facturas=[], total_facturas=0, ingresos_totales=0, pendientes=0)
    except Exception as e:
        print(f"Error inesperado en facturas: {e}")
        traceback.print_exc()
        flash('Ocurrio un error inesperado al cargar facturas.', 'danger')
        return render_template('facturas.html', facturas=[], total_facturas=0, ingresos_totales=0, pendientes=0)
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


@app.route('/facturas/<int:id_factura>')
@login_required
def ver_factura(id_factura):
    conn = None
    cursor = None
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        ensure_facturas_table(cursor)
        cursor.execute(
            """
            SELECT
                f.id_factura,
                f.fecha_emision,
                f.total,
                f.estado,
                f.metodo_pago,
                f.direccion_envio,
                f.nota,
                f.items_resumen,
                c.nombre AS cliente_nombre,
                c.email AS cliente_email,
                c.telefono AS cliente_telefono,
                c.ciudad AS cliente_ciudad
            FROM facturas f
            LEFT JOIN clientes c ON c.id_cliente = f.id_cliente
            WHERE f.id_factura = %s
            """,
            (id_factura,)
        )
        factura = cursor.fetchone()
        if not factura:
            flash('Factura no encontrada.', 'warning')
            return redirect(url_for('facturas'))

        items = []
        if factura.get('items_resumen'):
            items = [item.strip() for item in factura['items_resumen'].split('|') if item.strip()]

        return render_template('factura_detalle.html', factura=factura, items=items)
    except mysql.connector.Error as e:
        print(f"Error al consultar factura: {e}")
        flash('No se pudo abrir la factura.', 'danger')
        return redirect(url_for('facturas'))
    except Exception as e:
        print(f"Error inesperado al abrir factura: {e}")
        traceback.print_exc()
        flash('Ocurrio un error inesperado al abrir la factura.', 'danger')
        return redirect(url_for('facturas'))
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


@app.route('/facturas/reporte/pdf')
@login_required
def reporte_facturas_pdf():
    conn = None
    cursor = None
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        ensure_facturas_table(cursor)
        cursor.execute(
            """
            SELECT
                f.id_factura,
                f.fecha_emision,
                f.total,
                f.estado,
                c.nombre AS cliente_nombre
            FROM facturas f
            LEFT JOIN clientes c ON c.id_cliente = f.id_cliente
            ORDER BY f.fecha_emision DESC
            """
        )
        facturas_list = cursor.fetchall()

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'Reporte de Facturas', ln=True, align='C')
        pdf.ln(6)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(24, 8, 'Factura', 1)
        pdf.cell(54, 8, 'Cliente', 1)
        pdf.cell(44, 8, 'Fecha', 1)
        pdf.cell(30, 8, 'Total', 1)
        pdf.cell(36, 8, 'Estado', 1)
        pdf.ln()

        pdf.set_font('Arial', '', 9)
        for f in facturas_list:
            fecha = str(f.get('fecha_emision') or '')
            pdf.cell(24, 8, pdf_safe_text(f"FAC-{f.get('id_factura')}"), 1)
            pdf.cell(54, 8, pdf_safe_text(str(f.get('cliente_nombre') or 'Sin cliente')[:30]), 1)
            pdf.cell(44, 8, pdf_safe_text(fecha[:19]), 1)
            pdf.cell(30, 8, pdf_safe_text(f"${float(f.get('total') or 0):.2f}"), 1)
            pdf.cell(36, 8, pdf_safe_text(str(f.get('estado') or '-')[:20]), 1)
            pdf.ln()

        response = app.response_class(pdf.output(dest='S').encode('latin1'), mimetype='application/pdf')
        response.headers['Content-Disposition'] = 'attachment; filename=reporte_facturas.pdf'
        return response
    except mysql.connector.Error as e:
        print(f"Error de base de datos al generar reporte PDF de facturas: {e}")
        flash('No se pudo generar el reporte PDF de facturas por un error de base de datos.', 'danger')
        return redirect(url_for('facturas'))
    except Exception as e:
        print(f"Error inesperado al generar reporte PDF de facturas: {e}")
        traceback.print_exc()
        flash('Ocurrio un error inesperado al generar el reporte PDF de facturas.', 'danger')
        return redirect(url_for('facturas'))
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()



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
    if request.method == 'POST':
        if form.validate_on_submit():
            nombre = form.nombre.data
            descripcion = form.descripcion.data
            precio = form.precio.data
            cantidad = form.cantidad.data
            categoria = form.categoria.data
        else:
            # Fallback para formularios HTML legacy sin campos WTForms alineados.
            nombre = request.form.get('nombre', '').strip()
            descripcion = request.form.get('descripcion', '').strip()
            precio = request.form.get('precio')
            cantidad = request.form.get('cantidad', request.form.get('stock', 0))
            categoria = request.form.get('categoria', '').strip()

        try:
            crear_producto_db(
                nombre,
                descripcion,
                precio,
                int(cantidad or 0),
                categoria,
                None
            )
            flash('Producto creado exitosamente', 'success')
            return redirect(url_for('formulario_producto'))
        except Exception as e:
            print(f"Error al crear producto desde formulario: {e}")
            flash('No se pudo crear el producto. Revisa los datos ingresados.', 'danger')

    productos = obtener_productos_db()
    return render_template('producto_form.html', form=form, productos=productos)


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
        nombre = request.form.get('nombre', '').strip()
        email = request.form.get('email', '').strip()
        raw_password = request.form.get('password', '')

        if not nombre or not email or not raw_password:
            flash('Todos los campos son obligatorios.', 'warning')
            return render_template('register.html')

        conn = None
        cursor = None
        try:
            conn = get_mysql_connection()
            cursor = conn.cursor(dictionary=True)

            # Evita error por correo duplicado y permite mostrar un mensaje amigable.
            cursor.execute("SELECT id_usuario FROM usuarios WHERE email = %s", (email,))
            if cursor.fetchone():
                flash('Ese correo ya está registrado. Usa otro o inicia sesión.', 'warning')
                return render_template('register.html')

            password = generate_password_hash(raw_password)
            cursor.execute(
                "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
                (nombre, email, password)
            )
            conn.commit()
            flash('Usuario registrado. Inicia sesión.', 'success')
            return redirect(url_for('login'))
        except mysql.connector.Error as e:
            print(f"Error en registro de usuario: {e}")
            if e.errno in (2002, 2003, 2005, 2013):
                flash('No hay conexión con MySQL. En Render, revisa MYSQL_HOST, MYSQL_PORT y que la base permita conexiones externas.', 'danger')
            elif e.errno == 1045:
                flash('MySQL rechazó el usuario/contraseña. Revisa MYSQL_USER y MYSQL_PASSWORD en Render.', 'danger')
            elif e.errno == 1049:
                flash('La base de datos no existe. Revisa MYSQL_DATABASE en Render.', 'danger')
            else:
                flash('No se pudo completar el registro por un error de base de datos.', 'danger')
            return render_template('register.html')
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)


