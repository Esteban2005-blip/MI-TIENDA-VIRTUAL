# 🚀 GUÍA DE DESPLIEGUE EN GITHUB Y RENDER

## 📋 Tabla de Contenidos

1. [Crear Repositorio en GitHub](#crear-repositorio-en-github)
2. [Sincronizar Código Local](#sincronizar-código-local)
3. [Desplegar en Render](#desplegar-en-render)
4. [Actualizaciones Automáticas](#actualizaciones-automáticas)

---

## 1. Crear Repositorio en GitHub

### Paso 1: Registrarse en GitHub

1. Ve a [https://github.com](https://github.com)
2. Click en "Sign up" si no tienes cuenta
3. Completa el registro con tu email y contraseña

### Paso 2: Crear un Nuevo Repositorio

1. Click en el ícono `+` en la esquina superior derecha
2. Selecciona "New repository"
3. Completa los datos:
   - **Repository name**: `tienda-virtual-flask` (o el nombre que prefieras)
   - **Description**: "Aplicación Flask de Tienda Virtual con Jinja2"
   - **Public**: Selecciona para que sea visible
   - **.gitignore**: Puedes ignorar (ya tenemos uno)
   - **License**: MIT (opcional)
4. Click en "Create repository"

### Paso 3: Copiar la URL del Repositorio

En la página del repositorio, verás un botón verde "Code" que muestra:
```
https://github.com/TU_USUARIO/tienda-virtual-flask.git
```

Copia esta URL (la usaremos después).

---

## 2. Sincronizar Código Local

### Configurar Git Localmente

```bash
# Navega a la carpeta del proyecto
cd "c:\Users\ESTEBAN PAREDES\Documents\TIENDA VIRTUAL"

# Inicializar como repositorio Git
git init

# Configurar tu usuario (si es la primera vez)
git config --global user.name "Tu Nombre"
git config --global user.email "tu.email@gmail.com"
```

### Agregar Archivos al Repositorio

```bash
# Agregar todos los archivos
git add .

# Ver archivos preparados
git status
```

Deberías ver algo como:
```
On branch master

Initial commit

Changes to be committed:
  new file:   .gitignore
  new file:   INSTRUCCIONES.md
  new file:   README.md
  new file:   app.py
  new file:   requirements.txt
  ...
```

### Hacer el Primer Commit

```bash
git commit -m "Proyecto Tienda Virtual Flask con plantillas Jinja2"
```

### Conectar al Repositorio Remoto

Reemplaza `TU_USUARIO` con tu usuario de GitHub:

```bash
git remote add origin https://github.com/TU_USUARIO/tienda-virtual-flask.git

# Verificar que se agregó correctamente
git remote -v
```

### Subir el Código a GitHub

```bash
# Renombrar rama a 'main' (estándar actual)
git branch -M main

# Subir al repositorio remoto
git push -u origin main
```

Se te pedirá iniciar sesión. Usa:
- **Username**: Tu usuario de GitHub
- **Password**: Tu token de acceso personal

> 💡 **Crear Token de Acceso Personal** (si lo necesitas):
> 1. En GitHub, ve a Settings → Developer settings → Personal access tokens
> 2. Click en "Generate new token"
> 3. Selecciona "repo" y "workflow"
> 4. Click "Generate token"
> 5. Copia el token y úsalo como contraseña en Git

---

## 3. Desplegar en Render

### Requisitos Previos

- Acceso a [https://render.com](https://render.com)
- Tu repositorio en GitHub públicamente disponible

### Paso 1: Registrarse en Render

1. Ve a [https://render.com](https://render.com)
2. Click en "Sign up"
3. Puedes usar tu cuenta de GitHub para registrarte rápidamente
4. Completa el proceso de verificación

### Paso 2: Crear un Nuevo Servicio Web

1. En el dashboard de Render, click en "New +" → "Web Service"
2. Conectar con GitHub:
   - Click "Connect account"
   - Autoriza Render para acceder a tus repositorios
   - Selecciona el repositorio `tienda-virtual-flask`

### Paso 3: Configurar el Servicio

Completa los siguientes campos:

| Campo | Valor |
|-------|-------|
| **Name** | tienda-virtual-flask |
| **Region** | Frankfurt (EU) o el más cercano |
| **Branch** | main |
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |
| **Plan** | Free (o pago si quieres mejor performance) |

### Paso 4: Agregar Dependencia de Producción

Necesitamos agregar `gunicorn` al archivo `requirements.txt`:

```txt
Flask==3.0.0
Werkzeug==3.0.1
Jinja2==3.1.2
gunicorn==21.2.0
```

Luego haz commit y push:

```bash
git add requirements.txt
git commit -m "Agregar gunicorn para producción"
git push
```

### Paso 5: Deploying

1. En Render, click en "Deploy"
2. Espera a que se complete el despliegue (verás un log en tiempo real)
3. Una vez completado, verás un URL como: `https://tienda-virtual-flask.onrender.com`

### Paso 6: Verificar Despliegue

1. Haz click en el URL generado
2. Deberías ver tu aplicación Tienda Virtual en línea
3. Prueba las diferentes páginas:
   - ``https://tu-nombre-servicio.onrender.com/``
   - ``https://tu-nombre-servicio.onrender.com/productos``
   - ``https://tu-nombre-servicio.onrender.com/contacto``

---

## 4. Actualizaciones Automáticas

Una vez conectado, Render se sincroniza automáticamente con tu repositorio GitHub:

### Para Actualizar la Aplicación:

```bash
# 1. Haz cambios en tus archivos locales
# 2. Agrega los cambios
git add .

# 3. Haz commit
git commit -m "Descripción de los cambios"

# 4. Sube a GitHub
git push

# 5. Render detectará automáticamente los cambios
#    y redesplegará la aplicación
```

**Total de tiempo de redeploy**: 1-2 minutos

---

## 📊 Flujo Completo de Actualización

```
Local (Tu Computadora)
    ↓ git push
GitHub (Repositorio Central)
    ↓ webhook automático
Render (Servidor en Nube)
    ↓ rebuild y restart
Aplicación Publicada Online
```

---

## 🔍 Verificar Estado en Render

### Dashboard
1. Ve a tu dashboard en Render
2. Click en tu servicio `tienda-virtual-flask`
3. Verás:
   - **Status**: "Live" o "Deploying"
   - **Last Deploy**: Fecha y hora del último despliegue
   - **Logs**: Historial de eventos

### Logs en Tiempo Real
1. Click en la pestaña "Logs"
2. Verás el output completo del servidor
3. Útil para debugging

---

## 🐛 Solución de Problemas en Render

### El servicio no inicia

**Causa común**: Falta `gunicorn` en requirements.txt

**Solución**:
1. Agrega `gunicorn==21.2.0` a requirements.txt
2. Haz commit y push
3. El despliegue se reiniciará automáticamente

### Error "Application failed to start"

**Causa**: El archivo `app.py` no existe o está mal configurado

**Solución**:
1. Verifica que `app.py` existe en la raíz del repositorio
2. Revisa los logs en Render para más detalles
3. El comando Start Command debe ser exacto: `gunicorn app:app`

### La aplicación sigue una versión vieja

**Causa**: Render caché

**Solución**:
1. En el dashboard de Render, click "Manual Deploy"
2. Selecciona la rama y click "Deploy"

---

## 📱 Compartir tu Aplicación

Una vez desplegada, puedes compartir tu URL:

```
Mi Tienda Virtual: https://tu-nombre-servicio.onrender.com
```

Tu profesor y compañeros pueden acceder y ver tu proyecto navegando esta URL.

---

## 📝 Checklist Final

- [ ] Repositorio creado en GitHub
- [ ] Código subido a GitHub
- [ ] Cuenta creada en Render
- [ ] Servicio web creado en Render
- [ ] `gunicorn` agregado a requirements.txt
- [ ] Aplicación desplegada exitosamente
- [ ] Puedes acceder a la URL de Render
- [ ] Todas las páginas funcionan correctamente

---

## 🎯 Próximas Actualizaciones

Cuando hagas cambios a tu proyecto:

```bash
# Desde tu terminal en la carpeta del proyecto
git add .
git commit -m "Descripción del cambio"
git push

# ¡Eso es todo! Render se actualiza automáticamente
```

---

¡Listo! Tu aplicación Flask está en línea y públicamente accesible. 🎉

