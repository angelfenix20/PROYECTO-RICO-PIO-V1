import tkinter as tk
from tkinter import ttk
from theme import Theme

class MesasView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=Theme.APP_BG)
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        # Header / Top Action Bar
        header = tk.Frame(self, bg="#201815", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        # Title
        title_f = tk.Frame(header, bg="#201815")
        title_f.pack(side="left", padx=20, pady=15)
        
        tk.Label(title_f, text="Mesas", fg="white", bg="#201815", font=("Segoe UI", 16, "bold")).pack(side="left")
        tk.Label(title_f, text="  6 de 6 disponibles", fg=Theme.TEXT_SECONDARY, bg="#201815", font=("Segoe UI", 10)).pack(side="left", pady=(5,0))

        # Right Action Buttons
        actions_f = tk.Frame(header, bg="#201815")
        actions_f.pack(side="right", padx=20, pady=10)

        # Action icons (refresh, flash, print, wifi)
        for icon, color in [("🔄", "#5c4a40"), ("⚡", Theme.DANGER), ("🖨️", Theme.SUCCESS), ("📡", Theme.DANGER)]:
            btn = tk.Label(actions_f, text=icon, font=("Segoe UI", 14), bg=color, fg="white", width=2, height=1, relief="flat", highlightbackground="#201815", highlightthickness=2)
            btn.pack(side="left", padx=5)
            # Make it circular (via pack/corner radius isn't natural in tk, so we just use normal labels)

        # Toolbar (Area Principal / Nueva Mesa)
        toolbar = tk.Frame(self, bg="#33251e", padx=15, pady=10, highlightthickness=0)
        toolbar.pack(fill="x", padx=15, pady=15)
        
        tk.Button(toolbar, text="  Área Principal (6)  ", bg="#4a3b34", fg="white", font=Theme.FONT_BOLD, relief="flat").pack(side="left")
        tk.Button(toolbar, text=" + Nueva Mesa", bg=Theme.SUCCESS, fg="white", font=Theme.FONT_BOLD, relief="flat").pack(side="right")
        tk.Button(toolbar, text=" ◎ Nueva Área ", bg="#5c4a40", fg="white", font=Theme.FONT_BOLD, relief="flat").pack(side="right", padx=10)

        # Grid de Mesas
        grid_frame = tk.Frame(self, bg=Theme.APP_BG)
        grid_frame.pack(fill="both", expand=True, padx=15)
        
        for i in range(6):
            grid_frame.columnconfigure(i, weight=1, uniform="mesas")
        
        for i in range(6):
            self._crear_mesa(grid_frame, i+1, 0, i)
            
    def _crear_mesa(self, parent, numero, row, col):
        # Color simulando madera rojiza / caja clara
        mesa_bg = "#d9a05b"
        card = tk.Frame(parent, bg=mesa_bg, width=120, height=150, highlightthickness=2, highlightbackground="#9e6621")
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        card.pack_propagate(False)

        # Numero de mesa
        tk.Label(card, text=str(numero), font=("Segoe UI", 36, "bold"), bg=mesa_bg, fg="white").pack(pady=(20, 5))
        
        # Etiqueta de disponible
        badge = tk.Frame(card, bg="#ffffff", padx=10, pady=2)
        badge.pack()
        tk.Label(badge, text="Disponible", font=("Segoe UI", 9, "bold"), bg="#ffffff", fg="#c48a43").pack()

        # Punto verde
        tk.Label(card, text="●", font=("Segoe UI", 16), bg=mesa_bg, fg="#10b981").pack(pady=5)

        # Bind events
        def on_click(e):
            self._abrir_punto_venta(numero)

        for w in card.winfo_children():
            w.bind("<Button-1>", on_click)
            w.config(cursor="hand2")
            if hasattr(w, "winfo_children"): # para el badge
                for ww in w.winfo_children():
                    ww.bind("<Button-1>", on_click)
                    ww.config(cursor="hand2")
        card.bind("<Button-1>", on_click)
        card.config(cursor="hand2")

    def _abrir_punto_venta(self, numero_mesa):
        from panels.punto_venta import PuntoVentaModal
        PuntoVentaModal(self.winfo_toplevel(), self.controller, numero_mesa)
