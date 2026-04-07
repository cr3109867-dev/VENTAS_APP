# -*- coding: utf-8 -*-
from itsdangerous import SignatureExpired, BadSignature
from itsdangerous import URLSafeTimedSerializer
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
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
            session["negocio"] = usuario["negocio"]


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
            # 👉 Aquí cambiamos: en vez de ir al index, va a selección de negocio
            return redirect(url_for("seleccionar_negocio"))

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
# Seleccionar negocio
#----------------------------
@app.route("/seleccionar_negocio", methods=["GET", "POST"])
def seleccionar_negocio():
    if "usuario_id" not in session:
        # Si no hay sesión activa, redirige al login
        return redirect(url_for("login"))

    if request.method == "POST":
        negocio = request.form.get("negocio")
        session["negocio"] = negocio

        # ✅ Actualizar el negocio en la base de datos
        conn = get_db_connection()
        conn.execute(
            "UPDATE usuarios SET negocio=? WHERE id=?",
            (negocio, session["usuario_id"])
        )
        conn.commit()
        conn.close()

        # ✅ Mensaje flash de confirmación
        flash(f"Negocio cambiado a {negocio.capitalize()}", "success")

        # Redirigir al dashboard correspondiente
        if negocio == "tienda_de_ropa":
            return redirect(url_for("dashboard_tienda_de_ropa"))
        elif negocio == "farmacia":
            return redirect(url_for("dashboard_farmacia"))
        elif negocio == "ferreteria":
            return redirect(url_for("dashboard_ferreteria"))
        elif negocio == "mercado":
            return redirect(url_for("dashboard_mercado"))
        else:
            flash("Seleccione un negocio válido", "danger")
            return redirect(url_for("seleccionar_negocio"))

    # ✅ Mostrar la página de selección con el negocio actual
    negocio_actual = session.get("negocio")
    return render_template("seleccionar_negocio.html", negocio_actual=negocio_actual)


# ---------------------------
# DASHBOARD FARMACIA
# ---------------------------
@app.route("/dashboard_farmacia")
def dashboard_farmacia():
    categorias = ["Analgésicos", "Antibióticos", "Vitaminas", "Otros"]
    ventas_categoria = [500, 300, 200, 100]
    proximos_vencer = [
        {"nombre": "Paracetamol", "lote": "A123", "vencimiento": "2026-05-10", "stock": 50},
        {"nombre": "Amoxicilina", "lote": "B456", "vencimiento": "2026-06-15", "stock": 30}
    ]

    # Depuración: imprime en consola
    print("Categorías:", categorias)
    print("Ventas por categoría:", ventas_categoria)

    return render_template("dashboard_farmacia.html",
                           categorias=categorias,
                           ventas_categoria=ventas_categoria,
                           proximos_vencer=proximos_vencer)
# ---------------------------
# DASHBOARD FERRETERÍA
# ---------------------------
@app.route("/dashboard_ferreteria")
def dashboard_ferreteria():
    meses = ["Enero", "Febrero", "Marzo", "Abril"]
    ventas = [800, 1200, 1500, 1000]
    materiales = [
        {"nombre": "Martillo", "unidad": "Unidad", "stock": 20, "precio": 15000},
        {"nombre": "Cemento", "unidad": "Kg", "stock": 100, "precio": 25000}
    ]
    bajo_stock = [m for m in materiales if m["stock"] < 30]

    # Depuración: imprime en consola
    print("Meses:", meses)
    print("Ventas ferretería:", ventas)
    print("Materiales:", materiales)
    print("Bajo stock:", bajo_stock)

    return render_template("dashboard_ferreteria.html",
                           meses=meses,
                           ventas=ventas,
                           materiales=materiales,
                           bajo_stock=bajo_stock)
# ---------------------------
# DASHBOARD MERCADO
# ---------------------------
@app.route("/dashboard_mercado")
def dashboard_mercado():
    productos = [
        {"nombre": "Manzanas", "stock": 100, "precio": 2000},
        {"nombre": "Plátanos", "stock": 80, "precio": 1500},
        {"nombre": "Tomates", "stock": 50, "precio": 2500}
    ]
    ventas_diarias = [20, 35, 40, 25]

    return render_template("dashboard_mercado.html",
                           productos=productos,
                           ventas_diarias=ventas_diarias)

