# 🛍️ Tienda Virtual Flask

Una aplicación web moderna construida con Flask y Jinja2 para gestionar una tienda virtual completa.

## 📋 Características

- **Plantillas Dinámicas**: Uso de Jinja2 para reutilizar componentes y heredar estructuras
- **Diseño Responsivo**: CSS moderno con grid y flexbox para adaptarse a cualquier dispositivo
- **Múltiples Páginas**:
  - 🏠 **Inicio**: Dashboard con productos destacados y características principales
  - 🛒 **Productos**: Catálogo completo con búsqueda y filtros
  - 👥 **Clientes**: Gestión de clientes con tabla de información
  - 📄 **Facturas**: Gestión de facturas y estado de pagos
  - ℹ️ **Acerca de**: Información de la empresa y estadísticas
  - 📞 **Contacto**: Formulario de contacto e información de comunicación

## 🏗️ Estructura del Proyecto

```
TIENDA VIRTUAL/
├── app.py                 # Aplicación Flask principal
├── requirements.txt       # Dependencias del proyecto
├── .gitignore            # Archivos a ignorar en Git
├── README.md             # Este archivo
├── templates/            # Carpeta de plantillas HTML
│   ├── base.html         # Plantilla base con herencia
│   ├── index.html        # Página de inicio
│   ├── about.html        # Página Acerca de
│   ├── productos.html    # Catálogo de productos
│   ├── clientes.html     # Gestión de clientes
│   ├── facturas.html     # Gestión de facturas
│   └── contacto.html     # Página de contacto
└── static/               # Carpeta de archivos estáticos
    └── styles.css        # Estilos CSS
```

## 🚀 Cómo Ejecutar

### Requisitos Previos
- Python 3.8 o superior
- pip (administrador de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio** (o descargar los archivos):
```bash
git clone <URL_DEL_REPOSITORIO>
cd TIENDA\ VIRTUAL
```

2. **Crear un entorno virtual**:
```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

4. **Ejecutar la aplicación**:
```bash
python app.py
```

5. **Acceder a la aplicación**:
Abre tu navegador y ve a `http://localhost:5000`

## 🎨 Espacios Clave de la Aplicación

### Plantillas (Templates)

#### **base.html** - Plantilla Base
- Encabezado con logo y eslogan
- Menú de navegación principal
- Bloque de contenido reutilizable
- Pie de página con información de contacto

Todas las demás plantillas heredan de `base.html` usando:
```jinja2
{% extends "base.html" %}
{% block content %}
    <!-- Tu contenido aquí -->
{% endblock %}
```

#### Páginas Principales

- **index.html**: Sección hero, características, y productos destacados
- **productos.html**: Catálogo con búsqueda, filtros y cards de productos
- **clientes.html**: Tabla de clientes y estadísticas
- **facturas.html**: Tabla de facturas y estado de pagos
- **about.html**: Información, misión, visión y valores
- **contacto.html**: Formulario de contacto, información y FAQs

### Estilos (CSS)

**styles.css** incluye:
- Variables CSS para colores consistentes
- Estilos de encabezado y navegación
- Grid y flexbox responsivos
- Componentes de tarjetas y botones
- Tablas estilizadas
- Formularios funcionales
- Media queries para dispositivos móviles

## 📊 Rutas Disponibles

| Ruta | Descripción |
|------|-------------|
| `/` | Página de inicio |
| `/productos` | Catálogo de productos |
| `/clientes` | Gestión de clientes |
| `/facturas` | Gestión de facturas |
| `/about` | Información de la empresa |
| `/contacto` | Formulario de contacto |

## 🔧 Tecnologías Utilizadas

- **Flask 3.0.0**: Framework web minimalista para Python
- **Jinja2 3.1.2**: Motor de plantillas para HTML dinámico
- **Python 3**: Lenguaje de programación
- **CSS3**: Estilos modernos y responsivos
- **HTML5**: Estructura semántica

## 📝 Notas Importantes

- La aplicación está en modo debug (`DEBUG = True`) para desarrollo
- Las tablas contienen datos de ejemplo estáticos
- El formulario de contacto no envía emails (es necesario implementar un backend)
- Los estilos están optimizados para máximo 1200px de ancho de contenedor
- El proyecto responde bien en dispositivos móviles (responsive design)

## 🎓 Conceptos de Aprendizaje

Este proyecto enseña:

1. **Herencia de Plantillas**: Uso de `{% extends %}` y `{% block %}`
2. **Variables Jinja2**: Interpolación con `{{ variable }}`
3. **Condicionales**: `{% if %}`, `{% else %}`
4. **Iteraciones**: `{% for item in list %}`
5. **Rutas Flask**: Decorador `@app.route()`
6. **Archivos Estáticos**: Uso de `url_for()` para assets
7. **Manejo de Errores**: `@app.errorhandler()`
8. **CSS Moderno**: Grid, Flexbox, Variables CSS

## 📱 Responsividad

La aplicación es totalmente responsive con breakpoints en:
- **Desktop**: 1200px
- **Tablet**: 768px
- **Mobile**: 480px

## 🚀 Próximos Pasos

Para expandir este proyecto, considera:

1. **Base de Datos**: Integrar SQLAlchemy para persistencia de datos
2. **Autenticación**: Implementar login de usuarios
3. **Carrito de Compras**: Sistema de compra completo
4. **API**: Crear endpoints REST para consumo externo
5. **Búsqueda Avanzada**: Filtros y búsqueda con Ajax
6. **Pagos**: Integrar pasarelas de pago (Stripe, PayPal)
7. **Correos**: Sistema de notificación por email

## 📄 Licencia

Este proyecto está disponible bajo la licencia MIT.

## 👤 Autor

Desarrollado como proyecto educativo de la Semana 10 del curso de Flask.

---

**¡Disfruta desarrollando con Flask! 🎉**
