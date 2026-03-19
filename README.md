# 🛒 Ventas App

**Ventas App** es un sistema web desarrollado con **Flask** y **SQLite** para la gestión de inventario, ventas y usuarios.
Incluye autenticación (registro y login) y envío de notificaciones por correo electrónico usando Gmail.

---

## 🚀 Características principales

* 👤 **Autenticación de usuarios**

  * Registro de usuarios
  * Inicio y cierre de sesión
  * Notificación por correo al registrarse
  * Notificación por correo al iniciar sesión

* 📦 **Inventario**

  * Registro de productos
  * Edición y eliminación de productos

* 💰 **Ventas**

  * Registro de ventas con cliente, cantidad y fecha
  * Actualización automática del inventario

* 📊 **Reportes**

  * Cálculo de ganancias
  * Productos más vendidos

* 📧 **Sistema de correos**

  * Envío de correos con SMTP (Gmail)
  * Plantillas HTML personalizadas

* 🎨 **Interfaz**

  * Diseño responsive adaptable a distintos dispositivos

* 🗄️ **Base de datos**

  * SQLite para almacenamiento local

---

## 📂 Estructura del proyecto

```id="estructura1"
VENTAS_APP/
│
├── app.py
├── crud.py
├── init_db.py
├── main.py
├── requirements.txt
├── README.md
├── test_mail.py
├── test_mail_login.py
├── ventas_app.db
│
├── venv/                  # Entorno virtual (NO subir a GitHub)
│
├── static/
│   └── style.css
│
└── templates/
    ├── base.html
    ├── index.html
    ├── login.html
    ├── register.html
    ├── inventario.html
    ├── registrar_producto.html
    ├── registrar_venta.html
    ├── ventas.html
    ├── reporte.html
    │
    └── emails/
        ├── welcome.html
        └── login_notification.html
```

---

## ⚙️ Instalación y uso

### 1. Clonar el repositorio

```bash id="clone1"
git clone https://github.com/TU_USUARIO/ventas-app.git
cd VENTAS_APP
```

---

### 2. Crear entorno virtual (opcional)

```bash id="venv1"
python -m venv venv
venv\Scripts\activate
```

---

### 3. Instalar dependencias

```bash id="deps1"
pip install -r requirements.txt
```

---

### 4. Inicializar base de datos

```bash id="db1"
python init_db.py
```

---

### 5. Configurar correo (IMPORTANTE)

En `app.py` configura:

```python id="mail1"
EMAIL = "tu_correo@gmail.com"
PASSWORD = "tu_password_de_aplicacion"
```

🔐 Usa una **contraseña de aplicación de Gmail**

---

### 6. Ejecutar la aplicación

```bash id="run1"
python app.py
```

---

### 7. Abrir en el navegador

```id="url1"
http://127.0.0.1:5000
```

---

## 🔐 Tecnologías utilizadas

* Python 3.12.3
