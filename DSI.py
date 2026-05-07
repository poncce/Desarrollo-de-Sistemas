import tkinter as tk
from tkinter import ttk, messagebox
import os

ARCHIVO = "clientes.txt"


def crear_archivo():
    if not os.path.exists(ARCHIVO):
        open(ARCHIVO, "w").close()


def limpiar_campos():
    codigo.set("")
    nombre.set("")
    apellido.set("")
    dni.set("")
    direccion.set("")
    estado.set("ACTIVO")


def leer_clientes():
    crear_archivo()
    clientes = []

    with open(ARCHIVO, "r") as archivo:
        for linea in archivo:
            datos = linea.strip().split("|")
            if len(datos) == 6:
                clientes.append(datos)

    return clientes


def guardar_clientes(clientes):
    with open(ARCHIVO, "w") as archivo:
        for cliente in clientes:
            archivo.write("|".join(cliente) + "\n")


def cargar_tabla():
    for fila in tabla.get_children():
        tabla.delete(fila)

    for cliente in leer_clientes():
        tabla.insert("", "end", values=cliente)


def validar_campos(validar_id=True):
    """
    Valida todos los campos del formulario.
    Retorna True si todo es correcto, False si hay algún error.
    """
    if validar_id:
        if codigo.get().strip() == "":
            messagebox.showwarning("Atención", "Debe completar el campo Identificador.")
            return False
        if not codigo.get().strip().isdigit():
            messagebox.showwarning("Atención", "El Identificador debe ser un valor numérico.")
            return False

    if nombre.get().strip() == "":
        messagebox.showwarning("Atención", "Debe completar el campo Nombre.")
        return False

    if apellido.get().strip() == "":
        messagebox.showwarning("Atención", "Debe completar el campo Apellido.")
        return False

    if dni.get().strip() == "":
        messagebox.showwarning("Atención", "Debe completar el campo DNI.")
        return False
    if not dni.get().strip().isdigit():
        messagebox.showwarning("Atención", "El DNI debe ser un valor numérico.")
        return False

    if direccion.get().strip() == "":
        messagebox.showwarning("Atención", "Debe completar el campo Dirección.")
        return False

    return True


def alta_cliente():
    if not validar_campos(validar_id=True):
        return

    clientes = leer_clientes()

    for cliente in clientes:
        if cliente[0] == codigo.get().strip():
            messagebox.showerror("Error", "El Identificador ya existe.")
            return

    nuevo = [
        codigo.get().strip(),
        nombre.get().strip(),
        apellido.get().strip(),
        dni.get().strip(),
        direccion.get().strip(),
        estado.get()
    ]

    clientes.append(nuevo)
    guardar_clientes(clientes)
    cargar_tabla()
    limpiar_campos()

    messagebox.showinfo("Alta", "Cliente dado de alta correctamente.")


def baja_cliente():
    if codigo.get().strip() == "":
        messagebox.showwarning("Atención", "Ingrese el Identificador del cliente.")
        return
    if not codigo.get().strip().isdigit():
        messagebox.showwarning("Atención", "El Identificador debe ser un valor numérico.")
        return

    clientes = leer_clientes()
    encontrado = False

    for cliente in clientes:
        if cliente[0] == codigo.get().strip():
            cliente[5] = "BAJA"
            encontrado = True

    guardar_clientes(clientes)
    cargar_tabla()

    if encontrado:
        messagebox.showinfo("Baja", "Cliente dado de baja correctamente.")
    else:
        messagebox.showerror("Error", "Cliente no encontrado.")


def modificar_cliente():
    if codigo.get().strip() == "":
        messagebox.showwarning("Atención", "Ingrese el Identificador del cliente.")
        return

    if not validar_campos(validar_id=True):
        return

    clientes = leer_clientes()
    encontrado = False

    for cliente in clientes:
        if cliente[0] == codigo.get().strip():
            cliente[1] = nombre.get().strip()
            cliente[2] = apellido.get().strip()
            cliente[3] = dni.get().strip()
            cliente[4] = direccion.get().strip()
            cliente[5] = estado.get()
            encontrado = True

    guardar_clientes(clientes)
    cargar_tabla()

    if encontrado:
        messagebox.showinfo("Modificación", "Cliente modificado correctamente.")
    else:
        messagebox.showerror("Error", "Cliente no encontrado.")


