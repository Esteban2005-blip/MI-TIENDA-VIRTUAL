# 📚 INSTRUCCIONES DE EJECUCIÓN

## Guía Paso a Paso para ejecutar la Tienda Virtual Flask

### ✅ Requisitos Previos

- **Python 3.8+** instalado en tu sistema
- **pip** (administrador de paquetes de Python)
- Un editor de código como **Visual Studio Code** o **PyCharm**
- Acceso a linea de comandos (PowerShell, CMD, o Terminal)

---

## 🚀 OPCIÓN 1: Ejecución Rápida (Sistema Global)

Si ya tienes Flask instalado en tu sistema Python global, puedes ejecutar directamente:

```bash
# 1. Navega a la carpeta del proyecto
cd "c:\Users\ESTEBAN PAREDES\Documents\TIENDA VIRTUAL"

# 2. Ejecuta la aplicación
python app.py

# 3. Abre tu navegador en:
# http://localhost:5000
```

---

## 🔧 OPCIÓN 2: Ejecución con Entorno Virtual (RECOMENDADO)

### Paso 1: Crear Entorno Virtual

```bash
# En la carpeta del proyecto
python -m venv venv
```

Esto crea una carpeta `venv/` con un ambiente aislado de Python.

### Paso 2: Activar Entorno Virtual

**En Windows (PowerShell):**
```powershell
# Cambiar política de ejecución temporalmente
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# Activar el entorno virtual
.\venv\Scripts\Activate.ps1
```

**En Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**En macOS/Linux:**
```bash
source venv/bin/activate
```

Si la activación es exitosa, verás `(venv)` al inicio del prompt de tu terminal.

### Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

Esto instalará:
- Flask 3.0.0
- Werkzeug 3.0.1
- Jinja2 3.1.2

### Paso 4: Ejecutar la Aplicación

```bash
python app.py
```

Deberías ver algo así:
```
==================================================
🚀 Iniciando Tienda Virtual Flask
==================================================
📍 Accede a: http://localhost:5000
==================================================
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### Paso 5: Acceder a la Aplicación

Abre tu navegador web y ve a:
```
http://localhost:5000
```

---

## 🌐 Rutas Disponibles

Una vez que la aplicación está ejecutándose, puedes acceder a:

| URL | Descripción |
|-----|-------------|
| `http://localhost:5000/` | Página de inicio |
| `http://localhost:5000/productos` | Catálogo de productos |
| `http://localhost:5000/clientes` | Gestión de clientes |
| `http://localhost:5000/facturas` | Gestión de facturas |
| `http://localhost:5000/about` | Acerca de nosotros |
| `http://localhost:5000/contacto` | Formulario de contacto |

---

## 🛑 Detener la Aplicación

Para detener el servidor Flask:

1. Ve a la terminal donde está ejecutándose
2. Presiona `Ctrl + C`

---

## 🚀 Ejecutar con Visual Studio Code

### 1. Abrir la carpeta del proyecto

- Abre VS Code
- Click en `File` → `Open Folder`
- Selecciona la carpeta `TIENDA VIRTUAL`

### 2. Configurar el intérprete de Python

- Presiona `Ctrl + Shift + P`
- Busca "Python: Select Interpreter"
- Elige el intérprete en `./venv/Scripts/python.exe` si existe

### 3. Crear una terminal integrada

- Presiona `` Ctrl + ` ``
- Se abrirá una terminal integrada de VS Code

### 4. Activar el entorno virtual (si es necesario)

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Ejecutar la aplicación

```bash
python app.py
```

### 6. Abrir en navegador

- Haz click en el enlace `http://localhost:5000` mostrado en la terminal
- O copia y pega en tu navegador

---

## 🚀 Ejecutar con PyCharm

### 1. Abrir el proyecto

- Abre PyCharm
- `File` → `Open`
- Selecciona la carpeta `TIENDA VIRTUAL`

### 2. Configurar el intérprete

- `File` → `Settings` (en Windows/Linux) o `PyCharm` → `Preferences` (en macOS)
- Ve a `Project: TIENDA VIRTUAL` → `Python Interpreter`
- Click el engranaje ⚙️ → `Add...`
- Selecciona `Existing Environment`
- Navega a `./venv/Scripts/python.exe`
- Click `OK`

### 3. Crear configuración de ejecución

- Ve a `Run` → `Edit Configurations...`
- Click `+` para agregar nueva configuración
- Tipo: `Python`
- Script path: `./app.py`
- Click `OK`

### 4. Ejecutar

- Click en el botón verde ▶️ o presiona `Shift + F10`

---

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'flask'"

**Solución:** Asegúrate de que:
1. Instalaste las dependencias con `pip install -r requirements.txt`
2. Estás usando el intérprete correcto del entorno virtual
3. El entorno virtual está activado (debe ver `(venv)` en el prompt)

### Error: "Address already in use"

**Solución:** El puerto 5000 está ocupado. Opciones:
```bash
# Cambiar el puerto en app.py:
app.run(port=5001)

# O terminar el proceso en el puerto 5000
# En Windows (PowerShell):
Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess | Stop-Process
```

### Las plantillas no cargan / Error 404

**Solución:** Verifica que:
1. La carpeta `templates/` existe en el mismo directorio que `app.py`
2. Los archivos `.html` están dentro de `templates/`
3. Los nombres de archivo coinciden en `render_template()`

### Los estilos CSS no se cargan

**Solución:** Verifica que:
1. La carpeta `static/` existe al lado de `app.py`
2. El archivo `styles.css` está en `static/`
3. En el HTML está el `<link>` correcto: `{{ url_for('static', filename='styles.css') }}`

---

## 📝 Comandos Útiles

```bash
# Ver versión de Python instalada
python --version

# Ver paquetes instalados en el entorno virtual
pip list

# Instalar un paquete adicional
pip install nombre_paquete

# Desactivar el entorno virtual
deactivate

# Eliminar el entorno virtual (si necesitas regenerarlo)
rmdir /s venv    # En Windows
rm -rf venv      # En macOS/Linux
```

---

## 🎯 Verificación Rápida

Para verificar que todo está correctamente configurado, ejecuta:

```bash
python validate.py
```

Este script validará la estructura del proyecto y mostrará un resumen.

---

## ✨ Próximos Pasos

Una vez que la aplicación esté funcionando:

1. **Explorar el código** en `app.py`
2. **Modificar las plantillas** en `templates/`
3. **Ajustar los estilos** en `static/styles.css`
4. **Agregar nuevas rutas** para expandir funcionalidades
5. **Conectar a una base de datos** para persistencia de datos

---

## 📞 Soporte

Si encuentras problemas:

1. Verifica que Python está instalado: `python --version`
2. Comprueba que Flask está disponible: `python -c "import flask; print(flask.__version__)"`
3. Revisa la salida completa del error en la terminal
4. Asegúrate de estar en la carpeta correcta del proyecto

---

¡Listo! Tu aplicación Flask debe estar ejecutándose ahora. 🎉

