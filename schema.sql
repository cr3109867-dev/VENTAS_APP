CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    correo TEXT UNIQUE NOT NULL,
    contraseña TEXT NOT NULL,
    nombre TEXT,
    rol TEXT DEFAULT 'vendedor',
    reset_token TEXT,
    negocio TEXT
);

CREATE TABLE inventario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    producto TEXT NOT NULL,
    precio REAL NOT NULL,
    stock INTEGER NOT NULL
);

CREATE TABLE productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    categoria TEXT,
    precio REAL,
    cantidad INTEGER,
    proveedor TEXT,
    negocio TEXT,
    codigo_barras TEXT
);

CREATE TABLE detalle_ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    venta_id INTEGER NOT NULL,
    producto_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    precio REAL NOT NULL,
    FOREIGN KEY(venta_id) REFERENCES ventas(id),
    FOREIGN KEY(producto_id) REFERENCES productos(id)
);

CREATE TABLE ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT NOT NULL,
    cliente TEXT NOT NULL,
    total REAL NOT NULL,
    usuario_id INTEGER,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);
