import tkinter as tk
from tkinter import ttk
from theme import Theme
from ui_helpers import UIHelpers

class ArticulosInventarioDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Artículos de inventario")
        self.geometry("950x700")
        self.configure(bg=Theme.SURFACE)
        self.resizable(True, True)
        self.transient(parent)
        self.grab_set()
        self._build_ui()

    def _build_ui(self):
        UIHelpers.create_header(self, "Gestión de Artículos y Servicios")
        
        # Header de Búsqueda rápida
        search_f = tk.Frame(self, bg=Theme.APP_BG, padx=20, pady=15)
        search_f.pack(fill="x")
        
        tk.Label(search_f, text="Código del Artículo:", font=Theme.FONT_BOLD, bg=Theme.APP_BG).pack(side="left")
        e_search = tk.Entry(search_f, font=("Segoe UI", 12), width=30, relief="flat", highlightthickness=1, highlightbackground=Theme.BORDER)
        e_search.pack(side="left", padx=15, ipady=4)
        tk.Button(search_f, text=" 🔍 Buscar ", font=Theme.FONT_SMALL, bg=Theme.PRIMARY, fg="white", relief="flat").pack(side="left")

        # Contenedor Principal (Notebook)
        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=20, pady=10)
        
        f1 = tk.Frame(nb, bg=Theme.SURFACE, padx=15, pady=15)
        f2 = tk.Frame(nb, bg=Theme.SURFACE, padx=15, pady=15)
        f3 = tk.Frame(nb, bg=Theme.SURFACE, padx=15, pady=15)
        
        nb.add(f1, text=" Datos Generales ")
        nb.add(f2, text=" Precios e Impuestos ")
        nb.add(f3, text=" Existencias ")

        self._build_general_tab(f1)
        self._build_pricing_tab(f2)

        # Footer Actions
        footer = tk.Frame(self, bg=Theme.FOOTER_BG, pady=15, padx=25)
        footer.pack(fill="x", side="bottom")
        
        UIHelpers.btn_primary(footer, "🖫 Guardar Artículo").pack(side="right", padx=5)
        tk.Button(footer, text="🗑 Eliminar", font=Theme.FONT_BOLD, bg="white", fg=Theme.DANGER, relief="flat", padx=10).pack(side="right", padx=5)
        tk.Button(footer, text="Cerrar", font=Theme.FONT_BOLD, bg="white", fg=Theme.TEXT_SECONDARY, relief="flat", command=self.destroy).pack(side="left", padx=5)

    def _build_general_tab(self, parent):
        top = tk.Frame(parent, bg=Theme.SURFACE)
        top.pack(fill="x")
        
        # Lado Izquierdo: Formulario
        f_left = tk.Frame(top, bg=Theme.SURFACE)
        f_left.pack(side="left", fill="both", expand=True)
        
        for lbl in ["Nombre o Descripción:", "Grupo del Artículo:", "Marca / Fabricante:"]:
            row = tk.Frame(f_left, bg=Theme.SURFACE)
            row.pack(fill="x", pady=5)
            tk.Label(row, text=lbl, font=Theme.FONT_SMALL, bg=Theme.SURFACE, width=20, anchor="w").pack(side="left")
            tk.Entry(row, relief="flat", highlightthickness=1, highlightbackground=Theme.BORDER).pack(side="left", fill="x", expand=True, ipady=3)

        # Lado Derecho: Foto
        f_right = tk.Frame(top, bg=Theme.SURFACE, width=200, padx=20)
        f_right.pack(side="right", fill="y")
        
        label_pic = tk.Label(f_right, text="Fotografía", font=Theme.FONT_SMALL, bg=Theme.SURFACE)
        label_pic.pack()
        pic_box = tk.Frame(f_right, width=150, height=150, bg=Theme.APP_BG, highlightthickness=1, highlightbackground=Theme.BORDER)
        pic_box.pack(pady=5)
        pic_box.pack_propagate(False)
        tk.Label(pic_box, text="NO IMAGE", font=("Segoe UI", 8), bg=Theme.APP_BG, fg=Theme.TEXT_SECONDARY).place(relx=0.5, rely=0.5, anchor="center")

    def _build_pricing_tab(self, parent):
        tk.Label(parent, text="Configuración de Costos y Precios", font=Theme.FONT_H2, bg=Theme.SURFACE, fg=Theme.PRIMARY).pack(anchor="w", pady=(0, 20))
        
        grid = tk.Frame(parent, bg=Theme.SURFACE)
        grid.pack(fill="x")
        
        labels = ["Costo de Compra:", "Precio Venta 1:", "Precio Venta 2:", "Precio Venta 3:"]
        for i, lbl in enumerate(labels):
            tk.Label(grid, text=lbl, font=Theme.FONT_SMALL, bg=Theme.SURFACE).grid(row=i, column=0, sticky="w", pady=5)
            tk.Entry(grid, width=15, justify="right", relief="flat", highlightthickness=1, highlightbackground=Theme.BORDER).grid(row=i, column=1, padx=10, ipady=2)
            tk.Label(grid, text="Impuesto Aplicable:", font=Theme.FONT_SMALL, bg=Theme.SURFACE).grid(row=i, column=2, sticky="w", padx=(20, 0))
            ttk.Combobox(grid, values=["IVA 16%", "Exento", "Reducido 8%"], width=15).grid(row=i, column=3, padx=10)
