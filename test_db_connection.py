from db import get_connection

try:
    conn = get_connection()
    print("¡Conexión exitosa a la base de datos MySQL!")
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    print("Usuarios en la base de datos:")
    for usuario in usuarios:
        print(usuario)
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Error al conectar o consultar: {e}")
