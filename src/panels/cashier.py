import tkinter as tk
from theme import Theme
from ui_helpers import UIHelpers

class CashierPanel(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=Theme.APP_BG)
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        # Header Premium
        header = tk.Frame(self, bg=Theme.SURFACE, height=70, highlightthickness=1, highlightbackground=Theme.BORDER)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="CAJA Y FACTURACIÓN", font=Theme.FONT_H1, bg=Theme.SURFACE, fg=Theme.PRIMARY).pack(side="left", padx=25)
        
        # Info Usuario en Header
        user_info = tk.Frame(header, bg=Theme.SURFACE)
        user_info.pack(side="right", padx=25)
        tk.Label(user_info, text="CAJERO ACTIVO", font=Theme.FONT_SMALL, fg=Theme.TEXT_SECONDARY, bg=Theme.SURFACE).pack(side="left", padx=10)
        UIHelpers.btn_primary(user_info, "Cerrar Turno").pack(side="left")

        # Área de Contenido
        content = tk.Frame(self, bg=Theme.APP_BG)
        content.pack(fill="both", expand=True, padx=50, pady=50)

        # Card de Bienvenida
        welcome_card = tk.Frame(content, bg=Theme.SURFACE, padx=40, pady=40, highlightthickness=1, highlightbackground=Theme.BORDER)
        welcome_card.pack(fill="x")

        tk.Label(welcome_card, text="Punto de Venta Rico Pío", font=Theme.FONT_H1, bg=Theme.SURFACE, fg=Theme.TEXT_PRIMARY).pack(anchor="w")
        tk.Label(welcome_card, text="Seleccione una acción para comenzar el proceso de facturación.", 
                 font=Theme.FONT_BODY, bg=Theme.SURFACE, fg=Theme.TEXT_SECONDARY).pack(anchor="w", pady=(5, 30))

        # Botones Principales de Caja
        btn_grid = tk.Frame(welcome_card, bg=Theme.SURFACE)
        btn_grid.pack(fill="x")

        for icon, txt in [("🛒", "Nueva Venta"), ("📋", "Comandas"), ("💰", "Cierre de Caja")]:
            f = tk.Frame(btn_grid, bg=Theme.APP_BG, padx=20, pady=20, cursor="hand2")
            f.pack(side="left", padx=10, expand=True, fill="both")
            tk.Label(f, text=icon, font=("Segoe UI", 30), bg=Theme.APP_BG).pack()
            tk.Label(f, text=txt, font=Theme.FONT_BOLD, bg=Theme.APP_BG, fg=Theme.PRIMARY).pack()
            
            # Hover effect for the card frame
            f.bind("<Enter>", lambda e, w=f: w.configure(bg=Theme.BORDER))
            f.bind("<Leave>", lambda e, w=f: w.configure(bg=Theme.APP_BG))

        # Botón Volver (Logout)
        tk.Button(self, text="⮐ Salir al Login", font=Theme.FONT_BOLD, fg=Theme.DANGER, bg=Theme.APP_BG,
                  relief="flat", command=self.controller.mostrar_login).pack(side="bottom", pady=30)
