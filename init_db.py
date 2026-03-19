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

# Insertar productos ficticios (solo si la tabla está vacía)
productos = [
    ("Arroz 1kg", "Granos", 5000, 50, "Distribuidora La 14"),
    ("Aceite 500ml", "Abarrotes", 8000, 30, "Alimentos S.A."),
    ("Pan artesanal", "Panadería", 2000, 40, "Panadería El Sol"),
    ("Leche 1L", "Lácteos", 4500, 25, "Lácteos Andinos"),
    ("Café molido 250g", "Bebidas", 12000, 15, "Café de Colombia"),
    ("Jabón de baño", "Aseo", 2500, 60, "Higiene Hogar"),
    ("Gaseosa 1.5L", "Bebidas", 6000, 20, "Bebidas Nacionales"),
    ("Huevos docena", "Proteína", 7000, 35, "Granja Santa Fé")
]

cursor.executemany("""
INSERT INTO productos (nombre, categoria, precio, cantidad, proveedor)
VALUES (?, ?, ?, ?, ?)
""", productos)

# Guardar cambios y cerrar conexión
conn.commit()
conn.close()

print("✅ Base de datos 'ventas_app.db' creada con éxito y productos insertados.")


