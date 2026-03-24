# init_db.py
import sqlite3

# Conexión a la base de datos principal
conn = sqlite3.connect("ventas_app.db")
cursor = conn.cursor()

# Tabla de usuarios (para login)
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    correo TEXT UNIQUE NOT NULL,
    contraseña TEXT NOT NULL,
    nombre TEXT
)
""")

# Tabla de inventario (productos simples)
cursor.execute("""
CREATE TABLE IF NOT EXISTS inventario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    producto TEXT NOT NULL,
    precio REAL NOT NULL,
    stock INTEGER NOT NULL
)
""")

# Tabla de productos (más detallada, con proveedor y categoría)
cursor.execute("""
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    categoria TEXT,
    precio REAL NOT NULL,
    cantidad INTEGER NOT NULL,
    proveedor TEXT
)
""")

# Tabla de ventas (relaciona usuarios y productos)
cursor.execute("""
CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    producto_id INTEGER,
    cantidad INTEGER,
    fecha TEXT,
    cliente TEXT,
    FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY(producto_id) REFERENCES productos(id)
)
""")



# Guardar cambios y cerrar conexión
conn.commit()
conn.close()

print("✅ Base de datos 'ventas_app.db' creada con éxito y productos insertados.")


