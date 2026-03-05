# Ventas App

*Ventas App* es un sistema web desarrollado con *Flask* y *SQLite* para la gestión de inventario y ventas en pequeños negocios.  
Su objetivo es ofrecer una solución sencilla, accesible y profesional para tiendas, ferreterías, farmacias y otros comercios que necesitan controlar productos, registrar ventas y generar reportes de ganancias.

---

## 🚀 Características principales
- 📦 *Inventario*: registrar productos con nombre, categoría, precio, cantidad y proveedor.
- ✏️ *Edición y eliminación*: actualizar datos de productos o eliminarlos cuando ya no estén disponibles.
- 💰 *Ventas*: registrar ventas con cliente, cantidad y fecha automáticamente.
- 📊 *Reportes*: calcular ganancias totales y mostrar historial de ventas.
- 🎨 *Interfaz responsive*: diseño moderno que se adapta a PC, tablet y celular.
- 🔒 *Base de datos local*: almacenamiento seguro con SQLite.
- 🗑️ *Gestión completa CRUD*: crear, leer, actualizar y eliminar productos.

---

## 📂 Estructura del proyecto

VENTAS_APP/
│── app.py                # Aplicación Flask principal
│── init_db.py            # Script para inicializar la base de datos
│── database.db           # Base de datos SQLite
│── requirements.txt      # Dependencias del proyecto
│── README.md             # Documentación
│── LICENSE               # Licencia (ej. MIT)
│
├── static/               # Archivos estáticos
│   └── style.css
│
└── templates/            # Plantillas HTML
    ├── base.html
    ├── index.html
    ├── inventario.html
    ├── registrar_producto.html
    ├── registrar_venta.html
    ├── ventas.html
    └── reporte.html
`

---

⚙️ Instalación y uso

1. Clona el repositorio:
   `bash
   git clone 
   cd ventas_app
   `

2. 2. Instala dependencias:
   `bash
   pip install -r requirements.txt
   `

3. Inicializa la base de datos:
   `bash
   python init_db.py
   `

4. Ejecuta la aplicación:
   `bash
   python app.py
   `

5. Abre en tu navegador:
   `
   http://127.0.0.1:5000
   `


       Licencia
       
       Este proyecto está bajo la licencia MIT.  
       Puedes usarlo, modificarlo y distribuirlo libremente, siempre dando crédito al autor.