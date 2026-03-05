from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Función auxiliar para conectar a la base de datos
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# Página principal
@app.route("/")
def index():
    return render_template("index.html")

# Inventario: listar productos con alerta de stock bajo
@app.route("/inventario")
def inventario():
    conn = get_db_connection()
    productos = conn.execute("SELECT * FROM productos").fetchall()
    conn.close()
    return render_template("inventario.html", productos=productos)

# Registrar producto
@app.route("/registrar_producto", methods=["GET", "POST"])
def registrar_producto():
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

# Editar producto
@app.route("/editar_producto/<int:id>", methods=["GET", "POST"])
def editar_producto(id):
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
    return render_template("registrar_producto.html", producto=producto)

# Eliminar producto
@app.route("/eliminar_producto/<int:id>", methods=["POST"])
def eliminar_producto(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM productos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("inventario"))

# Registrar venta
@app.route("/registrar_venta", methods=["GET", "POST"])
def registrar_venta():
    conn = get_db_connection()
    productos = conn.execute("SELECT * FROM productos").fetchall()

    if request.method == "POST":
        producto_id = int(request.form["producto_id"])
        cantidad = int(request.form["cantidad"])
        cliente = request.form["cliente"]
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Insertar venta
        conn.execute(
            "INSERT INTO ventas (producto_id, fecha, cantidad, cliente) VALUES (?, ?, ?, ?)",
            (producto_id, fecha, cantidad, cliente),
        )

        # Actualizar inventario
        conn.execute(
            "UPDATE productos SET cantidad = cantidad - ? WHERE id = ?",
            (cantidad, producto_id),
        )

        conn.commit()
        conn.close()
        return redirect(url_for("ventas"))

    conn.close()
    return render_template("registrar_venta.html", productos=productos)

# Listar ventas
@app.route("/ventas")
def ventas():
    conn = get_db_connection()
    ventas = conn.execute("""
        SELECT v.id, v.fecha, v.cantidad, v.cliente, p.nombre, p.precio
        FROM ventas v
        JOIN productos p ON v.producto_id = p.id
    """).fetchall()
    conn.close()
    return render_template("ventas.html", ventas=ventas)

# Reporte de ganancias y productos más vendidos
@app.route("/reporte")
def reporte():
    conn = get_db_connection()
    ventas = conn.execute("""
        SELECT v.cantidad, p.precio, p.nombre
        FROM ventas v
        JOIN productos p ON v.producto_id = p.id
    """).fetchall()
    conn.close()

    # Calcular ganancias totales
    ganancias = sum(v["cantidad"] * v["precio"] for v in ventas)

    # Calcular productos más vendidos y precios
    productos_vendidos = {}
    precios_productos = {}
    for v in ventas:
        productos_vendidos[v["nombre"]] = productos_vendidos.get(v["nombre"], 0) + v["cantidad"]
        precios_productos[v["nombre"]] = v["precio"]

    # Ordenar productos por cantidad vendida
    productos_top = sorted(productos_vendidos.items(), key=lambda x: x[1], reverse=True)
    precios_lista = [precios_productos[p[0]] for p in productos_top]

    return render_template(
        "reporte.html",
        ganancias=ganancias,
        productos_top=productos_top,
        precios_productos=precios_lista
    )

if __name__ == "__main__":
    app.run(debug=True)