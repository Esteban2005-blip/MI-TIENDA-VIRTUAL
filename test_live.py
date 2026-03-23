import requests

rutas = ['/', '/login', '/register', '/productos', '/datos', '/usuarios', '/contacto', '/carrito', '/productos/formulario', '/about', '/facturas', '/clientes']
for ruta in rutas:
    try:
        r = requests.get('http://127.0.0.1:5000' + ruta, timeout=5, allow_redirects=False)
        print(f'{ruta}: {r.status_code}')
        if r.status_code == 500:
            print('--- ERROR BODY ---')
            print(r.text[:1000])
    except Exception as e:
        print(f'{ruta}: ERROR {e}')
