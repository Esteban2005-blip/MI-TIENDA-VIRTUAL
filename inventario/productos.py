"""
Modelo de Productos para la base de datos SQLite
"""

from inventario.bd import db
from datetime import datetime

class Producto(db.Model):
    """Modelo de datos para productos"""
    __tablename__ = 'productos'
    
    # Atributos
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.String(500), nullable=True)
    precio = db.Column(db.Float, nullable=False)
    cantidad = db.Column(db.Integer, default=0)
    categoria = db.Column(db.String(50), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Producto {self.nombre} - ${self.precio}>"
    
    def to_dict(self):
        """Convertir producto a diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio': self.precio,
            'cantidad': self.cantidad,
            'categoria': self.categoria,
            'fecha_creacion': self.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S') if self.fecha_creacion else None
        }
