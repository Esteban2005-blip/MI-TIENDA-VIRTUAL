"""
Gestión de persistencia de datos en TXT, JSON, CSV y SQLite
"""

import json
import csv
import os
from datetime import datetime
from pathlib import Path

class GestorArchivos:
    """Gestor para guardar y leer datos en archivos"""
    
    def __init__(self, ruta_base="inventario/data"):
        """Inicializar rutas de archivos"""
        self.ruta_base = ruta_base
        self.ruta_txt = os.path.join(ruta_base, "datos.txt")
        self.ruta_json = os.path.join(ruta_base, "datos.json")
        self.ruta_csv = os.path.join(ruta_base, "datos.csv")
        
        # Crear directorio si no existe
        Path(ruta_base).mkdir(parents=True, exist_ok=True)
    
    # ==================== MÉTODOS TXT ====================
    
    def guardar_en_txt(self, datos):
        """Guardar datos en formato TXT"""
        try:
            with open(self.ruta_txt, 'a', encoding='utf-8') as archivo:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                linea = f"[{timestamp}] {datos}\n"
                archivo.write(linea)
            return True
        except Exception as e:
            print(f"Error al guardar en TXT: {e}")
            return False
    
    def leer_txt(self):
        """Leer datos desde TXT"""
        try:
            if os.path.exists(self.ruta_txt):
                with open(self.ruta_txt, 'r', encoding='utf-8') as archivo:
                    return archivo.readlines()
            return []
        except Exception as e:
            print(f"Error al leer TXT: {e}")
            return []
    
    # ==================== MÉTODOS JSON ====================
    
    def guardar_en_json(self, producto_dict):
        """Guardar producto en formato JSON"""
        try:
            # Leer datos existentes
            productos = self.leer_json()
            
            # Agregar nuevo producto
            productos.append(producto_dict)
            
            # Guardar lista actualizada
            with open(self.ruta_json, 'w', encoding='utf-8') as archivo:
                json.dump(productos, archivo, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error al guardar en JSON: {e}")
            return False
    
    def leer_json(self):
        """Leer datos desde JSON"""
        try:
            if os.path.exists(self.ruta_json):
                with open(self.ruta_json, 'r', encoding='utf-8') as archivo:
                    contenido = archivo.read()
                    if contenido.strip():
                        return json.loads(contenido)
            return []
        except Exception as e:
            print(f"Error al leer JSON: {e}")
            return []
    
    # ==================== MÉTODOS CSV ====================
    
    def guardar_en_csv(self, producto_dict):
        """Guardar producto en formato CSV"""
        try:
            # Definir encabezados
            encabezados = ['id', 'nombre', 'descripcion', 'precio', 'cantidad', 'categoria', 'fecha_creacion']
            
            # Verificar si el archivo existe
            archivo_existe = os.path.exists(self.ruta_csv)
            
            with open(self.ruta_csv, 'a', newline='', encoding='utf-8') as archivo:
                writer = csv.DictWriter(archivo, fieldnames=encabezados)
                
                # Escribir encabezados si es nuevo
                if not archivo_existe:
                    writer.writeheader()
                
                # Escribir fila de datos
                writer.writerow(producto_dict)
            return True
        except Exception as e:
            print(f"Error al guardar en CSV: {e}")
            return False
    
    def leer_csv(self):
        """Leer datos desde CSV"""
        try:
            productos = []
            if os.path.exists(self.ruta_csv):
                with open(self.ruta_csv, 'r', encoding='utf-8') as archivo:
                    reader = csv.DictReader(archivo)
                    for fila in reader:
                        productos.append(fila)
            return productos
        except Exception as e:
            print(f"Error al leer CSV: {e}")
            return []