# ---------------------------
# DASHBOARD TIENDA DE ROPA
# ---------------------------
@app.route("/dashboard_tienda_de_ropa")
def dashboard_tienda_de_ropa():
    categorias = ["Ropa", "Electrodomésticos", "Juguetes"]
    ventas_categoria = [300, 500, 200]

    return render_template("dashboard_tienda_de_ropa.html",
                           categorias=categorias,
                           ventas_categoria=ventas_categoria)


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
    """
    Muestra el inventario filtrado por el negocio actual.
    Cada producto está asociado a un negocio en la columna 'negocio'.
    """
    negocio_actual = session.get("negocio")

    if not negocio_actual:
        # Si no hay negocio en sesión, redirigimos al selector
        flash("Debes seleccionar un negocio antes de ver el inventario.", "warning")
        return redirect(url_for("seleccionar_negocio"))

    try:
        conn = get_db_connection()
        query = "SELECT * FROM productos WHERE negocio = ?"
        productos = conn.execute(query, (negocio_actual,)).fetchall()
    except Exception as e:
        # Manejo de errores más claro
        flash(f"Error al cargar inventario: {str(e)}", "danger")
        productos = []
    finally:
        conn.close()

    return render_template(
        "inventario.html",
        productos=productos,
        negocio_actual=negocio_actual
    )



# ---------------------------
# REGISTRAR PRODUCTO (ADMIN)
# ---------------------------
@app.route("/registrar_producto", methods=["GET", "POST"])
def registrar_producto():
    """
    Permite registrar un nuevo producto en el inventario del negocio actual.
    Solo los usuarios con rol 'admin' pueden acceder.
    """

    # Validar rol
    if session.get("rol") != "admin":
        flash("No tienes permisos para registrar productos.", "danger")
        return redirect(url_for("inventario"))

    negocio_actual = session.get("negocio")
    if not negocio_actual:
        flash("Debes seleccionar un negocio antes de registrar productos.", "warning")
        return redirect(url_for("seleccionar_negocio"))

    if request.method == "POST":
        try:
            # Capturar y limpiar datos del formulario
            nombre = request.form["nombre"].strip()
            categoria = request.form["categoria"].strip()
            precio = float(request.form["precio"])
            cantidad = int(request.form["cantidad"])
            proveedor = request.form.get("proveedor", "").strip()
            codigo_barras = request.form.get("codigo_barras", "").strip()  # ✅ Nuevo campo

            # Guardar producto asociado al negocio actual
            conn = get_db_connection()
            query = """
                INSERT INTO productos (nombre, categoria, precio, cantidad, proveedor, codigo_barras, negocio)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            conn.execute(query, (nombre, categoria, precio, cantidad, proveedor, codigo_barras, negocio_actual))
            conn.commit()
            flash(f"Producto '{nombre}' registrado en {negocio_actual}.", "success")

        except Exception as e:
            flash(f"Error al registrar producto: {str(e)}", "danger")
        finally:
            conn.close()

        return redirect(url_for("inventario"))

    # Renderizar formulario con contexto del negocio
    return render_template("registrar_producto.html", negocio_actual=negocio_actual)



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
        try:
            import json
            carrito_json = request.form.get("carrito")
            carrito = json.loads(carrito_json) if carrito_json else []

            cliente = request.form.get("cliente", "Consumidor Final")
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if not carrito:
                flash("El carrito está vacío, no se puede registrar la venta.", "danger")
                conn.close()
                return redirect(url_for("registrar_venta"))

            # ✅ Calcular total acumulado
            total_venta = sum(float(item["precio"]) * int(item["cantidad"]) for item in carrito)

            # 1️⃣ Insertar cabecera de la venta
            cur = conn.execute(
                "INSERT INTO ventas (fecha, cliente, total, usuario_id) VALUES (?, ?, ?, ?)",
                (fecha, cliente, total_venta, session.get("usuario_id") or 0)
            )
            venta_id = cur.lastrowid  # obtener el ID de la venta recién creada

            # 2️⃣ Insertar detalle de la venta
            for item in carrito:
                producto_id = int(item["id"])
                cantidad = int(item["cantidad"])
                precio = float(item["precio"])

                conn.execute(
                    "INSERT INTO detalle_ventas (venta_id, producto_id, cantidad, precio) VALUES (?, ?, ?, ?)",
                    (venta_id, producto_id, cantidad, precio)
                )

                # 3️⃣ Actualizar stock
                conn.execute(
                    "UPDATE productos SET cantidad = cantidad - ? WHERE id = ?",
                    (cantidad, producto_id)
                )

            conn.commit()
            flash(f"Venta registrada con éxito. Total: ${total_venta:,.2f}", "success")

        except Exception as e:
            flash(f"Error al registrar la venta: {str(e)}", "danger")
        finally:
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
        SELECT v.id,
               v.fecha,
               v.cliente,
               v.total,
               u.nombre AS vendedor
        FROM ventas v
        LEFT JOIN usuarios u ON v.usuario_id = u.id
        ORDER BY v.fecha DESC
    """).fetchall()
    conn.close()
    return render_template("ventas.html", ventas=ventas)


