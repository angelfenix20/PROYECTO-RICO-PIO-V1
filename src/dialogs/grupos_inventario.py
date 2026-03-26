import tkinter as tk
from tkinter import ttk
from theme import Theme
from ui_helpers import UIHelpers

class GruposInventarioDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Grupos de inventario")
        self.geometry("760x560")
        self.configure(bg=Theme.BG_WHITE)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self._build_ui()

    def _build_ui(self):
        UIHelpers.create_header(self, "Grupos de inventario")
        body = tk.Frame(self, bg=Theme.BG_WHITE)
        body.pack(fill="both", expand=True, padx=10, pady=8)

        left = tk.Frame(body, bg=Theme.BG_WHITE)
        left.pack(side="left", fill="both", expand=True)

        self._build_row(left, "Código:", 6, show_search=True)
        self._build_row(left, "Nombre:", 38)
        self._build_row(left, "Corto:", 22)

        cc_frame = tk.LabelFrame(left, text=" Códigos Contables: ", bg=Theme.BG_WHITE, font=Theme.FONT_NORMAL, padx=8, pady=6)
        cc_frame.pack(fill="x", pady=6)
        for lbl_text in ["Cta. de Inventario:", "Cta. de Costos:", "Cta. de Ingresos:", "Cta. de Devolución:", "Devol. Compras:"]:
            row = tk.Frame(cc_frame, bg=Theme.BG_WHITE)
            row.pack(fill="x", pady=2)
            tk.Label(row, text=lbl_text, bg=Theme.BG_WHITE, font=Theme.FONT_NORMAL, width=18, anchor="e").pack(side="left")
            tk.Entry(row, width=22, bg=Theme.ENTRY_HIGHLIGHT, relief="solid", bd=1).pack(side="left", padx=2)
            tk.Button(row, text="...", width=2, font=Theme.FONT_SMALL, relief="solid", bd=1).pack(side="left", padx=1)

        tk.Checkbutton(left, text="No mostrar este Grupo en Pto.Venta Touch Screen", bg=Theme.BG_WHITE, font=Theme.FONT_NORMAL).pack(anchor="w", pady=2)
        tk.Checkbutton(left, text="Son Licores", bg=Theme.BG_WHITE, font=Theme.FONT_NORMAL).pack(anchor="w", pady=2)

        seg_row = tk.Frame(left, bg=Theme.BG_WHITE)
        seg_row.pack(fill="x", pady=2)
        tk.Label(seg_row, text="Tipo de seguridad:", bg=Theme.BG_WHITE, font=Theme.FONT_NORMAL).pack(side="left")
        ttk.Combobox(seg_row, values=["Seguridad Estricta", "Normal", "Sin Seguridad"], width=18).pack(side="left", padx=4)

        fmt_row = tk.Frame(left, bg=Theme.BG_WHITE)
        fmt_row.pack(fill="x", pady=2)
        tk.Label(fmt_row, text="Formato de Impresión para comanda:", bg=Theme.BG_WHITE, font=Theme.FONT_NORMAL).pack(anchor="w")
        ttk.Combobox(fmt_row, values=[], width=36).pack(anchor="w", pady=2)

        cid_row = tk.Frame(left, bg=Theme.BG_WHITE)
        cid_row.pack(fill="x", pady=4)
        tk.Label(cid_row, text="Color ID", bg=Theme.BG_WHITE, font=Theme.FONT_NORMAL).pack(side="left")
        tk.Entry(cid_row, width=6, relief="solid", bd=1).pack(side="left", padx=4)

        mid = tk.Frame(body, bg=Theme.BG_WHITE, width=180)
        mid.pack(side="left", fill="y", padx=10)
        mid.pack_propagate(False)

        tk.Label(mid, text="Imagen asociada", bg=Theme.BG_WHITE, font=Theme.FONT_BOLD).pack(pady=(0,4))
        img_box = tk.Frame(mid, width=130, height=110, bg="#f0f0f0", relief="sunken", bd=1)
        img_box.pack()
        img_box.pack_propagate(False)
        tk.Label(img_box, text="SIN IMAGEN", bg="#f0f0f0", fg="#aaaaaa", font=Theme.FONT_NORMAL).place(relx=0.5, rely=0.5, anchor="center")

        tk.Button(mid, text="Asociar imagen", font=Theme.FONT_NORMAL, relief="solid", bd=1, padx=6, pady=4).pack(pady=8)
        tk.Button(mid, text="Indicar Sub. Grupos", font=Theme.FONT_BOLD, bg="#c8c8c8", relief="raised", padx=6, pady=4).pack(pady=4)

        right = tk.Frame(body, bg=Theme.BG_WHITE)
        right.pack(side="right", fill="y", padx=4)
        self._build_porcentaje_section(right, "% de Utilidad:")
        self._build_porcentaje_section(right, "% de Descuento:")

        btn_bar = tk.Frame(self, bg=Theme.BG_DEFAULT, pady=6)
        btn_bar.pack(fill="x", side="bottom")
        tk.Button(btn_bar, text="🖫  Grabar", bg=Theme.BUTTON_GRAY, fg="white", font=Theme.FONT_BOLD, padx=10, pady=4).pack(side="right", padx=5)
        tk.Button(btn_bar, text="🗑  Borrar", bg=Theme.BUTTON_GRAY, fg="white", font=Theme.FONT_BOLD, padx=10, pady=4).pack(side="right", padx=5)
        tk.Button(btn_bar, text="⮐  Salir", bg=Theme.ACCENT_RED, fg="white", font=Theme.FONT_BOLD, padx=10, pady=4, command=self.destroy).pack(side="right", padx=5)

        UIHelpers.create_status_bar(self, "Indique el Código de Grupo de Inventario", "ANT: 13   NUEVO")

    def _build_row(self, parent, label, width, show_search=False):
        r = tk.Frame(parent, bg=Theme.BG_WHITE)
        r.pack(fill="x", pady=2)
        tk.Label(r, text=label, bg=Theme.BG_WHITE, font=Theme.FONT_NORMAL).pack(side="left")
        tk.Entry(r, width=width, relief="solid", bd=1).pack(side="left", padx=4)
        if show_search:
            tk.Button(r, text="Buscar", font=Theme.FONT_SMALL, relief="solid", bd=1, padx=4).pack(side="left", padx=4)

    def _build_porcentaje_section(self, parent, title):
        tk.Label(parent, text=title, bg=Theme.BG_WHITE, font=Theme.FONT_BOLD).pack(anchor="w", pady=(6,2))
        for i in range(1, 8):
            row = tk.Frame(parent, bg=Theme.BG_WHITE)
            row.pack(anchor="w")
            tk.Label(row, text=f"# {i}", bg=Theme.BG_WHITE, font=Theme.FONT_SMALL, width=3).pack(side="left")
            e = tk.Entry(row, width=8, relief="solid", bd=1, justify="right")
            e.insert(0, "0,000")
            e.pack(side="left", padx=2, pady=1)
