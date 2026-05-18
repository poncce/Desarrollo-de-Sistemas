"""
INDUSTRIAL DEL SUR - Sistema de Gestión Textil
================================================
Entidades: Clientes, Proveedores, Productos,
           Compras, Ventas, Facturas, Stock
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
from datetime import date

# ═══════════════════════════════════════════════════════════════════
#  PALETA  (tema oscuro industrial)
# ═══════════════════════════════════════════════════════════════════
BG       = "#0D1117"
SIDEBAR  = "#161B22"
CARD     = "#1C2128"
BORDER   = "#30363D"
TEXT     = "#E6EDF3"
MUTED    = "#7D8590"
ACCENT   = "#58A6FF"   # azul GitHub
GREEN    = "#3FB950"
RED      = "#F85149"
YELLOW   = "#D29922"
PURPLE   = "#BC8CFF"
ORANGE   = "#F0883E"
TEAL     = "#39D353"
ROW_ODD  = "#1C2128"
ROW_EVEN = "#22272E"
SEL      = "#1F6FEB"

# Color e ícono por módulo
META = {
    "clientes":    ("#58A6FF", "👥"),
    "proveedores": ("#3FB950", "🏭"),
    "productos":   ("#D29922", "🧵"),
    "compras":     ("#F0883E", "🛒"),
    "ventas":      ("#BC8CFF", "💰"),
    "facturas":    ("#39D353", "🧾"),
    "stock":       ("#F85149", "📊"),
}

HOY = date.today().strftime("%d/%m/%Y")

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
#  WIDGET HELPERS
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
    style.configure(style_name,
                    fieldbackground="#0D1117",
                    background=CARD,
                    foreground=TEXT,
                    selectbackground=SEL)
    cb = ttk.Combobox(parent, textvariable=var, values=values,
                      state="readonly", width=26,
                      font=("Consolas", 9))
    cb.configure(style=style_name)
    if values:
        var.set(values[0])
    return cb


def btn(parent, text, color, cmd, w=11):
    dark_fg = color in (GREEN, YELLOW, TEAL, ORANGE)
    return tk.Button(
        parent, text=text, command=cmd,
        bg=color, fg="#0D1117" if dark_fg else TEXT,
        font=("Segoe UI", 9, "bold"),
        relief="flat", bd=0, width=w, pady=6,
        activebackground=color, cursor="hand2",
    )


# ═══════════════════════════════════════════════════════════════════
#  CLASE BASE ABM
# ═══════════════════════════════════════════════════════════════════

class ABMBase(tk.Frame):
    """
    Subclases declaran:
      entidad  : str
      titulo   : str
      campos   : list[ (label, key, "entry"|"combo", [opts]) ]
      columnas : list[ (header, width) ]
      numericos: set de keys que deben ser dígitos
    """
    entidad   = ""
    titulo    = ""
    campos    = []
    columnas  = []
    numericos = set()

    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self.vars = {c[1]: tk.StringVar() for c in self.campos}
        self._init_defaults()
        self._build()
        self.recargar()

    def _init_defaults(self):
        for label, key, tipo, *opts in self.campos:
            if tipo == "combo" and opts and opts[0]:
                self.vars[key].set(opts[0][0])

    # ── UI ────────────────────────────────────────────────────────

    def _build(self):
        color, icon = META.get(self.entidad, (ACCENT, ""))

        # ── Encabezado
        hdr = tk.Frame(self, bg=SIDEBAR, pady=10)
        hdr.pack(fill="x")
        tk.Label(hdr, text=f"{icon}  {self.titulo}",
                 font=("Segoe UI", 16, "bold"),
                 bg=SIDEBAR, fg=color).pack(side="left", padx=24)

        # ── Cuerpo
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=16, pady=10)

        # ── Formulario
        card_f = tk.Frame(body, bg=CARD,
                          highlightthickness=1, highlightbackground=color)
        card_f.pack(side="left", fill="y", padx=(0, 14), ipadx=14, ipady=14)

        tk.Label(card_f, text="Datos del registro",
                 font=("Segoe UI", 10, "bold"),
                 bg=CARD, fg=color).grid(row=0, column=0, columnspan=2,
                                          pady=(10, 14), padx=10, sticky="w")

        for i, (label, key, tipo, *opts) in enumerate(self.campos, 1):
            tk.Label(card_f, text=label + ":", font=("Consolas", 9),
                     bg=CARD, fg=MUTED, anchor="w"
                     ).grid(row=i, column=0, sticky="w", padx=(10, 4), pady=3)

            if tipo == "combo":
                w = combo(card_f, self.vars[key], opts[0] if opts else [])
            else:
                w = entry(card_f, self.vars[key], color)
            w.grid(row=i, column=1, pady=3, padx=(0, 10))

        # Botones acción
        bf = tk.Frame(card_f, bg=CARD)
        bf.grid(row=len(self.campos) + 1, column=0, columnspan=2, pady=16)
        btn(bf, "Alta",      GREEN,  self.alta     ).grid(row=0, column=0, padx=4, pady=3)
        btn(bf, "Modificar", ACCENT, self.modificar).grid(row=0, column=1, padx=4, pady=3)
        btn(bf, "Baja",      RED,    self.baja     ).grid(row=1, column=0, padx=4, pady=3)
        btn(bf, "Limpiar",   MUTED,  self.limpiar  ).grid(row=1, column=1, padx=4, pady=3)

        # ── Tabla
        tf = tk.Frame(body, bg=BG)
        tf.pack(side="left", fill="both", expand=True)

        # Estilo global unico (compatible con Windows / Python 3.13)
        st = ttk.Style()
        st.theme_use("clam")
        st.configure("Custom.Treeview",
                     background=ROW_ODD, foreground=TEXT,
                     fieldbackground=ROW_ODD,
                     rowheight=24, font=("Consolas", 8),
                     borderwidth=0)
        st.configure("Custom.Treeview.Heading",
                     background=SIDEBAR, foreground=color,
                     font=("Segoe UI", 8, "bold"), relief="flat")
        st.map("Custom.Treeview",
               background=[("selected", SEL)],
               foreground=[("selected", "#FFFFFF")])

        cols = [c[0] for c in self.columnas]
        self.tabla = ttk.Treeview(tf, columns=cols, show="headings",
                                  style="Custom.Treeview")
        for col_hdr, w in self.columnas:
            self.tabla.heading(col_hdr, text=col_hdr)
            self.tabla.column(col_hdr, width=w, anchor="w")
        self.tabla.tag_configure("odd",  background=ROW_ODD)
        self.tabla.tag_configure("even", background=ROW_EVEN)

        sc = ttk.Scrollbar(tf, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=sc.set)
        self.tabla.pack(side="left", fill="both", expand=True)
        sc.pack(side="right", fill="y")
        self.tabla.bind("<<TreeviewSelect>>", self._seleccionar)

    # ── Tabla ops ─────────────────────────────────────────────────

    def recargar(self):
        for r in self.tabla.get_children():
            self.tabla.delete(r)
        for i, row in enumerate(leer(self.entidad)):
            tag = "odd" if i % 2 == 0 else "even"
            self.tabla.insert("", "end", values=row, tags=(tag,))

    def _seleccionar(self, _event):
        sel = self.tabla.focus()
        if sel:
            vals = self.tabla.item(sel, "values")
            keys = [c[1] for c in self.campos]
            for j, k in enumerate(keys):
                if j < len(vals):
                    self.vars[k].set(vals[j])

    # ── Helpers ───────────────────────────────────────────────────

    def limpiar(self):
        for label, key, tipo, *opts in self.campos:
            if tipo == "combo" and opts and opts[0]:
                self.vars[key].set(opts[0][0])
            else:
                self.vars[key].set("")

    def _vals(self):
        return [self.vars[c[1]].get().strip() for c in self.campos]

    def _id(self):
        return self.vars[self.campos[0][1]].get().strip()

    def _validar(self):
        for label, key, tipo, *_ in self.campos:
            v = self.vars[key].get().strip()
            if v == "":
                messagebox.showwarning("Atención", f"Complete «{label}».")
                return False
            if key in self.numericos and not v.isdigit():
                messagebox.showwarning("Atención", f"«{label}» debe ser numérico.")
                return False
        return True

    # ── CRUD ──────────────────────────────────────────────────────

    def alta(self):
        if not self._validar():
            return
        rows = leer(self.entidad)
        if any(r[0] == self._id() for r in rows):
            messagebox.showerror("Error", "El identificador ya existe.")
            return
        rows.append(self._vals())
        guardar(self.entidad, rows)
        self.recargar()
        self.limpiar()
        messagebox.showinfo("Alta", "Registro creado correctamente.")

    def baja(self):
        id_ = self._id()
        if not id_:
            messagebox.showwarning("Atención", "Ingrese el identificador.")
            return
        rows = leer(self.entidad)
        ok = False
        for r in rows:
            if r[0] == id_:
                r[-1] = "BAJA"
                ok = True
        guardar(self.entidad, rows)
        self.recargar()
        messagebox.showinfo("Baja", "Dado de baja." if ok else "No encontrado.")

    def modificar(self):
        if not self._validar():
            return
        rows = leer(self.entidad)
        ok = False
        vals = self._vals()
        n = len(vals)
        for r in rows:
            if r[0] == self._id():
                # Reemplaza exactamente los campos del formulario; descarta sobrante
                r[:n] = vals
                del r[n:]
                ok = True
        guardar(self.entidad, rows)
        self.recargar()
        messagebox.showinfo("Modificar",
                            "Modificado correctamente." if ok else "No encontrado.")


# ═══════════════════════════════════════════════════════════════════
#  ENTIDADES
# ═══════════════════════════════════════════════════════════════════

class Clientes(ABMBase):
    entidad   = "clientes"
    titulo    = "Gestión de Clientes"
    numericos = {"id", "cuit", "tel"}
    campos = [
        ("ID Cliente",       "id",       "entry"),
        ("Razón Social",     "razon",    "entry"),
        ("CUIT",             "cuit",     "entry"),
        ("Dirección",        "dir",      "entry"),
        ("Teléfono",         "tel",      "entry"),
        ("E-mail",           "email",    "entry"),
        ("Localidad",        "loc",      "entry"),
        ("Condición IVA",    "iva",      "combo",
         ["Responsable Inscripto", "Monotributista", "Consumidor Final", "Exento"]),
        ("Estado",           "estado",   "combo", ["ACTIVO", "BAJA"]),
    ]
    columnas = [
        ("ID",        50), ("Razón Social", 130), ("CUIT",    90),
        ("Dirección", 110), ("Teléfono",     80),  ("E-mail", 110),
        ("Localidad",  80), ("Cond. IVA",    120), ("Estado",  60),
    ]


class Proveedores(ABMBase):
    entidad   = "proveedores"
    titulo    = "Gestión de Proveedores"
    numericos = {"id", "cuit", "tel"}
    campos = [
        ("ID Proveedor",  "id",       "entry"),
        ("Razón Social",  "razon",    "entry"),
        ("CUIT",          "cuit",     "entry"),
        ("Rubro",         "rubro",    "combo",
         ["Tejidos", "Hilos", "Avíos", "Confección", "Tintorería", "Otro"]),
        ("Contacto",      "contacto", "entry"),
        ("Teléfono",      "tel",      "entry"),
        ("E-mail",        "email",    "entry"),
        ("Localidad",     "loc",      "entry"),
        ("Condición IVA", "iva",      "combo",
         ["Responsable Inscripto", "Monotributista", "Exento"]),
        ("Estado",        "estado",   "combo", ["ACTIVO", "BAJA"]),
    ]
    columnas = [
        ("ID",       45), ("Razón Social", 120), ("CUIT",    85),
        ("Rubro",    80), ("Contacto",      90), ("Teléfono", 80),
        ("E-mail",  100), ("Localidad",     80), ("Cond. IVA",100),
        ("Estado",   55),
    ]


class Productos(ABMBase):
    entidad   = "productos"
    titulo    = "Gestión de Productos"
    numericos = {"id"}
    campos = [
        ("Código",         "id",        "entry"),
        ("Descripción",    "desc",      "entry"),
        ("Categoría",      "cat",       "combo",
         ["Remeras", "Pantalones", "Vestidos", "Abrigos",
          "Ropa Interior", "Accesorios", "Tejidos", "Otro"]),
        ("Talla",          "talla",     "combo",
         ["XS", "S", "M", "L", "XL", "XXL", "Único"]),
        ("Color",          "color",     "entry"),
        ("Composición",    "comp",      "entry"),   # ej: 100% algodón
        ("Precio Costo",   "p_costo",   "entry"),
        ("Precio Venta",   "p_venta",   "entry"),
        ("Unidad Medida",  "um",        "combo", ["Unidad", "Metro", "Kg", "Rollo"]),
        ("Estado",         "estado",    "combo", ["ACTIVO", "BAJA"]),
    ]
    columnas = [
        ("Código",    55), ("Descripción",  130), ("Categoría",  90),
        ("Talla",     45), ("Color",         70), ("Composición",90),
        ("P.Costo",   65), ("P.Venta",       65), ("UM",         50),
        ("Estado",    55),
    ]


class Compras(ABMBase):
    entidad   = "compras"
    titulo    = "Gestión de Compras"
    numericos = {"id", "prov_id", "prod_id", "cant"}
    campos = [
        ("Nro. Compra",    "id",       "entry"),
        ("Fecha",          "fecha",    "entry"),
        ("ID Proveedor",   "prov_id",  "entry"),
        ("ID Producto",    "prod_id",  "entry"),
        ("Cantidad",       "cant",     "entry"),
        ("Precio Unit.",   "p_unit",   "entry"),
        ("Descuento %",    "desc",     "entry"),
        ("Total",          "total",    "entry"),
        ("Condición Pago", "cond",     "combo",
         ["Contado", "30 días", "60 días", "90 días"]),
        ("Estado",         "estado",   "combo",
         ["PENDIENTE", "RECIBIDA", "ANULADA"]),
    ]
    columnas = [
        ("Nro.",    50), ("Fecha",    75), ("Prov.ID",  60),
        ("Prod.ID", 60), ("Cant.",    50), ("P.Unit.",  65),
        ("Desc.%",  50), ("Total",    70), ("Cond.",    70),
        ("Estado",  70),
    ]


class Ventas(ABMBase):
    entidad   = "ventas"
    titulo    = "Gestión de Ventas"
    numericos = {"id", "cli_id", "prod_id", "cant"}
    campos = [
        ("Nro. Venta",     "id",      "entry"),
        ("Fecha",          "fecha",   "entry"),
        ("ID Cliente",     "cli_id",  "entry"),
        ("ID Producto",    "prod_id", "entry"),
        ("Cantidad",       "cant",    "entry"),
        ("Precio Unit.",   "p_unit",  "entry"),
        ("Descuento %",    "desc",    "entry"),
        ("Total",          "total",   "entry"),
        ("Condición Pago", "cond",    "combo",
         ["Contado", "Tarjeta Déb.", "Tarjeta Créd.", "Transferencia", "Cuenta Cte."]),
        ("Estado",         "estado",  "combo",
         ["PENDIENTE", "FACTURADA", "ENTREGADA", "ANULADA"]),
    ]
    columnas = [
        ("Nro.",    50), ("Fecha",   75), ("Cli.ID",  60),
        ("Prod.ID", 60), ("Cant.",   50), ("P.Unit.", 65),
        ("Desc.%",  50), ("Total",   70), ("Cond.",   80),
        ("Estado",  70),
    ]


class Facturas(ABMBase):
    entidad   = "facturas"
    titulo    = "Gestión de Facturas"
    numericos = {"id"}
    campos = [
        ("Nro. Factura",  "id",       "entry"),
        ("Fecha",         "fecha",    "entry"),
        ("Tipo",          "tipo",     "combo", ["A", "B", "C", "X"]),
        ("Operación",     "op",       "combo", ["VENTA", "COMPRA", "NOTA DEB.", "NOTA CRED."]),
        ("ID Entidad",    "ent_id",   "entry"),  # cliente o proveedor
        ("Razón Social",  "razon",    "entry"),
        ("CUIT",          "cuit",     "entry"),
        ("Monto Neto",    "neto",     "entry"),
        ("IVA %",         "iva_pct",  "combo", ["21", "10.5", "27", "0"]),
        ("Monto IVA",     "iva_m",    "entry"),
        ("Total",         "total",    "entry"),
        ("Estado",        "estado",   "combo",
         ["EMITIDA", "ANULADA", "COBRADA", "PAGADA"]),
    ]
    columnas = [
        ("Nro.",    50), ("Fecha",  75), ("Tipo",   40),
        ("Op.",     75), ("Entidad",60), ("Razón",  110),
        ("CUIT",    85), ("Neto",   70), ("IVA%",   45),
        ("IVA $",   65), ("Total",  75), ("Estado", 65),
    ]


class Stock(ABMBase):
    entidad   = "stock"
    titulo    = "Gestión de Stock"
    numericos = {"prod_id"}
    campos = [
        ("ID Producto",    "prod_id",  "entry"),
        ("Descripción",    "desc",     "entry"),
        ("Categoría",      "cat",      "combo",
         ["Remeras", "Pantalones", "Vestidos", "Abrigos",
          "Ropa Interior", "Accesorios", "Tejidos", "Otro"]),
        ("Talla",          "talla",    "combo",
         ["XS", "S", "M", "L", "XL", "XXL", "Único"]),
        ("Color",          "color",    "entry"),
        ("Stock Actual",   "stk_act",  "entry"),
        ("Stock Mínimo",   "stk_min",  "entry"),
        ("Depósito",       "deposito", "entry"),
        ("Últ. Actualiz.", "fecha",    "entry"),
        ("Estado",         "estado",   "combo", ["OK", "BAJO MÍNIMO", "SIN STOCK"]),
    ]
    columnas = [
        ("Prod.ID",  60), ("Descripción",  120), ("Cat.",       80),
        ("Talla",    45), ("Color",         70), ("Stk.Actual", 75),
        ("Stk.Min",  65), ("Depósito",      80), ("Últ.Act.",   80),
        ("Estado",   80),
    ]

    def _init_defaults(self):
        super()._init_defaults()
        self.vars["fecha"].set(HOY)


# ═══════════════════════════════════════════════════════════════════
#  DASHBOARD
# ═══════════════════════════════════════════════════════════════════

class Dashboard(tk.Frame):
    MODULOS = [
        ("clientes",    "Clientes",    "Clientes",    "Cartera de compradores"),
        ("proveedores", "Proveedores", "Proveedores", "Proveedores textiles"),
        ("productos",   "Productos",   "Productos",   "Catálogo de artículos"),
        ("compras",     "Compras",     "Compras",     "Órdenes de compra"),
        ("ventas",      "Ventas",      "Ventas",      "Órdenes de venta"),
        ("facturas",    "Facturas",    "Facturas",    "Facturación A/B/C"),
        ("stock",       "Stock",       "Stock",       "Control de inventario"),
    ]

    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self._build()

    def _build(self):
        # Título
        tk.Label(self, text="Industrial del Sur",
                 font=("Segoe UI", 26, "bold"),
                 bg=BG, fg=TEXT).pack(pady=(48, 4))
        tk.Label(self, text="Sistema de Gestión Textil",
                 font=("Segoe UI", 11),
                 bg=BG, fg=MUTED).pack()
        tk.Label(self, text="Seleccione un módulo",
                 font=("Segoe UI", 9),
                 bg=BG, fg=BORDER).pack(pady=(2, 36))

        # Grid de tarjetas
        grid = tk.Frame(self, bg=BG)
        grid.pack()

        for i, (key, label, pantalla, desc) in enumerate(self.MODULOS):
            color, icon = META[key]
            r, c = divmod(i, 4)

            card = tk.Frame(grid, bg=CARD, cursor="hand2",
                            highlightthickness=1, highlightbackground=BORDER,
                            width=195, height=145)
            card.grid(row=r, column=c, padx=10, pady=10)
            card.pack_propagate(False)

            tk.Label(card, text=icon, font=("Segoe UI", 28),
                     bg=CARD, fg=color).pack(pady=(18, 2))
            tk.Label(card, text=label,
                     font=("Segoe UI", 11, "bold"),
                     bg=CARD, fg=TEXT).pack()
            tk.Label(card, text=desc,
                     font=("Segoe UI", 7),
                     bg=CARD, fg=MUTED).pack(pady=2)

            def _nav(e, p=pantalla):
                self.controller.mostrar(p)

            card.bind("<Button-1>", _nav)
            for w in card.winfo_children():
                w.bind("<Button-1>", _nav)

            def _hl(e, c=card, col=color):
                c.configure(highlightbackground=col, highlightthickness=2)

            def _unhl(e, c=card):
                c.configure(highlightbackground=BORDER, highlightthickness=1)

            card.bind("<Enter>", _hl)
            card.bind("<Leave>", _unhl)


# ═══════════════════════════════════════════════════════════════════
#  APLICACIÓN PRINCIPAL
# ═══════════════════════════════════════════════════════════════════

class App(tk.Tk):
    PANTALLAS = [
        ("Dashboard",    Dashboard,    None),
        ("Clientes",     Clientes,     "clientes"),
        ("Proveedores",  Proveedores,  "proveedores"),
        ("Productos",    Productos,    "productos"),
        ("Compras",      Compras,      "compras"),
        ("Ventas",       Ventas,       "ventas"),
        ("Facturas",     Facturas,     "facturas"),
        ("Stock",        Stock,        "stock"),
    ]

    NAV = [
        ("🏠  Inicio",       "Dashboard"),
        ("👥  Clientes",     "Clientes"),
        ("🏭  Proveedores",  "Proveedores"),
        ("🧵  Productos",    "Productos"),
        ("🛒  Compras",      "Compras"),
        ("💰  Ventas",       "Ventas"),
        ("🧾  Facturas",     "Facturas"),
        ("📊  Stock",        "Stock"),
    ]

    def __init__(self):
        super().__init__()
        self.title("Industrial del Sur - Gestión Textil")
        self.geometry("1180x680")
        self.resizable(False, False)
        self.configure(bg=BG)

        self._sidebar()
        self._main()

        self.frames = {}
        for name, Cls, _ in self.PANTALLAS:
            f = Cls(self.area, self)
            self.frames[name] = f
            f.place(relwidth=1, relheight=1)

        self.mostrar("Dashboard")

    # ── Sidebar ───────────────────────────────────────────────────

    def _sidebar(self):
        sb = tk.Frame(self, bg=SIDEBAR, width=188)
        sb.pack(side="left", fill="y")
        sb.pack_propagate(False)

        # Logo
        logo = tk.Frame(sb, bg=SIDEBAR, pady=16)
        logo.pack(fill="x")
        tk.Label(logo, text="⚙  Industrial del Sur",
                 font=("Segoe UI", 10, "bold"),
                 bg=SIDEBAR, fg=TEXT).pack(padx=14, anchor="w")
        tk.Label(logo, text="Gestión Textil",
                 font=("Segoe UI", 7),
                 bg=SIDEBAR, fg=MUTED).pack(padx=14, anchor="w")
        tk.Frame(sb, bg=BORDER, height=1).pack(fill="x", padx=10, pady=4)

        self.nav_btns = {}
        for label, target in self.NAV:
            b = tk.Button(
                sb, text=label,
                font=("Segoe UI", 9),
                bg=SIDEBAR, fg=MUTED,
                relief="flat", bd=0,
                anchor="w", padx=18, pady=9,
                cursor="hand2",
                activebackground=BG, activeforeground=TEXT,
                command=lambda t=target: self.mostrar(t),
            )
            b.pack(fill="x")
            self.nav_btns[target] = b

        tk.Frame(sb, bg=BORDER, height=1).pack(fill="x", padx=10, pady=16)
        tk.Button(sb, text="✕  Salir",
                  font=("Segoe UI", 9),
                  bg=SIDEBAR, fg=RED,
                  relief="flat", bd=0,
                  anchor="w", padx=18, pady=9,
                  cursor="hand2",
                  activebackground=BG,
                  command=self.destroy).pack(fill="x")

    def _main(self):
        self.area = tk.Frame(self, bg=BG)
        self.area.pack(side="left", fill="both", expand=True)

    # ── Navegación ────────────────────────────────────────────────

    def mostrar(self, nombre):
        for n, b in self.nav_btns.items():
            if n == nombre:
                b.configure(bg=BG, fg=TEXT, font=("Segoe UI", 9, "bold"))
            else:
                b.configure(bg=SIDEBAR, fg=MUTED, font=("Segoe UI", 9))
        self.frames[nombre].lift()


# ═══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    for k in META:
        crear_archivo(k)
    App().mainloop()