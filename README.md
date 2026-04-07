# VENTAS_APP

Sistema de ventas desarrollado con **Flask** y **SQLite**, pensado para la gestión de inventarios, ventas y reportes.  
Incluye autenticación de usuarios, manejo de productos, generación de reportes con gráficas y exportación de datos.

---

## 🚀 Requisitos previos

- **Python 3.12** (⚠️ obligatorio, no compatible con versiones más nuevas como 3.14).
- **Git** instalado en el sistema.
- Entorno virtual recomendado para aislar dependencias.

---

## 📦 Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/cr3109867-dev/VENTAS_APP.git
   cd VENTAS_APP

## Crear entorno virtual con Python 3.12

py -3.12 -m venv .venv
.\.venv\Scripts\activate

## Verifica la versión:
python --version

## Instalar dependencias
pip install -r requirements.txt

## Inicializar base de datos
Ejecuta el script de inicialización para crear tablas y datos de prueba:
python init_db.py

## Ejecutar la aplicación
flask run

Abre en el navegador: http://127.0.0.1:5000


📂 Estructura del proyecto
app.py → punto de entrada principal de la aplicación Flask

main.py → configuración y arranque de la app

crud.py → funciones auxiliares para operaciones con la base de datos

app/ → lógica principal y controladores

templates/ → vistas HTML (interfaz de usuario)

static/ → archivos estáticos (CSS, JS, imágenes)

scripts/ → utilidades y scripts adicionales

init_db.py → inicialización de la base de datos con tablas y datos de prueba

requirements.txt → dependencias del proyecto

README.md → documentación


📊 Funcionalidades principales
Gestión de inventario (productos, precios, stock).

Registro de ventas con detalle de productos.

Reportes con gráficas (Chart.js).

Cálculo automático de ganancias.

Exportación de datos a Excel y PDF.

Inicialización rápida de la base de datos con init_db.py.


👨‍💻 Autor
Desarrollado por Cristian (cr3109867-dev)