#----------------------------
# Detalle de venta
#----------------------------
@app.route("/ventas/<int:venta_id>")
def detalle_venta(venta_id):
    conn = get_db_connection()

    # Traer cabecera de la venta
    venta = conn.execute("""
        SELECT v.id, v.fecha, v.cliente, v.total, u.nombre AS vendedor
        FROM ventas v
        LEFT JOIN usuarios u ON v.usuario_id = u.id
        WHERE v.id = ?
    """, (venta_id,)).fetchone()

    # Traer detalle de productos
    detalle = conn.execute("""
        SELECT d.producto_id, p.nombre AS producto, d.cantidad, d.precio
        FROM detalle_ventas d
        JOIN productos p ON d.producto_id = p.id
        WHERE d.venta_id = ?
    """, (venta_id,)).fetchall()

    conn.close()
    return render_template("detalle_venta.html", venta=venta, detalle=detalle)


# ---------------------------
# Exportar ventas a Excel
# ---------------------------
@app.route("/ventas/export/excel")
def exportar_ventas_excel():
    import pandas as pd
    conn = get_db_connection()
    ventas = conn.execute("""
        SELECT v.id, v.fecha, v.cliente, v.total, u.nombre AS vendedor
        FROM ventas v
        LEFT JOIN usuarios u ON v.usuario_id = u.id
        ORDER BY v.fecha DESC
    """).fetchall()
    conn.close()

    # Convertir a DataFrame
    df = pd.DataFrame(ventas, columns=["id", "fecha", "cliente", "total", "vendedor"])

    # Guardar en Excel
    filename = "ventas.xlsx"
    df.to_excel(filename, index=False)

    return send_file(filename, as_attachment=True)


# ---------------------------
# Exportar ventas a PDF
# ---------------------------
@app.route("/ventas/export/pdf")
def exportar_ventas_pdf():
    from fpdf import FPDF
    conn = get_db_connection()

    # Traer todas las ventas
    ventas = conn.execute("""
        SELECT v.id, v.fecha, v.cliente, v.total, u.nombre AS vendedor
        FROM ventas v
        LEFT JOIN usuarios u ON v.usuario_id = u.id
        ORDER BY v.fecha DESC
    """).fetchall()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Reporte de Ventas", ln=True, align="C")
    pdf.ln(10)

    # Recorrer cada venta
    for v in ventas:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, f"Venta #{v['id']} - Cliente: {v['cliente']} - Total: ${v['total']:,.2f}", ln=True)
        pdf.set_font("Arial", size=10)
        pdf.cell(200, 8, f"Fecha: {v['fecha']} | Vendedor: {v['vendedor'] if v['vendedor'] else 'N/A'}", ln=True)

        # Traer detalle de productos
        detalle = conn.execute("""
            SELECT d.cantidad, d.precio, p.nombre AS producto
            FROM detalle_ventas d
            JOIN productos p ON d.producto_id = p.id
            WHERE d.venta_id = ?
        """, (v["id"],)).fetchall()

        # Listar productos
        for d in detalle:
            subtotal = d["cantidad"] * d["precio"]
            pdf.cell(200, 8, f"- {d['producto']} | Cant: {d['cantidad']} | Precio: ${d['precio']:,.2f} | Subtotal: ${subtotal:,.2f}", ln=True)

        pdf.ln(5)  # espacio entre ventas

    conn.close()

    filename = "ventas_detalle.pdf"
    pdf.output(filename)

    return send_file(filename, as_attachment=True)



# ---------------------------
# Reporte
# ---------------------------
@app.route("/reporte")
def reporte():
    conn = get_db_connection()
    ventas = conn.execute("""
        SELECT dv.cantidad, dv.precio, p.nombre
        FROM detalle_ventas dv
        JOIN productos p ON dv.producto_id = p.id
    """).fetchall()
    conn.close()

    # ✅ Calcular ganancias totales
    ganancias = sum(v["cantidad"] * v["precio"] for v in ventas)

    # ✅ Agrupar productos vendidos
    productos_vendidos = {}
    precios_productos = {}

    for v in ventas:
        productos_vendidos[v["nombre"]] = productos_vendidos.get(v["nombre"], 0) + v["cantidad"]
        precios_productos[v["nombre"]] = v["precio"]

    # ✅ Ordenar productos más vendidos
    productos_top = sorted(productos_vendidos.items(), key=lambda x: x[1], reverse=True)
    precios_lista = [precios_productos[p[0]] for p in productos_top]

    return render_template(
        "reporte.html",
        ganancias=ganancias,
        productos_top=productos_top,
        precios_productos=precios_lista,
        negocio_actual="farmacia"  # ⚠️ Ajusta según tu sesión o negocio actual
    )

# ---------------------------
# MAIN
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)