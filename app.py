# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from datetime import datetime, timedelta   # ⬅️ Importamos timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from werkzeug.security import generate_password_hash, check_password_hash  # 🔐 seguridad
import uuid  # para generar tokens únicos

app = Flask(__name__)
app.secret_key = "clave_secreta_segura"

# ⬅️ Configuración de expiración de sesión
app.permanent_session_lifetime = timedelta(minutes=30)

# 🔐 CONFIGURACIÓN DE CORREO
EMAIL = "cr3109867@gmail.com"
PASSWORD = "ksjg crnr jsvo acys"  # contraseña de aplicación de Gmail

# ---------------------------
# Conexión a base de datos
# ---------------------------
def get_db_connection():
    conn = sqlite3.connect("ventas_app.db")
    conn.row_factory = sqlite3.Row
    conn.text_factory = lambda b: b.decode("utf-8")  # ✅ UTF-8 correcto
    return conn

# ---------------------------
# Enviar correo
# ---------------------------
def enviar_correo(destinatario, asunto, html, remitente=EMAIL):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = str(asunto)
    msg["From"] = remitente
    msg["To"] = destinatario

    msg.attach(MIMEText(html, "html", "utf-8"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.sendmail(remitente, destinatario, msg.as_string())
            print("✅ Correo enviado correctamente")
    except Exception as e:
        print("❌ Error enviando correo:", e)

# ---------------------------
# Página principal
# ---------------------------
@app.route("/")
def index():
    return render_template("index.html")

# ---------------------------
# Registro
# ---------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        correo = request.form["correo"]
        contraseña = request.form["contraseña"]
        nombre = request.form["nombre"]

        if not correo or not contraseña or not nombre:
            flash("⚠️ Todos los campos son obligatorios.", "warning")
            return redirect(url_for("register"))

        contraseña_hash = generate_password_hash(contraseña)

        conn = get_db_connection()
        try:
            conn.execute(
                "INSERT INTO usuarios (correo, contraseña, nombre, rol) VALUES (?, ?, ?, ?)",
                (correo, contraseña_hash, nombre, "vendedor"),
            )
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            flash("⚠️ El correo ya está registrado.", "warning")
            return redirect(url_for("register"))
        conn.close()

        html = render_template("emails/welcome.html", nombre=str(nombre))
        enviar_correo(correo, u"Bienvenido al sistema de ventas", html)

        flash("✅ Registro exitoso, ahora puedes iniciar sesión.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

# ---------------------------
# Login
# ---------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form["correo"]
        contraseña = request.form["contraseña"]

        conn = get_db_connection()
        usuario = conn.execute("SELECT * FROM usuarios WHERE correo=?", (correo,)).fetchone()
        conn.close()

        if usuario and check_password_hash(usuario["contraseña"], contraseña):
            # ⬅️ Activamos sesión permanente
            session.permanent = True

            session["usuario_id"] = usuario["id"]
            session["usuario_nombre"] = usuario["nombre"]
            session["rol"] = usuario["rol"]

            html = render_template("emails/login_notification.html", nombre=str(usuario["nombre"]))
            enviar_correo(correo, u"Notificación de inicio de sesión", html)

            flash("✅ Bienvenido, " + usuario["nombre"], "success")
            return redirect(url_for("index"))
        else:
            flash("❌ Correo o contraseña incorrectos.", "danger")

    return render_template("login.html")

# ---------------------------
# Logout
# ---------------------------
@app.route("/logout")
def logout():
    session.clear()
    flash("✅ Sesión cerrada correctamente.", "info")
    return redirect(url_for("index"))

# ---------------------------
# Recuperación de contraseña
# ---------------------------
@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        correo = request.form["correo"]

        conn = get_db_connection()
        usuario = conn.execute("SELECT * FROM usuarios WHERE correo=?", (correo,)).fetchone()
        conn.close()

        if usuario:
            token = str(uuid.uuid4())
            conn = get_db_connection()
            conn.execute("UPDATE usuarios SET reset_token=? WHERE correo=?", (token, correo))
            conn.commit()
            conn.close()

            reset_link = url_for("reset_password", token=token, _external=True)
            html = f"<p>Hola {usuario['nombre']},</p><p>Haz clic en el siguiente enlace para restablecer tu contraseña:</p><a href='{reset_link}'>Restablecer contraseña</a>"
            enviar_correo(correo, "Recuperación de contraseña", html)

            flash("📧 Se ha enviado un enlace de recuperación a tu correo.", "info")
            return redirect(url_for("login"))
        else:
            flash("⚠️ El correo no está registrado.", "warning")

    return render_template("forgot_password.html")

@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if request.method == "POST":
        nueva_contraseña = request.form["contraseña"]
        contraseña_hash = generate_password_hash(nueva_contraseña)

        conn = get_db_connection()
        usuario = conn.execute("SELECT * FROM usuarios WHERE reset_token=?", (token,)).fetchone()

        if usuario:
            conn.execute("UPDATE usuarios SET contraseña=?, reset_token=NULL WHERE id=?", (contraseña_hash, usuario["id"]))
            conn.commit()
            conn.close()
            flash("✅ Tu contraseña ha sido restablecida. Ahora puedes iniciar sesión.", "success")
            return redirect(url_for("login"))
        else:
            conn.close()
            flash("⚠️ Token inválido o expirado.", "danger")
            return redirect(url_for("forgot_password"))

    return render_template("reset_password.html", token=token)

# ---------------------------
# Inventario
# ---------------------------
@app.route("/inventario")
def inventario():
    conn = get_db_connection()
    productos = conn.execute("SELECT * FROM productos").fetchall()
    conn.close()
    return render_template("inventario.html", productos=productos)

# ---------------------------
# Registrar producto (solo admin)
# ---------------------------
@app.route("/registrar_producto", methods=["GET", "POST"])
def registrar_producto():
    if session.get("rol") != "admin":
        flash("⚠️ No tienes permisos para registrar productos.", "danger")
        return redirect(url_for("inventario"))

    if request.method == "POST":
        nombre = request.form["nombre"]
        categoria = request.form["categoria"]
        precio = float(request.form["precio"])
        cantidad = int(request.form["cantidad"])
        proveedor = request.form["proveedor"]

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO productos (nombre, categoria, precio, cantidad, proveedor) VALUES (?, ?, ?, ?, ?)",
            (nombre, categoria, precio, cantidad, proveedor),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("inventario"))

    return render_template("registrar_producto.html")

# ---------------------------
# Editar producto (solo admin)
# ---------------------------
@app.route("/editar_producto/<int:id>", methods=["GET", "POST"])
def editar_producto(id):
    if session.get("rol") != "admin":
        flash("⚠️ No tienes permisos para editar productos.", "danger")
        return redirect(url_for("inventario"))

    conn = get_db_connection()
    producto = conn.execute("SELECT * FROM productos WHERE id = ?", (id,)).fetchone()

    if request.method == "POST":
        nombre = request.form["nombre"]
        categoria = request.form["categoria"]
        precio = float(request.form["precio"])
        cantidad = int(request.form["cantidad"])
        proveedor = request.form["proveedor"]

        conn.execute(
            "UPDATE productos SET nombre=?, categoria=?, precio=?, cantidad=?, proveedor=? WHERE id=?",
            (nombre, categoria, precio, cantidad, proveedor, id),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("inventario"))

    conn.close()
    return render_template("editar_producto.html", producto=producto)


    # mostrar formulario con datos precargados
    return render_template("editar_producto.html", producto=producto)

# ---------------------------
# Eliminar producto (solo admin)
# ---------------------------
@app.route("/eliminar_producto/<int:id>", methods=["POST"])
def eliminar_producto(id):
    if session.get("rol") != "admin":
        flash("⚠️ No tienes permisos para eliminar productos.", "danger")
        return redirect(url_for("inventario"))

    conn = get_db_connection()
    conn.execute("DELETE FROM productos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("inventario"))

# ---------------------------
# Registrar venta
# ---------------------------
@app.route("/registrar_venta", methods=["GET", "POST"])
def registrar_venta():
    conn = get_db_connection()
    productos = conn.execute("SELECT * FROM productos").fetchall()

    if request.method == "POST":
        producto_id = int(request.form["producto_id"])
        cantidad = int(request.form["cantidad"])
        cliente = request.form["cliente"]
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn.execute(
            "INSERT INTO ventas (usuario_id, producto_id, cantidad, fecha, cliente) VALUES (?, ?, ?, ?, ?)",
            (session.get("usuario_id"), producto_id, cantidad, fecha, cliente),
        )
        conn.execute(
            "UPDATE productos SET cantidad = cantidad - ? WHERE id = ?",
            (cantidad, producto_id),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("ventas"))

    conn.close()
    return render_template("registrar_venta.html", productos=productos)

# ---------------------------
# Ver ventas
# ---------------------------
@app.route("/ventas")
def ventas():
    conn = get_db_connection()
    ventas = conn.execute("""
        SELECT v.id, v.fecha, v.cantidad, v.cliente, p.nombre, p.precio, u.nombre AS vendedor
        FROM ventas v
        JOIN productos p ON v.producto_id = p.id
        LEFT JOIN usuarios u ON v.usuario_id = u.id
    """).fetchall()
    conn.close()
    return render_template("ventas.html", ventas=ventas)

# ---------------------------
# Reporte
# ---------------------------
@app.route("/reporte")
def reporte():
    conn = get_db_connection()
    ventas = conn.execute("""
        SELECT v.cantidad, p.precio, p.nombre
        FROM ventas v
        JOIN productos p ON v.producto_id = p.id
    """).fetchall()
    conn.close()

    ganancias = sum(v["cantidad"] * v["precio"] for v in ventas)

    productos_vendidos = {}
    precios_productos = {}

    for v in ventas:
        productos_vendidos[v["nombre"]] = productos_vendidos.get(v["nombre"], 0) + v["cantidad"]
        precios_productos[v["nombre"]] = v["precio"]

    productos_top = sorted(productos_vendidos.items(), key=lambda x: x[1], reverse=True)
    precios_lista = [precios_productos[p[0]] for p in productos_top]

    return render_template(
        "reporte.html",
        ganancias=ganancias,
        productos_top=productos_top,
        precios_productos=precios_lista
    )

# ---------------------------
# MAIN
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)