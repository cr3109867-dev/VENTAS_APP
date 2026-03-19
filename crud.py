# crud.py
import sqlite3

DB_NAME = "ventas_app.db"

# ---------------------------
# Funciones para Usuarios
# ---------------------------

def registrar_usuario(correo, contraseña, nombre=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (correo, contraseña, nombre) VALUES (?, ?, ?)",
                       (correo, contraseña, nombre))
        conn.commit()
        print("✅ Usuario registrado con éxito.")
    except sqlite3.IntegrityError:
        print("⚠️ Error: el correo ya está registrado.")
    finally:
        conn.close()

def login(correo, contraseña):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE correo=? AND contraseña=?", (correo, contraseña))
    usuario = cursor.fetchone()
    conn.close()
    if usuario:
        print("✅ Login exitoso. Bienvenido,", usuario[3])  # usuario[3] es el nombre
        return usuario
    else:
        print("❌ Correo o contraseña incorrectos.")
        return None

# ---------------------------
# Funciones para Productos
# ---------------------------

def agregar_producto(nombre, categoria, precio, cantidad, proveedor):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO productos (nombre, categoria, precio, cantidad, proveedor)
                      VALUES (?, ?, ?, ?, ?)""",
                   (nombre, categoria, precio, cantidad, proveedor))
    conn.commit()
    conn.close()
    print("✅ Producto agregado con éxito.")

def listar_productos():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return productos

# ---------------------------
# Funciones para Ventas
# ---------------------------

def registrar_venta(usuario_id, producto_id, cantidad, fecha, cliente):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO ventas (usuario_id, producto_id, cantidad, fecha, cliente)
                      VALUES (?, ?, ?, ?, ?)""",
                   (usuario_id, producto_id, cantidad, fecha, cliente))
    conn.commit()
    conn.close()
    print("✅ Venta registrada con éxito.")

def listar_ventas():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""SELECT v.id, u.nombre, p.nombre, v.cantidad, v.fecha, v.cliente
                      FROM ventas v
                      JOIN usuarios u ON v.usuario_id = u.id
                      JOIN productos p ON v.producto_id = p.id""")
    ventas = cursor.fetchall()
    conn.close()
    return ventas
