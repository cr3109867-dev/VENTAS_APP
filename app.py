# -*- coding: utf-8 -*-
from itsdangerous import SignatureExpired, BadSignature
from itsdangerous import URLSafeTimedSerializer
from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

app = Flask(__name__)

# PRIMERO define la clave
app.secret_key = "clave_secreta_segura"

# DESPUÉS creas el serializer
serializer = URLSafeTimedSerializer(app.secret_key)

app.permanent_session_lifetime = timedelta(minutes=30)

EMAIL = "cr3109867@gmail.com"
PASSWORD = "ksjg crnr jsvo acys"

# ---------------------------
# DB
# ---------------------------
def get_db_connection():
    conn = sqlite3.connect("ventas_app.db")
    conn.row_factory = sqlite3.Row
    conn.text_factory = lambda b: b.decode("utf-8")
    return conn

# ---------------------------
# EMAIL
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
    except Exception as e:
        print("Error correo:", e)

# ---------------------------
# INDEX
# ---------------------------
@app.route("/")
def index():
    return render_template("index.html")

# ---------------------------
# REGISTER
# ---------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        correo = request.form["correo"]
        contraseña = request.form["contraseña"]
        nombre = request.form["nombre"]

        contraseña_hash = generate_password_hash(contraseña)

        conn = get_db_connection()
        try:
            conn.execute(
                "INSERT INTO usuarios (correo, contraseña, nombre, rol) VALUES (?, ?, ?, ?)",
                (correo, contraseña_hash, nombre, "usuario"),
            )
            conn.commit()
        except:
            flash("Correo ya registrado", "danger")
            return redirect(url_for("register"))
        conn.close()

        flash("Registro exitoso", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

# ---------------------------
# LOGIN
# ---------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form["correo"]
        contraseña = request.form["contraseña"]

        conn = get_db_connection()
        usuario = conn.execute(
            "SELECT * FROM usuarios WHERE correo=?", (correo,)
        ).fetchone()
        conn.close()

        if usuario and check_password_hash(usuario["contraseña"], contraseña):
            session.permanent = True
            session["usuario_id"] = usuario["id"]
            session["usuario_nombre"] = usuario["nombre"]
            session["rol"] = usuario["rol"] if usuario["rol"] else "usuario"

            # 🔥 ENVIAR CORREO DE LOGIN
            try:
                html = render_template(
                    "emails/login_notification.html",
                    nombre=usuario["nombre"]
                )

                enviar_correo(
                    usuario["correo"],
                    "Inicio de sesión exitoso",
                    html
                )

                print("✅ Correo enviado correctamente")

            except Exception as e:
                print("❌ Error enviando correo:", e)

            flash("Bienvenido " + usuario["nombre"], "success")
            return redirect(url_for("index"))

        flash("Datos incorrectos", "danger")

    return render_template("login.html")
# ---------------------------
# FORGOT PASSWORD
# ---------------------------
@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        correo = request.form["correo"]

        conn = get_db_connection()
        usuario = conn.execute(
            "SELECT * FROM usuarios WHERE correo=?", (correo,)
        ).fetchone()
        conn.close()

        if usuario:
            # 🔐 Token seguro con email
            token = serializer.dumps(correo, salt="password-reset")

            # ⏱ Link con token
            link = url_for("reset_password", token=token, _external=True)

            html = f"""
            <h2>🔐 Recuperar contraseña</h2>
            <p>Hola {usuario["nombre"]},</p>
            <p>Haz clic en el botón para cambiar tu contraseña:</p>

            <a href="{link}" style="padding:10px 20px;
            background:#27ae60;color:white;text-decoration:none;border-radius:5px;">
            Cambiar contraseña
            </a>

            <p>⚠️ Este enlace expira en 15 minutos</p>
            """

            enviar_correo(correo, "Recuperar contraseña", html)

        flash("Si el correo existe, se enviará un enlace", "info")
        return redirect(url_for("login"))

    return render_template("forgot_password.html")

# ---------------------------
# RESET PASSWORD
# ---------------------------
@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    try:
        # ⏱ Expira en 900 segundos = 15 min
        correo = serializer.loads(token, salt="password-reset", max_age=900)

    except SignatureExpired:
        flash("⏰ El enlace expiró", "danger")
        return redirect(url_for("forgot_password"))

    except BadSignature:
        flash("⚠️ Token inválido", "danger")
        return redirect(url_for("login"))

    conn = get_db_connection()
    usuario = conn.execute(
        "SELECT * FROM usuarios WHERE correo=?", (correo,)
    ).fetchone()

    if not usuario:
        conn.close()
        flash("Usuario no encontrado", "danger")
        return redirect(url_for("login"))

    if request.method == "POST":
        nueva = request.form["contraseña"]

        if len(nueva) < 6:
            flash("Mínimo 6 caracteres", "warning")
            return redirect(request.url)

        hash_nueva = generate_password_hash(nueva)

        conn.execute(
            "UPDATE usuarios SET contraseña=? WHERE id=?",
            (hash_nueva, usuario["id"])
        )
        conn.commit()
        conn.close()

        flash("✅ Contraseña actualizada", "success")
        return redirect(url_for("login"))

    conn.close()
    return render_template("reset_password.html")
# ---------------------------
# LOGOUT
# ---------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

# ---------------------------
# USUARIOS (ADMIN)
# ---------------------------
@app.route("/usuarios")
def usuarios():
    if session.get("rol") != "admin":
        return redirect(url_for("index"))

    conn = get_db_connection()
    usuarios = conn.execute("SELECT id, nombre, correo, rol FROM usuarios").fetchall()
    conn.close()

    return render_template("usuarios.html", usuarios=usuarios)

# ---------------------------
# CAMBIAR ROL
# ---------------------------
@app.route("/cambiar_rol/<int:id>")
def cambiar_rol(id):
    if session.get("rol") != "admin":
        return redirect(url_for("index"))

    if id == session.get("usuario_id"):
        return redirect(url_for("usuarios"))

    conn = get_db_connection()
    usuario = conn.execute("SELECT rol FROM usuarios WHERE id=?", (id,)).fetchone()

    nuevo_rol = "admin" if usuario["rol"] == "usuario" else "usuario"

    conn.execute("UPDATE usuarios SET rol=? WHERE id=?", (nuevo_rol, id))
    conn.commit()
    conn.close()

    return redirect(url_for("usuarios"))

# ---------------------------
# INVENTARIO
# ---------------------------
@app.route("/inventario")
def inventario():
    conn = get_db_connection()
    productos = conn.execute("SELECT * FROM productos").fetchall()
    conn.close()
    return render_template("inventario.html", productos=productos)

# ---------------------------
# REGISTRAR PRODUCTO (ADMIN)
# ---------------------------
@app.route("/registrar_producto", methods=["GET", "POST"])
def registrar_producto():
    if session.get("rol") != "admin":
        return redirect(url_for("inventario"))

    if request.method == "POST":
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO productos (nombre, categoria, precio, cantidad, proveedor) VALUES (?, ?, ?, ?, ?)",
            (
                request.form["nombre"],
                request.form["categoria"],
                float(request.form["precio"]),
                int(request.form["cantidad"]),
                request.form["proveedor"],
            ),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("inventario"))

    return render_template("registrar_producto.html")

# ---------------------------
# EDITAR PRODUCTO
# ---------------------------
@app.route("/editar_producto/<int:id>", methods=["GET", "POST"])
def editar_producto(id):
    if session.get("rol") != "admin":
        return redirect(url_for("inventario"))

    conn = get_db_connection()
    producto = conn.execute("SELECT * FROM productos WHERE id=?", (id,)).fetchone()

    if request.method == "POST":
        conn.execute(
            "UPDATE productos SET nombre=?, categoria=?, precio=?, cantidad=?, proveedor=? WHERE id=?",
            (
                request.form["nombre"],
                request.form["categoria"],
                float(request.form["precio"]),
                int(request.form["cantidad"]),
                request.form["proveedor"],
                id,
            ),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("inventario"))

    conn.close()
    return render_template("editar_producto.html", producto=producto)

# ---------------------------
# ELIMINAR PRODUCTO
# ---------------------------
@app.route("/eliminar_producto/<int:id>", methods=["POST"])
def eliminar_producto(id):
    if session.get("rol") != "admin":
        return redirect(url_for("inventario"))

    conn = get_db_connection()
    conn.execute("DELETE FROM productos WHERE id=?", (id,))
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