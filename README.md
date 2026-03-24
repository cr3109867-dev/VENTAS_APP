🧾 Ventas App

Sistema web completo para la gestión de inventario, ventas y usuarios, desarrollado con Flask y SQLite.

🚀 Características
🔐 Autenticación
Registro de usuarios
Inicio de sesión seguro (hash de contraseñas)
Recuperación de contraseña
Manejo de sesiones
Roles de usuario (admin / usuario)
👥 Gestión de usuarios (Admin)
Ver lista de usuarios
Cambiar roles (admin / usuario)
Protección de accesos
📦 Inventario
Crear, editar y eliminar productos
Control de stock en tiempo real
Alertas de bajo stock
Gestión de proveedores
💰 Ventas
Registro de ventas
Validación de stock antes de vender
Historial de ventas
Buscador en tiempo real
📊 Reportes
Dashboard con estadísticas
Gráficas de productos más vendidos
Ganancias totales
Visualización clara del negocio
🛠️ Tecnologías utilizadas
Backend: Python + Flask
Base de datos: SQLite
Frontend: HTML, CSS, Bootstrap 5
Gráficas: Chart.js
Autenticación: Werkzeug (hash de contraseñas)
📁 Estructura del proyecto
ventas_app/
│
├── app/                    # 🔧 Lógica modular del backend
│   ├── __init__.py         # Convierte app en paquete Python
│   ├── main.py             # (Opcional) lógica alternativa o pruebas
│   ├── crud.py             # Operaciones CRUD (usuarios, productos, etc.)
│
├── scripts/                # ⚙️ Scripts auxiliares
│   └── init_db.py          # Inicialización de base de datos
│
├── templates/              # 🎨 Vistas HTML (Jinja2)
│   ├── emails/             # Plantillas de correos
│   │   ├── welcome.html
│   │   └── login_notification.html
│   │
│   ├── base.html           # Layout principal
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── usuarios.html
│   ├── inventario.html
│   ├── registrar_producto.html
│   ├── registrar_venta.html
│   ├── ventas.html
│   ├── reporte.html
│   ├── forgot_password.html
│   ├── reset_password.html
│
├── static/                 # 🎨 Archivos estáticos (CSS, JS)
│   └── style.css
│
├── tests/                  # 🧪 Pruebas
│   ├── test_mail.py
│   └── test_mail_login.py
│
├── app.py                  # 🚀 Punto principal de la aplicación Flask
├── ventas_app.db           # 🗄️ Base de datos SQLite
├── requirements.txt        # 📦 Dependencias
├── README.md               # 📘 Documentación
└── .gitignore              # 🚫 Archivos ignorados por Git
⚙️ Instalación
Clonar el repositorio:
git clone https://github.com/cr3109867-dev/sistema-ventas-flask
cd ventas-app
Crear entorno virtual:
python -m venv .venv
Activar entorno:
Windows:
.venv\Scripts\activate
Mac/Linux:
source .venv/bin/activate
Instalar dependencias:
pip install flask
Ejecutar la aplicación:
python app.py
Abrir en el navegador:
http://127.0.0.1:5000
🔐 Usuario administrador

Para crear un administrador manualmente:

UPDATE usuarios SET rol = 'admin' WHERE correo = 'tu_correo@gmail.com';

Ventas
🌐 Futuras mejoras
Autenticación con Google
Base de datos PostgreSQL
API REST
Exportación de reportes (PDF / Excel)
Sistema de suscripciones (SaaS)
💰 Monetización

Este sistema puede convertirse en un producto SaaS:

Cobro mensual por uso
Planes (Gratis / Premium)
Implementación en negocios reales
👨‍💻 Autor

Desarrollado por Cristian Ramírez

📄 Licencia

Este proyecto es de uso libre para fines educativos o comerciales.