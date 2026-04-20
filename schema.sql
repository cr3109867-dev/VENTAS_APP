-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    correo TEXT NOT NULL,
    contraseña TEXT NOT NULL,
    nombre TEXT,
    rol TEXT DEFAULT 'vendedor',
    reset_token TEXT,
    negocio TEXT
);

-- Tabla de productos
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    categoria TEXT,
    precio REAL NOT NULL,
    cantidad INTEGER NOT NULL,
    proveedor TEXT,
    negocio TEXT,
    codigo_barras TEXT,
    fecha_vencimiento DATE,
    qr_path TEXT
);

-- Tabla inventario (auxiliar)
CREATE TABLE IF NOT EXISTS inventario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    producto TEXT NOT NULL,
    precio REAL NOT NULL,
    stock INTEGER NOT NULL
);

-- Tabla de ventas
CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT NOT NULL,
    cliente TEXT NOT NULL,
    total REAL NOT NULL,
    usuario_id INTEGER,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- Tabla detalle de ventas
CREATE TABLE IF NOT EXISTS detalle_ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    venta_id INTEGER NOT NULL,
    producto_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    precio REAL NOT NULL,
    FOREIGN KEY (venta_id) REFERENCES ventas(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

-- Tabla de negocios
CREATE TABLE IF NOT EXISTS negocios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL,          -- Ej: farmacia, ferretería, mercado, ropa
    nombre TEXT NOT NULL,        -- Nombre del negocio
    patron TEXT,                 -- Datos del patrón/propietario
    usuario TEXT,                -- Usuario responsable
    descripcion TEXT,            -- Descripción del negocio
    gmail TEXT                   -- Correo electrónico del negocio
);

-- Tabla de reportes programados
CREATE TABLE IF NOT EXISTS reportes_programados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    negocio TEXT NOT NULL,
    frecuencia TEXT NOT NULL,        -- "diario", "semanal", "mensual"
    hora TEXT NOT NULL,              -- formato HH:MM
    destinatario TEXT NOT NULL,      -- correo principal
    formato TEXT NOT NULL DEFAULT 'pdf', -- pdf, excel, ambos
    tipo_reporte TEXT NOT NULL DEFAULT 'completo', -- completo, stock_bajo, proximos_vencer
    cc TEXT,                         -- correo opcional para copia
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de reportes enviados
CREATE TABLE IF NOT EXISTS reportes_enviados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    negocio TEXT NOT NULL,
    reporte TEXT NOT NULL,
    fecha_envio TEXT NOT NULL,
    destinatario TEXT
);

-- Tabla negocio (auxiliar)
CREATE TABLE IF NOT EXISTS negocio (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    patron TEXT,
    usuario TEXT,
    descripcion TEXT
);

-- Tabla de logs
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT NOT NULL,
    usuario TEXT NOT NULL,
    accion TEXT NOT NULL,
    detalle TEXT,
    negocio TEXT
);
