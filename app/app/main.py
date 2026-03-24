import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
from app.crud import registrar_usuario, listar_usuarios, actualizar_usuario, borrar_usuario

def registrar():
    nombre = entry_nombre.get()
    correo = entry_correo.get()
    usuarios = listar_usuarios()
    if any(u['correo'] == correo for u in usuarios):
        messagebox.showerror("Error", "El correo ya existe en la base de datos")
        return

    resultado = registrar_usuario(nombre, correo)
    if "message" in resultado:
        messagebox.showerror("Error", resultado["message"])
    else:
        messagebox.showinfo("Éxito", "Usuario registrado correctamente")
        listar()

def listar():
    # Limpiar tabla
    for item in tree.get_children():
        tree.delete(item)

    resultado = listar_usuarios()
    if isinstance(resultado, list):
        for u in resultado:
            tree.insert("", tk.END, values=(u['nombre'], u['correo']))
    else:
        messagebox.showerror("Error", str(resultado))

def actualizar():
    correo = entry_correo.get()
    nuevo_nombre = entry_nombre.get()
    resultado = actualizar_usuario(correo, nuevo_nombre)
    if "message" in resultado:
        messagebox.showerror("Error", resultado["message"])
    else:
        messagebox.showinfo("Éxito", "Usuario actualizado correctamente")
        listar()

def borrar():
    correo = entry_correo.get()
    resultado = borrar_usuario(correo)
    if resultado == 204:
        messagebox.showinfo("Éxito", "Usuario borrado correctamente")
        listar()
    else:
        messagebox.showerror("Error", f"No se pudo borrar (código {resultado})")

def exportar_csv():
    archivo = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")])
    if archivo:
        with open(archivo, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Nombre", "Correo"])
            for item in tree.get_children():
                fila = tree.item(item)["values"]
                writer.writerow(fila)
        messagebox.showinfo("Éxito", f"Usuarios exportados a {archivo}")

def importar_csv():
    archivo = filedialog.askopenfilename(filetypes=[("CSV files","*.csv")])
    if archivo:
        usuarios_existentes = listar_usuarios()
        correos_existentes = {u['correo'] for u in usuarios_existentes}

        with open(archivo, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for fila in reader:
                nombre = fila.get("Nombre")
                correo = fila.get("Correo")
                if nombre and correo and correo not in correos_existentes:
                    registrar_usuario(nombre, correo)
                    correos_existentes.add(correo)
        messagebox.showinfo("Éxito", f"Usuarios importados desde {archivo}")
        listar()

def buscar():
    criterio = entry_buscar.get().lower()
    for item in tree.get_children():
        tree.delete(item)

    resultado = listar_usuarios()
    if isinstance(resultado, list):
        for u in resultado:
            if criterio in u['nombre'].lower() or criterio in u['correo'].lower():
                tree.insert("", tk.END, values=(u['nombre'], u['correo']))
    else:
        messagebox.showerror("Error", str(resultado))

# Ventana principal
root = tk.Tk()
root.title("VentasApp - Usuarios")

# Campos de entrada
tk.Label(root, text="Nombre").grid(row=0, column=0)
entry_nombre = tk.Entry(root)
entry_nombre.grid(row=0, column=1)

tk.Label(root, text="Correo").grid(row=1, column=0)
entry_correo = tk.Entry(root)
entry_correo.grid(row=1, column=1)

# Botones CRUD
tk.Button(root, text="Registrar", command=registrar).grid(row=2, column=0)
tk.Button(root, text="Listar", command=listar).grid(row=2, column=1)
tk.Button(root, text="Actualizar", command=actualizar).grid(row=2, column=2)
tk.Button(root, text="Borrar", command=borrar).grid(row=2, column=3)
tk.Button(root, text="Exportar CSV", command=exportar_csv).grid(row=2, column=4)
tk.Button(root, text="Importar CSV", command=importar_csv).grid(row=2, column=5)

# Campo de búsqueda
tk.Label(root, text="Buscar").grid(row=3, column=0)
entry_buscar = tk.Entry(root)
entry_buscar.grid(row=3, column=1)
tk.Button(root, text="Filtrar", command=buscar).grid(row=3, column=2)

# Tabla tipo Excel (Treeview)
tree = ttk.Treeview(root, columns=("Nombre", "Correo"), show="headings")
tree.heading("Nombre", text="Nombre")
tree.heading("Correo", text="Correo")
tree.grid(row=4, column=0, columnspan=6)

root.mainloop()