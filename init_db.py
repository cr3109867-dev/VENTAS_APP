# init_db.py
import sqlite3

# Conectar (si no existe, se crea automáticamente en la misma carpeta)
conn = sqlite3.connect("database.db")
c = conn.cursor()

# Crear tabla de productos
c.execute('''CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    categoria TEXT,
    precio REAL,
    cantidad INTEGER,
    proveedor TEXT
)''')

# Crear tabla de ventas
c.execute('''CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    producto_id INTEGER,
    fecha TEXT,
    cantidad INTEGER,
    cliente TEXT,
    FOREIGN KEY(producto_id) REFERENCES productos(id)
)''')

# Insertar productos ficticios
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

c.executemany(
    "INSERT INTO productos (nombre, categoria, precio, cantidad, proveedor) VALUES (?, ?, ?, ?, ?)",
    productos
)

# Guardar cambios y cerrar conexión
conn.commit()
conn.close()

print("✅ Base de datos creada con éxito y productos insertados.")