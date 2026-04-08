# VENTAS_APP

Sistema de ventas desarrollado con **Flask** y **SQLite**, pensado para la gestión de inventarios, ventas y reportes.  
Incluye autenticación de usuarios, manejo de productos, generación de reportes con gráficas y exportación de datos.

---

## 🚀 Requisitos previos

- **Python 3.12** (⚠️ obligatorio, no compatible con versiones más nuevas como 3.14).
- **Git** instalado en el sistema.
- **SQLite3** instalado para manejar la base de datos.
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

🗄️ Inicialización de la base de datos
Tienes dos opciones para crear la base de datos:

Opción A: Usar schema.sql (recomendado)

Este archivo contiene la definición exacta de las tablas.
Ejecuta: 
sqlite3 ventas_app.db < schema.sql

Opción B: Usar init_db.py

Este script crea las tablas y además inserta datos de prueba (usuario Admin y un producto demo).
Ejecuta:
python init_db.py

⚠️ Usa solo una de las dos opciones. Si ya tienes la base creada, no es necesario volver a ejecutar estos pasos.


## Ejecutar la aplicación
flask run o python 

Abre en el navegador: http://127.0.0.1:5000

📂 Estructura del proyecto
app.py → punto de entrada principal de la aplicación Flask

main.py → configuración y arranque de la app

crud.py → funciones auxiliares para operaciones con la base de datos

app/ → lógica principal y controladores

templates/ → vistas HTML (interfaz de usuario)

static/ → archivos estáticos (CSS, JS, imágenes)

scripts/ → utilidades y scripts adicionales

init_db.py → inicialización de la base de datos con datos de prueba

schema.sql → definición de la estructura de la base de datos

requirements.txt → dependencias del proyecto

README.md → documentación

📊 Funcionalidades principales
Gestión de inventario (productos, precios, stock).

Registro de ventas con detalle de productos.

Reportes con gráficas (Chart.js).

Cálculo automático de ganancias.

Exportación de datos a Excel y PDF.

Inicialización rápida de la base de datos con schema.sql o init_db.py.

👨‍💻 Autor
Desarrollado por Cristian (cr3109867-dev)

✅ Notas importantes
Usa siempre Python 3.12 para evitar incompatibilidades.

Si clonas el repo en otro PC, recuerda ejecutar: sqlite3 ventas_app.db < schema.sql
o bien:
python init_db.py
para que la base de datos se cree con la misma estructura y datos iniciales.