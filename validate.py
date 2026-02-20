"""
Script de prueba rápida para validar la estructura del proyecto
"""

import os
import sys

def check_project_structure():
    """Verifica que la estructura del proyecto sea correcta"""
    
    print("=" * 60)
    print("✓ VALIDACIÓN DE ESTRUCTURA DE PROYECTO")
    print("=" * 60)
    
    # Archivos requeridos en la raíz
    required_files = {
        'app.py': 'Aplicación Flask',
        'requirements.txt': 'Dependencias',
        '.gitignore': 'Configuración Git',
        'README.md': 'Documentación'
    }
    
    # Carpetas requeridas
    required_dirs = {
        'templates': 'Plantillas HTML',
        'static': 'Archivos estáticos'
    }
    
    # Archivos en templates/
    template_files = {
        'base.html': 'Plantilla base',
        'index.html': 'Página inicio',
        'about.html': 'Página acerca de',
        'productos.html': 'Catálogo productos',
        'clientes.html': 'Gestión clientes',
        'facturas.html': 'Gestión facturas',
        'contacto.html': 'Página contacto'
    }
    
    # Archivos en static/
    static_files = {
        'styles.css': 'Estilos CSS'
    }
    
    errors = []
    
    # Validar archivos en raíz
    print("\n📁 Verificando archivos en la raíz...")
    for filename, description in required_files.items():
        filepath = os.path.join(os.getcwd(), filename)
        if os.path.exists(filepath):
            print(f"  ✓ {filename:<20} - {description}")
        else:
            print(f"  ✗ {filename:<20} - {description} [FALTA]")
            errors.append(f"Falta: {filename}")
    
    # Validar carpetas
    print("\n📂 Verificando carpetas...")
    for dirname, description in required_dirs.items():
        dirpath = os.path.join(os.getcwd(), dirname)
        if os.path.isdir(dirpath):
            print(f"  ✓ {dirname:<20} - {description}")
        else:
            print(f"  ✗ {dirname:<20} - {description} [FALTA]")
            errors.append(f"Falta: {dirname}/")
    
    # Validar templates
    print("\n📄 Verificando plantillas HTML...")
    for filename, description in template_files.items():
        filepath = os.path.join(os.getcwd(), 'templates', filename)
        if os.path.exists(filepath):
            print(f"  ✓ templates/{filename:<20} - {description}")
        else:
            print(f"  ✗ templates/{filename:<20} - {description} [FALTA]")
            errors.append(f"Falta: templates/{filename}")
    
    # Validar estáticos
    print("\n🎨 Verificando archivos estáticos...")
    for filename, description in static_files.items():
        filepath = os.path.join(os.getcwd(), 'static', filename)
        if os.path.exists(filepath):
            print(f"  ✓ static/{filename:<20} - {description}")
        else:
            print(f"  ✗ static/{filename:<20} - {description} [FALTA]")
            errors.append(f"Falta: static/{filename}")
    
    # Resultado final
    print("\n" + "=" * 60)
    if not errors:
        print("✓ ¡ESTRUCTURA COMPLETA Y CORRECTA!")
        print("=" * 60)
        print("\n🚀 Próximos pasos:")
        print("  1. Crear el entorno virtual: python -m venv venv")
        print("  2. Activar: venv\\Scripts\\activate (Windows)")
        print("  3. Instalar dependencias: pip install -r requirements.txt")
        print("  4. Ejecutar: python app.py")
        print("  5. Abrir: http://localhost:5000")
        return True
    else:
        print("❌ ERRORES ENCONTRADOS:")
        for error in errors:
            print(f"  - {error}")
        print("=" * 60)
        return False


if __name__ == '__main__':
    success = check_project_structure()
    sys.exit(0 if success else 1)
