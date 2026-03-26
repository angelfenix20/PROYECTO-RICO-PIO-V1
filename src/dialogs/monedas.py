import tkinter as tk
from tkinter import ttk
from theme import Theme
from ui_helpers import UIHelpers

class DefinirMonedasDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Monedas")
        self.geometry("520x370")
        self.configure(bg=Theme.BG_WHITE)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self._build_ui()
        
    def _build_ui(self):
        UIHelpers.create_header(self, "Monedas")
        body = tk.Frame(self, bg=Theme.BG_WHITE, padx=18, pady=10)
        body.pack(fill="both", expand=True)

        UIHelpers.lbl(body, "Código:", 0, 0)
        ef = tk.Frame(body, bg=Theme.BG_WHITE)
        ef.grid(row=0, column=1, sticky="w", padx=4, pady=3)
        tk.Entry(ef, width=6, relief="solid", bd=1).pack(side="left")
        tk.Button(ef, text="Buscar", font=Theme.FONT_SMALL, relief="solid", bd=1, padx=4).pack(side="left", padx=4)

        UIHelpers.lbl(body, "Nombre:", 1, 0)
        UIHelpers.entry(body, 1, 1, width=40)

        UIHelpers.lbl(body, "Singular:", 2, 0)
        ef2 = tk.Frame(body, bg=Theme.BG_WHITE)
        ef2.grid(row=2, column=1, sticky="w", padx=4, pady=3)
        tk.Entry(ef2, width=18, relief="solid", bd=1).pack(side="left")
        tk.Label(ef2, text="Plural:", bg=Theme.BG_WHITE, font=Theme.FONT_NORMAL).pack(side="left", padx=(10,2))
        tk.Entry(ef2, width=14, relief="solid", bd=1).pack(side="left")

        UIHelpers.lbl(body, "Símbolo:", 3, 0)
        ef3 = tk.Frame(body, bg=Theme.BG_WHITE)
        ef3.grid(row=3, column=1, sticky="w", padx=4, pady=3)
        tk.Entry(ef3, width=6, relief="solid", bd=1).pack(side="left")
        tk.Label(ef3, text="Ultima Cotización:", bg=Theme.BG_WHITE, font=Theme.FONT_NORMAL).pack(side="left", padx=(10,2))
        cotiz = tk.Entry(ef3, width=14, relief="solid", bd=1, bg=Theme.ENTRY_HIGHLIGHT, justify="right")
        cotiz.insert(0, "0,00")
        cotiz.pack(side="left")
        tk.Button(ef3, text="...", width=2, font=Theme.FONT_SMALL, relief="solid", bd=1).pack(side="left", padx=2)

        UIHelpers.lbl(body, "Decimal:", 4, 0)
        ef4 = tk.Frame(body, bg=Theme.BG_WHITE)
        ef4.grid(row=4, column=1, sticky="w", padx=4, pady=3)
        dec_e = tk.Entry(ef4, width=4, relief="solid", bd=1)
        dec_e.insert(0, "0")
        dec_e.pack(side="left")
        tk.Label(ef4, text="Código ISO 4217:", bg=Theme.BG_WHITE, font=Theme.FONT_NORMAL).pack(side="left", padx=(10,2))
        iso_cb = ttk.Combobox(ef4, width=8, values=["USD","EUR","VES","COP"])
        iso_cb.pack(side="left")
        tk.Button(ef4, text="Asignar Icono", font=Theme.FONT_SMALL, relief="solid", bd=1, padx=4).pack(side="left", padx=6)

        UIHelpers.lbl(body, "Tipo:", 5, 0)
        tipo_var = tk.StringVar(value="Nacional")
        ef5 = tk.Frame(body, bg=Theme.BG_WHITE)
        ef5.grid(row=5, column=1, sticky="w", padx=4, pady=3)
        tk.Radiobutton(ef5, text="Nacional", variable=tipo_var, value="Nacional", bg=Theme.BG_WHITE).pack(side="left")
        tk.Radiobutton(ef5, text="Extranjera", variable=tipo_var, value="Extranjera", bg=Theme.BG_WHITE).pack(side="left", padx=6)

        calc_frame = tk.LabelFrame(body, text=" En los procesos de Cuentas por Pagar ", bg=Theme.BG_WHITE, font=Theme.FONT_SMALL, padx=8, pady=4)
        calc_frame.grid(row=6, column=0, columnspan=2, sticky="ew", padx=4, pady=4)
        calc_var = tk.StringVar(value="multiplica")
        calc_inner = tk.Frame(calc_frame, bg=Theme.BG_WHITE)
        calc_inner.pack(side="left", fill="x", expand=True)
        tk.Label(calc_inner, text="Cálculo", bg=Theme.BG_WHITE, font=Theme.FONT_BOLD).pack(anchor="w")
        tk.Radiobutton(calc_inner, text="Multiplica por la moneda nacional", variable=calc_var, value="multiplica", bg=Theme.BG_WHITE, font=Theme.FONT_NORMAL).pack(anchor="w")
        tk.Radiobutton(calc_inner, text="Divide entre la moneda nacional", variable=calc_var, value="divide", bg=Theme.BG_WHITE, font=Theme.FONT_NORMAL).pack(anchor="w")
        tk.Button(calc_frame, text="Cargar Var.", font=Theme.FONT_SMALL, relief="solid", bd=1, padx=6).pack(side="right", anchor="center")

        btn_bar = tk.Frame(self, bg=Theme.BG_DEFAULT, pady=6)
        btn_bar.pack(fill="x", side="bottom")
        tk.Button(btn_bar, text="Importar Tasas", bg=Theme.MODAL_HEADER_BG, fg="white", font=Theme.FONT_BOLD, padx=8, pady=4).pack(side="left", padx=10)
        tk.Button(btn_bar, text="🖫  Grabar", bg=Theme.BUTTON_GRAY, fg="white", font=Theme.FONT_BOLD, padx=8, pady=4).pack(side="right", padx=4)
        tk.Button(btn_bar, text="🗑  Borrar", bg=Theme.BUTTON_GRAY, fg="white", font=Theme.FONT_BOLD, padx=8, pady=4).pack(side="right", padx=4)
        tk.Button(btn_bar, text="⮐  Salir", bg=Theme.ACCENT_RED, fg="white", font=Theme.FONT_BOLD, padx=8, pady=4, command=self.destroy).pack(side="right", padx=4)

        UIHelpers.create_status_bar(self, "Indique el CODIGO DE LA MONEDA", "ANT: 001   NUEVO")
