import tkinter as tk
from tkinter import ttk
from theme import Theme
from ui_helpers import UIHelpers

# Importar diálogos
from dialogs.tasa_cambio import TasaCambioDialog
from dialogs.monedas import DefinirMonedasDialog
from dialogs.grupos_inventario import GruposInventarioDialog
from dialogs.articulos_inventario import ArticulosInventarioDialog

class AdminPanel(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=Theme.APP_BG)
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        # Sidebar (Oscuro)
        sidebar = tk.Frame(self, bg=Theme.SIDEBAR_BG, width=240)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Logo/Marca en Sidebar
        brand_frame = tk.Frame(sidebar, bg=Theme.SIDEBAR_BG, pady=30)
        brand_frame.pack(fill="x")
        tk.Label(brand_frame, text="Rico Pío", fg=Theme.ACCENT, bg=Theme.SIDEBAR_BG, font=("Segoe UI", 18, "bold")).pack()
        tk.Label(brand_frame, text="ADMINISTRATIVO", fg=Theme.TEXT_LIGHT, bg=Theme.SIDEBAR_BG, font=("Segoe UI", 8)).pack()

        # Buscador en Sidebar
        search_f = tk.Frame(sidebar, bg=Theme.SIDEBAR_BG, padx=15, pady=10)
        search_f.pack(fill="x")
        search_e = tk.Entry(search_f, bg=Theme.DARK_PANEL, fg="white", relief="flat", insertbackground="white")
        search_e.pack(fill="x", ipady=4)
        search_e.insert(0, " Buscar función...")

        # Menú de Navegación (Treeview estilizado)
        tree_style = ttk.Style()
        tree_style.configure("Custom.Treeview", background=Theme.SIDEBAR_BG, foreground="white", 
                             fieldbackground=Theme.SIDEBAR_BG, borderwidth=0, font=Theme.FONT_BODY)
        
        tree = ttk.Treeview(sidebar, show="tree", style="Custom.Treeview")
        tree.pack(fill="both", expand=True, padx=5)
        
        fav_id = tree.insert("", "end", text=" ARCHIVOS", open=True)
        tree.insert(fav_id, "end", text=" Definir Monedas")
        tree.insert(fav_id, "end", text=" Grupos de Inventario")
        tree.insert(fav_id, "end", text=" Artículos de Inventario")
        
        proc_id = tree.insert("", "end", text=" PROCESOS", open=True)
        tree.insert(proc_id, "end", text=" Tasa de Cambio")

        def on_tree_click(event):
            item = tree.identify_row(event.y)
            if not item: return
            texto = tree.item(item, "text").strip()
            if texto == "Tasa de Cambio": TasaCambioDialog(self.controller.root)
            elif texto == "Definir Monedas": DefinirMonedasDialog(self.controller.root)
            elif texto == "Grupos de Inventario": GruposInventarioDialog(self.controller.root)
            elif texto == "Artículos de Inventario": ArticulosInventarioDialog(self.controller.root)
        
        tree.bind("<Double-1>", on_tree_click)

        # Botón Salir en Sidebar
        btn_exit = tk.Button(sidebar, text="Cerrar Sesión", bg=Theme.DANGER, fg="white", 
                             font=Theme.FONT_BOLD, relief="flat", command=self.controller.mostrar_login)
        btn_exit.pack(fill="x", side="bottom", padx=20, pady=20)

        # Área Principal
        main_area = tk.Frame(self, bg=Theme.APP_BG)
        main_area.pack(side="left", fill="both", expand=True)

        # Header Superior
        header = tk.Frame(main_area, bg=Theme.SURFACE, height=60, bd=0, highlightthickness=1, highlightbackground=Theme.BORDER)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="Panel General de Operaciones", font=Theme.FONT_H2, bg=Theme.SURFACE, fg=Theme.TEXT_PRIMARY).pack(side="left", padx=20)
        
        status_f = tk.Frame(header, bg=Theme.SURFACE)
        status_f.pack(side="right", padx=20)
        tk.Label(status_f, text="Estación: 001", font=Theme.FONT_SMALL, bg=Theme.SURFACE, fg=Theme.TEXT_SECONDARY).pack(side="left", padx=10)
        tk.Label(status_f, text="● Online", font=Theme.FONT_SMALL, fg=Theme.ACCENT, bg=Theme.SURFACE).pack(side="left")

        # Contenido Central (Grid de Acciones)
        content = tk.Frame(main_area, bg=Theme.APP_BG, padx=20, pady=40)
        content.pack(fill="both", expand=True)

        grid_f = tk.Frame(content, bg=Theme.APP_BG)
        grid_f.pack()

        self.create_action_card(grid_f, "Punto de Venta", "Ventas y facturación", "💳", 0, 0, command=self.controller.mostrar_punto_venta)
        self.create_action_card(grid_f, "Touch Screen", "Interfaz p/ Restaurante", "🍽️", 0, 1, command=self.controller.mostrar_punto_venta)
        self.create_action_card(grid_f, "Inventario", "Stock y Almacén", "📦", 0, 2)

    def create_action_card(self, parent, title, desc, icon, row, col, command=None):
        card = tk.Frame(parent, bg=Theme.SURFACE, width=190, height=170, relief="flat", 
                        highlightthickness=1, highlightbackground=Theme.BORDER)
        if command:
            card.configure(cursor="hand2")
            
        card.grid(row=row, column=col, padx=10, pady=15)
        card.pack_propagate(False)

        lbl_icon = tk.Label(card, text=icon, font=("Segoe UI", 40), bg=Theme.SURFACE)
        lbl_icon.pack(pady=(20, 10))
        lbl_title = tk.Label(card, text=title, font=Theme.FONT_BOLD, bg=Theme.SURFACE, fg=Theme.TEXT_PRIMARY)
        lbl_title.pack()
        lbl_desc = tk.Label(card, text=desc, font=Theme.FONT_SMALL, bg=Theme.SURFACE, fg=Theme.TEXT_SECONDARY)
        lbl_desc.pack(pady=5)
        
        # Simular hover en la card
        def on_enter(e): card.configure(highlightbackground=Theme.PRIMARY)
        def on_leave(e): card.configure(highlightbackground=Theme.BORDER)
        
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        
        # Enlazar command a los widgets
        if command:
            card.bind("<Button-1>", lambda e: command())
            lbl_icon.bind("<Button-1>", lambda e: command())
            lbl_title.bind("<Button-1>", lambda e: command())
            lbl_desc.bind("<Button-1>", lambda e: command())
