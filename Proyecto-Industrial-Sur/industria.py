"""
INDUSTRIAL DEL SUR - Sistema de Gestión Textil
================================================
Entidades: Proveedores, Productos,
           Ventas, Facturas
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os

# ═══════════════════════════════════════════════════════════════════
#  PALETA
# ═══════════════════════════════════════════════════════════════════
BG       = "#0D1117"
SIDEBAR  = "#161B22"
CARD     = "#1C2128"
BORDER   = "#30363D"
TEXT     = "#E6EDF3"
MUTED    = "#7D8590"
ACCENT   = "#58A6FF"
GREEN    = "#3FB950"
RED      = "#F85149"
YELLOW   = "#D29922"
PURPLE   = "#BC8CFF"
ROW_ODD  = "#1C2128"
ROW_EVEN = "#22272E"
SEL      = "#1F6FEB"

# Solo entidades restantes
META = {
    "proveedores": ("#3FB950", "🏭"),
    "productos":   ("#D29922", "🧵"),
    "ventas":      ("#BC8CFF", "💰"),
    "facturas":    ("#39D353", "🧾"),
}

# ═══════════════════════════════════════════════════════════════════
#  ARCHIVOS
# ═══════════════════════════════════════════════════════════════════
ARCHIVOS = {k: f"ids_{k}.txt" for k in META}


def crear_archivo(ent):
    if not os.path.exists(ARCHIVOS[ent]):
        open(ARCHIVOS[ent], "w", encoding="utf-8").close()


def leer(ent):
    crear_archivo(ent)
    rows = []
    with open(ARCHIVOS[ent], encoding="utf-8") as f:
        for ln in f:
            d = ln.strip().split("|")
            if d and d[0]:
                rows.append(d)
    return rows


def guardar(ent, rows):
    with open(ARCHIVOS[ent], "w", encoding="utf-8") as f:
        for r in rows:
            f.write("|".join(r) + "\n")


# ═══════════════════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════════════════

def entry(parent, var, accent):
    return tk.Entry(
        parent, textvariable=var, width=28,
        bg="#0D1117", fg=TEXT, insertbackground=TEXT,
        relief="flat", font=("Consolas", 9),
        highlightthickness=1,
        highlightbackground=BORDER,
        highlightcolor=accent,
    )


def combo(parent, var, values):
    style_name = "Dark.TCombobox"
    style = ttk.Style()

    style.configure(
        style_name,
        fieldbackground="#0D1117",
        background=CARD,
        foreground=TEXT
    )

    cb = ttk.Combobox(
        parent,
        textvariable=var,
        values=values,
        state="readonly",
        width=26
    )

    cb.configure(style=style_name)

    if values:
        var.set(values[0])

    return cb


def btn(parent, text, color, cmd, w=11):
    return tk.Button(
        parent,
        text=text,
        command=cmd,
        bg=color,
        fg=TEXT,
        relief="flat",
        width=w
    )


# ═══════════════════════════════════════════════════════════════════
#  BASE ABM
# ═══════════════════════════════════════════════════════════════════

class ABMBase(tk.Frame):

    entidad = ""
    titulo = ""
    campos = []
    columnas = []
    numericos = set()

    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)

        self.controller = controller
        self.vars = {c[1]: tk.StringVar() for c in self.campos}

        self._build()
        self.recargar()

    def _build(self):

        color, icon = META[self.entidad]

        tk.Label(
            self,
            text=f"{icon} {self.titulo}",
            bg=BG,
            fg=color,
            font=("Segoe UI", 18, "bold")
        ).pack(pady=12)

        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True)

        # FORM
        form = tk.Frame(body, bg=CARD)
        form.pack(side="left", fill="y", padx=10, pady=10)

        for i, (label, key, tipo, *opts) in enumerate(self.campos):

            tk.Label(
                form,
                text=label,
                bg=CARD,
                fg=TEXT
            ).grid(row=i, column=0, sticky="w", padx=8, pady=5)

            if tipo == "combo":
                w = combo(form, self.vars[key], opts[0])
            else:
                w = entry(form, self.vars[key], color)

            w.grid(row=i, column=1, padx=8, pady=5)

        # BOTONES
        bf = tk.Frame(form, bg=CARD)
        bf.grid(row=len(self.campos)+1, column=0, columnspan=2, pady=10)

        btn(bf, "Alta", GREEN, self.alta).grid(row=0, column=0, padx=5)
        btn(bf, "Modificar", ACCENT, self.modificar).grid(row=0, column=1, padx=5)
        btn(bf, "Baja", RED, self.baja).grid(row=0, column=2, padx=5)

        # TABLA
        tabla_frame = tk.Frame(body, bg=BG)
        tabla_frame.pack(side="left", fill="both", expand=True)

        cols = [c[0] for c in self.columnas]

        self.tabla = ttk.Treeview(
            tabla_frame,
            columns=cols,
            show="headings"
        )

        for col, w in self.columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=w)

        self.tabla.pack(fill="both", expand=True)

    def _vals(self):
        return [self.vars[c[1]].get() for c in self.campos]

    def _id(self):
        return self.vars[self.campos[0][1]].get()

    def recargar(self):

        for r in self.tabla.get_children():
            self.tabla.delete(r)

        for row in leer(self.entidad):
            self.tabla.insert("", "end", values=row)

    def alta(self):

        rows = leer(self.entidad)

        rows.append(self._vals())

        guardar(self.entidad, rows)

        self.recargar()

    def baja(self):

        rows = leer(self.entidad)

        rows = [r for r in rows if r[0] != self._id()]

        guardar(self.entidad, rows)

        self.recargar()

    def modificar(self):

        rows = leer(self.entidad)

        for i, r in enumerate(rows):
            if r[0] == self._id():
                rows[i] = self._vals()

        guardar(self.entidad, rows)

        self.recargar()


# ═══════════════════════════════════════════════════════════════════
#  ENTIDADES
# ═══════════════════════════════════════════════════════════════════

class Proveedores(ABMBase):

    entidad = "proveedores"
    titulo = "Gestión de Proveedores"

    campos = [
        ("ID", "id", "entry"),
        ("Razón Social", "razon", "entry"),
        ("CUIT", "cuit", "entry"),
        ("Teléfono", "tel", "entry"),
    ]

    columnas = [
        ("ID", 60),
        ("Razón Social", 180),
        ("CUIT", 120),
        ("Teléfono", 120),
    ]


class Productos(ABMBase):

    entidad = "productos"
    titulo = "Gestión de Productos"

    campos = [
        ("Código", "id", "entry"),
        ("Descripción", "desc", "entry"),
        ("Categoría", "cat", "combo",
         ["Remeras", "Pantalones", "Vestidos"]),
        ("Precio", "precio", "entry"),
    ]

    columnas = [
        ("Código", 80),
        ("Descripción", 200),
        ("Categoría", 120),
        ("Precio", 100),
    ]


class Ventas(ABMBase):

    entidad = "ventas"
    titulo = "Gestión de Ventas"

    campos = [
        ("Nro Venta", "id", "entry"),
        ("Fecha", "fecha", "entry"),
        ("Producto", "producto", "entry"),
        ("Cantidad", "cant", "entry"),
        ("Total", "total", "entry"),
    ]

    columnas = [
        ("Nro", 70),
        ("Fecha", 100),
        ("Producto", 160),
        ("Cantidad", 80),
        ("Total", 100),
    ]


class Facturas(ABMBase):

    entidad = "facturas"
    titulo = "Gestión de Facturas"

    campos = [
        ("Nro Factura", "id", "entry"),
        ("Fecha", "fecha", "entry"),
        ("Tipo", "tipo", "combo", ["A", "B", "C"]),
        ("Total", "total", "entry"),
    ]

    columnas = [
        ("Nro", 70),
        ("Fecha", 100),
        ("Tipo", 60),
        ("Total", 100),
    ]


# ═══════════════════════════════════════════════════════════════════
#  DASHBOARD
# ═══════════════════════════════════════════════════════════════════

class Dashboard(tk.Frame):

    MODULOS = [
        ("proveedores", "Proveedores", "Proveedores"),
        ("productos", "Productos", "Productos"),
        ("ventas", "Ventas", "Ventas"),
        ("facturas", "Facturas", "Facturas"),
    ]

    def __init__(self, parent, controller):

        super().__init__(parent, bg=BG)

        self.controller = controller

        tk.Label(
            self,
            text="Industrial del Sur",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 24, "bold")
        ).pack(pady=30)

        for key, label, pantalla in self.MODULOS:

            color, icon = META[key]

            b = tk.Button(
                self,
                text=f"{icon} {label}",
                bg=CARD,
                fg=color,
                relief="flat",
                width=25,
                height=2,
                command=lambda p=pantalla: controller.mostrar(p)
            )

            b.pack(pady=8)


# ═══════════════════════════════════════════════════════════════════
#  APP
# ═══════════════════════════════════════════════════════════════════

class App(tk.Tk):

    PANTALLAS = [
        ("Dashboard", Dashboard),
        ("Proveedores", Proveedores),
        ("Productos", Productos),
        ("Ventas", Ventas),
        ("Facturas", Facturas),
    ]

    def __init__(self):

        super().__init__()

        self.title("Industrial del Sur")
        self.geometry("1100x650")
        self.configure(bg=BG)

        self.area = tk.Frame(self, bg=BG)
        self.area.pack(fill="both", expand=True)

        self.frames = {}

        for name, Cls in self.PANTALLAS:

            f = Cls(self.area, self)

            self.frames[name] = f

            f.place(relwidth=1, relheight=1)

        self.mostrar("Dashboard")

    def mostrar(self, nombre):

        self.frames[nombre].lift()


# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":

    for k in META:
        crear_archivo(k)

    App().mainloop()