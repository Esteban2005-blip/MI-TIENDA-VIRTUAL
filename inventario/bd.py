"""
Configuración de la base de datos SQLite con SQLAlchemy
"""

from flask_sqlalchemy import SQLAlchemy
import os

# Crear instancia de SQLAlchemy
db = SQLAlchemy()

def init_db(app):
    """Inicializar la base de datos con la aplicación Flask"""
    db.init_app(app)
    
    # Crear las tablas si no existen
    with app.app_context():
        db.create_all()
        print("[OK] Base de datos inicializada correctamente")
