# models/producto.py

class Producto:
    def __init__(self, id_producto, nombre, precio, stock, descripcion=None, categoria=None, imagen=None):
        self.id_producto = id_producto
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.descripcion = descripcion
        self.categoria = categoria
        self.imagen = imagen
