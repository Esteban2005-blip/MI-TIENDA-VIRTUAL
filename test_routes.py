from app import app
import traceback

app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False

with app.test_client() as c:
    # Test without login
    print('--- Sin sesion ---')
    for ruta in ['/', '/productos', '/facturas', '/clientes']:
        r = c.get(ruta, follow_redirects=False)
        loc = r.headers.get('Location', '')
        print(f'{ruta}: {r.status_code} -> {loc}')

    # Set user session
    with c.session_transaction() as sess:
        sess['_user_id'] = '1'
        sess['_fresh'] = True

    print('--- Con sesion ---')
    for ruta in ['/', '/productos', '/facturas', '/clientes', '/datos', '/usuarios', '/carrito', '/productos/formulario', '/about', '/contacto']:
        try:
            r = c.get(ruta, follow_redirects=True)
            if r.status_code != 200:
                print(f'{ruta}: {r.status_code}')
                print(r.data.decode('utf-8', errors='replace')[:300])
            else:
                print(f'{ruta}: OK 200')
        except Exception as e:
            print(f'{ruta}: EXCEPTION - {e}')
            traceback.print_exc()

print('Done.')
