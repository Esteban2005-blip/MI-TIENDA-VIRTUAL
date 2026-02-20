# 🎯 GUÍA RÁPIDA - QUICK START

## 1️⃣ Ejecutar Localmente (30 segundos)

```bash
cd "c:\Users\ESTEBAN PAREDES\Documents\TIENDA VIRTUAL"
python app.py
```

**Luego abre**: http://localhost:5000

---

## 2️⃣ Subir a GitHub (5 minutos)

```bash
# Crear repo en github.com primero, luego:

git init
git add .
git commit -m "Tienda Virtual Flask"
git remote add origin https://github.com/TU_USUARIO/tienda-virtual-flask.git
git branch -M main
git push -u origin main
```

---

## 3️⃣ Desplegar en Render (2 minutos)

1. Ve a [https://render.com](https://render.com)
2. Crear New Web Service
3. Conectar tu repositorio GitHub
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `gunicorn app:app`
6. Deploy

**Listo!** Tu app está en línea en: `https://tu-nombre-servicio.onrender.com`

---

## 📱 URLs de la Aplicación

```
/ (Inicio)
/productos (Catálogo)
/clientes (Clientes)
/facturas (Facturas)
/about (Acerca de)
/contacto (Contacto)
```

---

## 📋 Estructura del Proyecto

```
TIENDA VIRTUAL/
├── app.py (Código Flask)
├── requirements.txt (Dependencias)
├── templates/ (7 archivos HTML)
├── static/styles.css (Estilos)
└── README.md (Documentación)
```

---

## 🎓 Lo Que Aprendiste

✅ Plantillas Jinja2 con herencia  
✅ Rutas Flask dinámicas  
✅ CSS responsivo moderno  
✅ Estructura profesional de proyectos  
✅ Despliegue en la nube  

---

## ❓ Problemas Comunes

**P: ¿Flask no inicia?**  
R: Instala dependencias: `pip install -r requirements.txt`

**P: ¿Los estilos no cargan?**  
R: Verifica que carpeta `static/` existe con `styles.css`

**P: ¿El puerto 5000 está ocupado?**  
R: Cambia puerto en app.py: `app.run(port=5001)`

---

## 📞 Archivos para Entregar

1. ✅ app.py
2. ✅ templates/ (7 archivos)
3. ✅ static/styles.css
4. ✅ requirements.txt
5. ✅ README.md
6. ✅ Link GitHub
7. ✅ Link Render (online)

---

🎉 **¡Listo en 5 minutos!**

