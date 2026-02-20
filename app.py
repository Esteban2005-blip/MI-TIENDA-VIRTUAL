"""
Aplicación Flask - Tienda Virtual
Semana 10: Plantillas dinámicas con Jinja2
"""

from flask import Flask, render_template

# Crear instancia de la aplicación Flask
app = Flask(__name__)

# Configuración básica
app.config['DEBUG'] = True


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
    """Página de Productos - Catálogo de productos"""
    return render_template('productos.html')


@app.route('/clientes')
def clientes():
    """Página de Clientes - Gestión de clientes"""
    return render_template('clientes.html')


@app.route('/facturas')
def facturas():
    """Página de Facturas - Gestión de facturas"""
    return render_template('facturas.html')


@app.route('/contacto')
def contacto():
    """Página de Contacto - Información de contacto y formulario"""
    return render_template('contacto.html')


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


# ===================== PUNTO DE ENTRADA =====================

if __name__ == '__main__':
    # Ejecutar la aplicación
    print("=" * 50)
    print("🚀 Iniciando Tienda Virtual Flask")
    print("=" * 50)
    print("📍 Accede a: http://localhost:5000")
    print("=" * 50)
    app.run(
        host='localhost',
        port=5000,
        debug=True
    )
