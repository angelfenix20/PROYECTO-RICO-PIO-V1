import tkinter as tk
from tkinter import ttk
from theme import Theme
from ui_helpers import UIHelpers
import customtkinter as ctk

ctk.set_appearance_mode("dark")

# Importar diálogos
from dialogs.tasa_cambio import TasaCambioDialog
from dialogs.monedas import DefinirMonedasDialog
from dialogs.grupos_inventario import GruposInventarioDialog
from dialogs.articulos_inventario import ArticulosInventarioDialog

class AdminPanel(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=Theme.APP_BG)
        self.controller = controller
        self._build_sidebar()
        self._build_main_area()

    def _build_sidebar(self):
        # Sidebar container oscurecido
        sidebar = tk.Frame(self, bg=Theme.SIDEBAR_BG, width=300)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Perfil Usuario
        profile_frame = tk.Frame(sidebar, bg="#1a1412", pady=20, highlightthickness=0)
        profile_frame.pack(fill="x")
        
        # Contenedor para el icono redondeado real
        logo_bg = ctk.CTkLabel(profile_frame, text="📊", font=("Segoe UI", 32), fg_color="white", text_color="#1a1412", width=60, height=60, corner_radius=15)
        logo_bg.pack(side="left", padx=15)
        
        user_info = tk.Frame(profile_frame, bg="#1a1412")
        user_info.pack(side="left", fill="y", expand=True)
        # Nombre "Rico Pio" solicitado
        tk.Label(user_info, text="Rico Pio", fg="white", bg="#1a1412", font=("Segoe UI", 16, "bold"), anchor="w").pack(fill="x")
        tk.Label(user_info, text="Rico Pio", fg=Theme.TEXT_SECONDARY, bg="#1a1412", font=("Segoe UI", 10), anchor="w").pack(fill="x")

        # Separador
        tk.Frame(sidebar, bg="#3d332e", height=1).pack(fill="x", padx=15, pady=5)

        # Scrollable Grid para botones (CustomTkinter)
        self.btn_frame = ctk.CTkScrollableFrame(
            sidebar, 
            fg_color=Theme.SIDEBAR_BG, 
            bg_color=Theme.SIDEBAR_BG,
            scrollbar_button_color="#3d332e",
            scrollbar_button_hover_color="#5a4d46"
        )
        self.btn_frame.pack(side="left", fill="both", expand=True, pady=10, padx=5)

        for i in range(2):
            self.btn_frame.columnconfigure(i, weight=1, uniform="col")

        botones = [
            ("Pedidos", "📋", None, Theme.BLUE),
            ("Mesas", "🟩", self.mostrar_mesas, Theme.SECONDARY),
            ("Cocina", "🍳", None, Theme.ORANGE),
            ("Productos", "🛍️", lambda: ArticulosInventarioDialog(self.controller.root), Theme.DANGER),
            ("Inventario", "📦", lambda: GruposInventarioDialog(self.controller.root), Theme.ACCENT),
            ("Ventas", "💲", None, Theme.SUCCESS),
            ("Análisis", "📈", None, Theme.PRIMARY),
            ("Config", "⚙️", None, Theme.TEXT_SECONDARY),
            ("Divisas", "💵", lambda: TasaCambioDialog(self.controller.root), Theme.ACCENT),
            ("Clientes", "👤", None, Theme.BLUE),
        ]

        row = 0
        col = 0
        for text, icon, cmd, color in botones:
            self._crear_btn_sidebar(text, icon, color, cmd, row, col)
            col += 1
            if col > 1:
                col = 0
                row += 1

    def _crear_btn_sidebar(self, text, icon, color, cmd, row, col):
        btn_bg = "#261e1b"
        # Usar un verdadero contenedor con bordes redondeados
        card = ctk.CTkFrame(self.btn_frame, fg_color=btn_bg, corner_radius=15, border_width=1, border_color="#3d332e")
        card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
        card.columnconfigure(0, weight=1)
        card.rowconfigure(0, weight=1)
        
        # Simular icono
        icon_lbl = ctk.CTkLabel(card, text=icon, font=("Segoe UI", 24), fg_color=color, text_color="white", width=40, height=40, corner_radius=8)
        icon_lbl.pack(pady=(15, 5))
        
        # Texto
        lblText = ctk.CTkLabel(card, text=text, text_color="white", fg_color="transparent", font=("Segoe UI", 11, "bold"))
        lblText.pack(pady=(0, 15))
        
        if cmd:
            def on_click(e):
                cmd()
            card.bind("<Button-1>", on_click)
            icon_lbl.bind("<Button-1>", on_click)
            lblText.bind("<Button-1>", on_click)
            try:
                card.configure(cursor="hand2")
                icon_lbl.configure(cursor="hand2")
                lblText.configure(cursor="hand2")
            except:
                pass
            
        def on_enter(e):
            card.configure(fg_color="#3a2f2b", border_color="#5a4d46")
        def on_leave(e):
            card.configure(fg_color=btn_bg, border_color="#3d332e")
            
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        icon_lbl.bind("<Enter>", on_enter)
        icon_lbl.bind("<Leave>", on_leave)
        lblText.bind("<Enter>", on_enter)
        lblText.bind("<Leave>", on_leave)

    def _build_main_area(self):
        self.main_area = tk.Frame(self, bg=Theme.APP_BG)
        self.main_area.pack(side="left", fill="both", expand=True)

        self.current_view = None
        self.mostrar_mesas() # Default view

    def mostrar_mesas(self):
        if self.current_view:
            self.current_view.destroy()
        
        try:
            from panels.mesas_view import MesasView
            self.current_view = MesasView(self.main_area, self.controller)
            self.current_view.pack(fill="both", expand=True)
        except ImportError:
            # Fallback temporal si no existe
            self.current_view = tk.Frame(self.main_area, bg=Theme.APP_BG)
            self.current_view.pack(fill="both", expand=True)
            tk.Label(self.current_view, text="Vista de Mesas no encontrada.", font=Theme.FONT_H2, bg=Theme.APP_BG, fg="white").pack(expand=True)
