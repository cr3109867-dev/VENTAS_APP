import sqlite3

def init_db():
    conn = sqlite3.connect("ventas_app.db")
    cursor = conn.cursor()

    # Crear tablas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        correo TEXT UNIQUE NOT NULL,
        contraseña TEXT NOT NULL,
        nombre TEXT,
        rol TEXT DEFAULT 'vendedor',
        reset_token TEXT,
        negocio TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        producto TEXT NOT NULL,
        precio REAL NOT NULL,
        stock INTEGER NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        categoria TEXT,
        precio REAL,
        cantidad INTEGER,
        proveedor TEXT,
        negocio TEXT,
        codigo_barras TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS detalle_ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        venta_id INTEGER NOT NULL,
        producto_id INTEGER NOT NULL,
        cantidad INTEGER NOT NULL,
        precio REAL NOT NULL,
        FOREIGN KEY(venta_id) REFERENCES ventas(id),
        FOREIGN KEY(producto_id) REFERENCES productos(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL,
        cliente TEXT NOT NULL,
        total REAL NOT NULL,
        usuario_id INTEGER,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    );
    """)

    # Datos de prueba
    cursor.execute("""
    INSERT OR IGNORE INTO usuarios (id, nombre, correo, contraseña, rol)
    VALUES (1, 'Admin', 'admin@test.com', '1234', 'admin');
    """)

    cursor.execute("""
    INSERT OR IGNORE INTO productos (id, nombre, cantidad, precio, categoria, proveedor)
    VALUES (1, 'Producto Prueba', 10, 500, 'General', 'Proveedor Demo');
    """)

    conn.commit()
    conn.close()
    print("✅ Base de datos inicializada correctamente.")

if __name__ == "__main__":
    init_db()
