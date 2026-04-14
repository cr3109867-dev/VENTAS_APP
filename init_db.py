import sqlite3
from werkzeug.security import generate_password_hash

def init_db():
    conn = sqlite3.connect("ventas_app.db")
    cursor = conn.cursor()

    # ---------------------------
    # Crear tablas
    # ---------------------------
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
        nombre TEXT NOT NULL,
        categoria TEXT,
        precio REAL NOT NULL,
        cantidad INTEGER NOT NULL,
        proveedor TEXT,
        negocio TEXT NOT NULL,
        codigo_barras TEXT,
        fecha_vencimiento DATE,
        qr_path TEXT
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

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS detalle_ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        venta_id INTEGER NOT NULL,
        producto_id INTEGER NOT NULL,
        cantidad INTEGER NOT NULL,
        precio REAL NOT NULL,
        FOREIGN KEY (venta_id) REFERENCES ventas(id),
        FOREIGN KEY (producto_id) REFERENCES productos(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS negocios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT NOT NULL,
        nombre TEXT NOT NULL,
        patron TEXT,
        usuario TEXT,
        descripcion TEXT,
        gmail TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reportes_programados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        negocio TEXT NOT NULL,
        frecuencia TEXT NOT NULL,        -- diario, semanal, mensual
        hora TEXT NOT NULL,              -- formato HH:MM
        destinatario TEXT NOT NULL,      -- correo principal
        formato TEXT NOT NULL DEFAULT 'pdf', -- pdf, excel, ambos
        tipo_reporte TEXT NOT NULL DEFAULT 'completo', -- completo, stock_bajo, proximos_vencer
        cc TEXT,                         -- correo opcional para copia
        creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reportes_enviados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        negocio TEXT NOT NULL,
        reporte TEXT NOT NULL,
        fecha_envio TEXT NOT NULL,
        destinatario TEXT
    );
    """)

    # ---------------------------
    # Datos de prueba garantizados
    # ---------------------------
    contraseña_hash = generate_password_hash("1234")
    cursor.execute("""
    INSERT OR REPLACE INTO usuarios (id, nombre, correo, contraseña, rol)
    VALUES (1, 'Admin', 'admin@test.com', ?, 'admin');
    """, (contraseña_hash,))

    cursor.execute("""
    INSERT OR REPLACE INTO productos (
        id, nombre, cantidad, precio, categoria, proveedor, negocio, codigo_barras, fecha_vencimiento, qr_path
    ) VALUES (
        1, 'Producto Prueba', 10, 500, 'General', 'Proveedor Demo', 'DemoNegocio', '000111222', NULL, NULL
    );
    """)

    cursor.execute("""
    INSERT OR REPLACE INTO reportes_programados (
        id, negocio, frecuencia, hora, destinatario, formato, tipo_reporte
    ) VALUES (
        1, 'DemoNegocio', 'diario', '08:00', 'admin@test.com', 'pdf', 'completo'
    );
    """)

    cursor.execute("""
    INSERT OR REPLACE INTO reportes_enviados (
        id, negocio, reporte, fecha_envio, destinatario
    ) VALUES (
        1, 'DemoNegocio', 'Reporte inicial', datetime('now'), 'admin@test.com'
    );
    """)

    conn.commit()
    conn.close()
    print("✅ Base de datos inicializada correctamente.")

if __name__ == "__main__":
    init_db()