def seleccionar_cliente(event):
    seleccionado = tabla.focus()

    if seleccionado:
        valores = tabla.item(seleccionado, "values")

        codigo.set(valores[0])
        nombre.set(valores[1])
        apellido.set(valores[2])
        dni.set(valores[3])
        direccion.set(valores[4])
        estado.set(valores[5])


# Ventana principal
ventana = tk.Tk()
ventana.title("Gestión de Clientes")
ventana.geometry("900x600")
ventana.resizable(False, False)
ventana.configure(bg="#f4f6fa")

# Variables
codigo = tk.StringVar()
nombre = tk.StringVar()
apellido = tk.StringVar()
dni = tk.StringVar()
direccion = tk.StringVar()
estado = tk.StringVar(value="ACTIVO")

# Título
titulo = tk.Label(
    ventana,
    text="GESTIÓN DE CLIENTES",
    font=("Arial", 22, "bold"),
    bg="#f4f6fa",
    fg="#172033"
)
titulo.pack(pady=15)

# Marco formulario
frame_form = tk.Frame(ventana, bg="white", padx=20, pady=20)
frame_form.place(x=30, y=80, width=390, height=430)

tk.Label(frame_form, text="Datos del cliente", font=("Arial", 14, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=10)

tk.Label(frame_form, text="Identificador:", bg="white").grid(row=1, column=0, sticky="w", pady=5)
tk.Entry(frame_form, textvariable=codigo, width=30).grid(row=1, column=1, pady=5)

tk.Label(frame_form, text="Nombre:", bg="white").grid(row=2, column=0, sticky="w", pady=5)
tk.Entry(frame_form, textvariable=nombre, width=30).grid(row=2, column=1, pady=5)

tk.Label(frame_form, text="Apellido:", bg="white").grid(row=3, column=0, sticky="w", pady=5)
tk.Entry(frame_form, textvariable=apellido, width=30).grid(row=3, column=1, pady=5)

tk.Label(frame_form, text="DNI:", bg="white").grid(row=4, column=0, sticky="w", pady=5)
tk.Entry(frame_form, textvariable=dni, width=30).grid(row=4, column=1, pady=5)

tk.Label(frame_form, text="Dirección:", bg="white").grid(row=5, column=0, sticky="w", pady=5)
tk.Entry(frame_form, textvariable=direccion, width=30).grid(row=5, column=1, pady=5)

tk.Label(frame_form, text="Estado:", bg="white").grid(row=6, column=0, sticky="w", pady=5)
ttk.Combobox(
    frame_form,
    textvariable=estado,
    values=["ACTIVO", "BAJA"],
    state="readonly",
    width=27
).grid(row=6, column=1, pady=5)

# Botones
tk.Button(frame_form, text="Alta", width=12, bg="#16A34A", fg="white", command=alta_cliente).grid(row=7, column=0, pady=15)
tk.Button(frame_form, text="Modificar", width=12, bg="#2563EB", fg="white", command=modificar_cliente).grid(row=7, column=1, pady=15)

tk.Button(frame_form, text="Baja", width=12, bg="#DC2626", fg="white", command=baja_cliente).grid(row=8, column=0, pady=5)
tk.Button(frame_form, text="Limpiar", width=12, bg="#6B7280", fg="white", command=limpiar_campos).grid(row=8, column=1, pady=5)

# Tabla
frame_tabla = tk.Frame(ventana, bg="white")
frame_tabla.place(x=445, y=80, width=430, height=430)

tabla = ttk.Treeview(
    frame_tabla,
    columns=("identificador", "nombre", "apellido", "dni", "direccion", "estado"),
    show="headings"
)

tabla.heading("identificador", text="Identificador")
tabla.heading("nombre", text="Nombre")
tabla.heading("apellido", text="Apellido")
tabla.heading("dni", text="DNI")
tabla.heading("direccion", text="Dirección")
tabla.heading("estado", text="Estado")

tabla.column("identificador", width=80)
tabla.column("nombre", width=70)
tabla.column("apellido", width=75)
tabla.column("dni", width=70)
tabla.column("direccion", width=80)
tabla.column("estado", width=60)

tabla.pack(fill="both", expand=True)
tabla.bind("<<TreeviewSelect>>", seleccionar_cliente)

# Botón salir
tk.Button(
    ventana,
    text="Salir",
    width=15,
    bg="#111827",
    fg="white",
    command=ventana.destroy
).place(x=745, y=530)

crear_archivo()
cargar_tabla()

ventana.mainloop()