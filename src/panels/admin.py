import tkinter as tk
from tkinter import ttk
from theme import Theme

# Importar diálogos desde el nuevo paquete
from dialogs.tasa_cambio import TasaCambioDialog
from dialogs.monedas import DefinirMonedasDialog
from dialogs.grupos_inventario import GruposInventarioDialog
from dialogs.articulos_inventario import ArticulosInventarioDialog

class AdminPanel(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=Theme.BG_WHITE)
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        header = tk.Frame(self, bg=Theme.BG_WHITE, height=50)
        header.pack(fill="x")
        
        logo_lbl = tk.Label(header, text="☁ Software", font=("Arial", 16, "bold", "italic"), fg=Theme.ACCENT_BLUE, bg=Theme.BG_WHITE)
        logo_lbl.pack(side="left", padx=10, pady=10)
        
        version_lbl = tk.Label(header, text="Administrativo 9.1\nRevisión: 2026", font=Theme.FONT_NORMAL, bg=Theme.BG_WHITE, justify="right")
        version_lbl.pack(side="right", padx=10)
        tk.Label(header, text="Versión Modular", font=("Arial", 10, "bold"), fg="#c0392b", bg=Theme.BG_WHITE).pack(side="right", padx=5)

        body = tk.Frame(self, bg=Theme.BG_WHITE)
        body.pack(fill="both", expand=True)

        left_panel = tk.Frame(body, width=200, bg="#f5f5f5", relief="sunken", bd=1)
        left_panel.pack(side="left", fill="y")
        left_panel.pack_propagate(False)

        search_frame = tk.Frame(left_panel, bg=Theme.MODAL_HEADER_BG)
        search_frame.pack(fill="x")
        tk.Label(search_frame, text="Buscar:", fg="white", bg=Theme.MODAL_HEADER_BG, font=Theme.FONT_BOLD).pack(side="left", padx=5)
        search_entry = tk.Entry(search_frame, width=15)
        search_entry.pack(side="left", padx=5, pady=2)
        tk.Button(search_frame, text="X", bg=Theme.ACCENT_RED, fg="white", bd=0, font=("Arial", 8, "bold")).pack(side="right", padx=2, pady=2)
        
        menu_container = tk.Frame(left_panel, bg=Theme.BG_WHITE)
        menu_container.pack(fill="both", expand=True)

        tabs_frame = tk.Frame(menu_container, bg=Theme.BG_DEFAULT)
        tabs_frame.pack(side="left", fill="y")
        for tab in ["Administración"]:
            vtext = "\n".join(list(tab))
            tk.Button(tabs_frame, text=vtext, width=2, font=("Arial", 7), bg="#f5f5f5", relief="groove").pack(pady=2)

        tree = ttk.Treeview(menu_container, show="tree")
        tree.pack(side="left", fill="both", expand=True)
        fav_id = tree.insert("", "end", text="Favoritos", open=True)
        
        archivos_id = tree.insert(fav_id, "end", text="Archivos", open=True)
        tree.insert(archivos_id, "end", text="Definir Monedas")
        tree.insert(archivos_id, "end", text="Grupos de Inventario")
        tree.insert(archivos_id, "end", text="Artículos de Inventario")
        
        procesos_id = tree.insert(fav_id, "end", text="Procesos", open=True)
        tree.insert(procesos_id, "end", text="Tasa de Cambio")
        
        tree.insert(fav_id, "end", text="Informes")

        def on_tree_double_click(event):
            selected = tree.selection()
            if not selected:
                return
            texto = tree.item(selected[0], "text")
            if texto == "Tasa de Cambio":
                TasaCambioDialog(self.controller.root)
            elif texto == "Definir Monedas":
                DefinirMonedasDialog(self.controller.root)
            elif texto == "Grupos de Inventario":
                GruposInventarioDialog(self.controller.root)
            elif texto == "Artículos de Inventario":
                ArticulosInventarioDialog(self.controller.root)
                
        tree.bind("<Double-1>", on_tree_double_click)

        support_lbl = tk.Label(left_panel, text="COMUNIDAD\nDE SOPORTE", font=("Arial", 10, "bold"), fg=Theme.SUCCESS_GREEN, bg=Theme.BG_WHITE, relief="ridge", bd=2)
        support_lbl.pack(side="bottom", fill="x", pady=2)

        right_panel = tk.Frame(body, width=50, bg=Theme.DARK_PANEL)
        right_panel.pack(side="right", fill="y")

        center_panel = tk.Frame(body, bg=Theme.BG_WHITE)
        center_panel.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        top_btns = tk.Frame(center_panel, bg=Theme.BG_WHITE)
        top_btns.pack(fill="x")

        self.create_big_btn(top_btns, "Punto de Venta", "PUNTO DE VENTA", "💳", "F2")
        self.create_big_btn(top_btns, "Touch Screen", "RESTAURANTES", "🍽️", "F3")
        self.create_big_btn(top_btns, "Consulta Precios", "PRECIOS", "🏷️", "F4")

        bottom_bar = tk.Frame(self, bg=Theme.BG_DEFAULT, height=30, bd=1, relief="raised")
        bottom_bar.pack(fill="x", side="bottom")

        status_text = "ADMIN-001  Módulo: Administrativo  Usuario: ADMINISTRACION"
        tk.Label(bottom_bar, text=status_text, bg=Theme.BG_DEFAULT, font=Theme.FONT_SMALL).pack(side="left", padx=5)

        sys_btns = tk.Frame(bottom_bar, bg=Theme.BG_DEFAULT)
        sys_btns.pack(side="right")
        tk.Button(sys_btns, text="Cambiar de Usuario (f6)", bg="#bdc3c7", font=Theme.FONT_SMALL, command=self.controller.mostrar_login).pack(side="left", padx=1)
        tk.Button(sys_btns, text="Salir (Esc)", bg="#c0392b", fg="white", font=("Arial", 8, "bold"), command=self.controller.root.destroy).pack(side="left", padx=1)

    def create_big_btn(self, parent, top_text, subtitle, icon, keybind):
        f = tk.Frame(parent, bg=Theme.BG_WHITE, relief="groove", bd=1)
        f.pack(side="left", padx=10)
        tk.Label(f, text=f"{top_text} ({keybind})", font=Theme.FONT_NORMAL, fg="#7f8c8d", bg=Theme.BG_WHITE).pack(anchor="w", padx=5)
        center_f = tk.Frame(f, bg=Theme.BG_WHITE)
        center_f.pack(pady=10, padx=20)
        tk.Label(center_f, text=icon, font=("Arial", 35), bg=Theme.BG_WHITE).pack()
        tk.Label(center_f, text=subtitle, font=("Arial", 10, "bold"), fg=Theme.ACCENT_BLUE, bg=Theme.BG_WHITE).pack()
