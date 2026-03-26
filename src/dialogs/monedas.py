import tkinter as tk
from tkinter import ttk
from theme import Theme
from ui_helpers import UIHelpers

class DefinirMonedasDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Monedas")
        self.geometry("550x450")
        self.configure(bg=Theme.SURFACE)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self._build_ui()
        
    def _build_ui(self):
        UIHelpers.create_header(self, "Definición de Monedas")
        
        body = tk.Frame(self, bg=Theme.SURFACE, padx=20, pady=15)
        body.pack(fill="both", expand=True)

        # Campos superiores
        row1 = tk.Frame(body, bg=Theme.SURFACE)
        row1.pack(fill="x", pady=5)
        UIHelpers.lbl(row1, "Código:", 0, 0, anchor="w")
        e_cod = UIHelpers.entry(row1, 0, 1, width=10)
        tk.Button(row1, text=" Buscar ", font=Theme.FONT_SMALL, relief="flat", bg=Theme.BORDER).grid(row=0, column=2, padx=5)

        row2 = tk.Frame(body, bg=Theme.SURFACE)
        row2.pack(fill="x", pady=5)
        UIHelpers.lbl(row2, "Nombre:", 0, 0, anchor="w")
        UIHelpers.entry(row2, 0, 1, width=45)

        # Grid de detalles
        grid_f = tk.Frame(body, bg=Theme.SURFACE)
        grid_f.pack(fill="x", pady=10)
        
        UIHelpers.lbl(grid_f, "Singular:", 0, 0)
        UIHelpers.entry(grid_f, 0, 1, width=15)
        UIHelpers.lbl(grid_f, "Plural:", 0, 2)
        UIHelpers.entry(grid_f, 0, 3, width=15)

        UIHelpers.lbl(grid_f, "Símbolo:", 1, 0)
        UIHelpers.entry(grid_f, 1, 1, width=8)
        UIHelpers.lbl(grid_f, "Cotización:", 1, 2)
        cot = UIHelpers.entry(grid_f, 1, 3, width=15, bg=Theme.ENTRY_HIGHLIGHT)
        cot.insert(0, "0,00")

        # Configuración Extra
        extra_f = tk.LabelFrame(body, text=" Configuración ", bg=Theme.SURFACE, font=Theme.FONT_SMALL, padx=10, pady=10)
        extra_f.pack(fill="x", pady=15)
        
        tk.Label(extra_f, text="Tipo de Moneda:", bg=Theme.SURFACE, font=Theme.FONT_SMALL).grid(row=0, column=0, sticky="w")
        v = tk.StringVar(value="N")
        tk.Radiobutton(extra_f, text="Nacional", variable=v, value="N", bg=Theme.SURFACE).grid(row=0, column=1)
        tk.Radiobutton(extra_f, text="Extranjera", variable=v, value="E", bg=Theme.SURFACE).grid(row=0, column=2)

        # Botonera
        btn_bar = tk.Frame(self, bg=Theme.APP_BG, pady=10, padx=20)
        btn_bar.pack(fill="x", side="bottom")
        
        UIHelpers.btn_primary(btn_bar, "🖫 Grabar", width=12).pack(side="right", padx=5)
        
        btn_del = tk.Button(btn_bar, text="🗑 Borrar", font=Theme.FONT_BOLD, bg="white", fg=Theme.DANGER, 
                            relief="flat", command=self.destroy)
        btn_del.pack(side="right", padx=5)
        UIHelpers.apply_hover(btn_del, "white", "#fee2e2")

        btn_exit = tk.Button(btn_bar, text="Salir", font=Theme.FONT_BOLD, bg="white", fg=Theme.TEXT_SECONDARY, relief="flat", command=self.destroy)
        btn_exit.pack(side="left", padx=5)
