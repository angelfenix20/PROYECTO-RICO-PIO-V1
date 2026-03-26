import tkinter as tk
from tkinter import ttk
from theme import Theme
from ui_helpers import UIHelpers

class PuntoVentaPanel(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=Theme.APP_BG)
        self.controller = controller
        
        # Variables de control
        self.total_str = tk.StringVar(value="0,00")
        
        self._build_ui()

    def _build_ui(self):
        # Header Principal
        header = tk.Frame(self, bg=Theme.PRIMARY, height=40)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="Punto de Venta TOUCH SCREEN", font=Theme.FONT_H2, bg=Theme.PRIMARY, fg="white").pack(side="left", padx=10)
        
        # Frame de botones del header
        btn_frame = tk.Frame(header, bg=Theme.PRIMARY)
        btn_frame.pack(side="right", padx=10)
        
        tk.Label(btn_frame, text="Tasa Actual USD$ (46,66)", font=Theme.FONT_SMALL, bg=Theme.PRIMARY, fg="white").pack(side="left", padx=15)
        
        if self.controller.current_frame.__class__.__name__ == "AdminPanel":
            btn_volver = tk.Button(btn_frame, text="Volver al Panel Admin", bg=Theme.DANGER, fg="white", 
                                   font=Theme.FONT_BOLD, relief="flat", command=self.controller.mostrar_panel_admin)
            btn_volver.pack(side="left", padx=5)
        else:
            btn_corte = tk.Button(btn_frame, text="Corte de Caja", bg=Theme.ACCENT, fg="white", 
                                  font=Theme.FONT_BOLD, relief="flat", command=self.controller.mostrar_login)
            btn_corte.pack(side="left", padx=5)

        # Contenedor principal dividido en izquierda y derecha
        main_container = tk.Frame(self, bg=Theme.APP_BG)
        main_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Panel Izquierdo (Facturación)
        left_panel = tk.Frame(main_container, bg=Theme.SURFACE, width=450, highlightthickness=1, highlightbackground=Theme.BORDER)
        left_panel.pack(side="left", fill="y", padx=(0, 5))
        left_panel.pack_propagate(False)
        self._build_left_panel(left_panel)
        
        # Panel Derecho (Pestañas)
        right_panel = tk.Frame(main_container, bg=Theme.SURFACE, highlightthickness=1, highlightbackground=Theme.BORDER)
        right_panel.pack(side="left", fill="both", expand=True)
        self._build_right_panel(right_panel)

    def _build_left_panel(self, parent):
        # Total
        top_frame = tk.Frame(parent, bg=Theme.SURFACE, pady=10, padx=10)
        top_frame.pack(fill="x")
        
        total_frame = tk.Frame(top_frame, bg="black", pady=10)
        total_frame.pack(fill="x")
        tk.Label(total_frame, text="Total Cuenta Actual:", bg="black", fg="white", font=Theme.FONT_BODY).pack(anchor="w", padx=10)
        tk.Label(total_frame, textvariable=self.total_str, bg="black", fg="#00FF00", font=("Segoe UI", 36, "bold")).pack(anchor="e", padx=10)
        tk.Label(total_frame, text="PVP+I.V.A.: 0,0000 $", bg="black", fg="cyan", font=Theme.FONT_SMALL).pack(anchor="e", padx=10)
        
        # Formulario de datos
        form_frame = tk.Frame(parent, bg=Theme.SURFACE, padx=10, pady=5)
        form_frame.pack(fill="x")
        
        tk.Label(form_frame, text="CLIENTE: 0 USUARIO FINAL", bg=Theme.SURFACE, fg=Theme.PRIMARY, font=Theme.FONT_BOLD).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 10))
        
        tk.Label(form_frame, text="Mesa:", bg=Theme.SURFACE, font=Theme.FONT_SMALL).grid(row=1, column=0, sticky="w")
        tk.Entry(form_frame, width=15, font=Theme.FONT_BODY).grid(row=1, column=1, sticky="w", padx=5)
        
        tk.Label(form_frame, text="Vendedor:", bg=Theme.SURFACE, font=Theme.FONT_SMALL).grid(row=1, column=2, sticky="w")
        tk.Entry(form_frame, width=15, font=Theme.FONT_BODY).grid(row=1, column=3, sticky="w", padx=5)
        
        tk.Label(form_frame, text="Cód Artículo:", bg=Theme.SURFACE, font=Theme.FONT_SMALL).grid(row=2, column=0, sticky="w", pady=(10, 0))
        tk.Entry(form_frame, width=15, font=Theme.FONT_BODY).grid(row=2, column=1, sticky="w", padx=5, pady=(10, 0))
        
        tk.Label(form_frame, text="Cantidad:", bg=Theme.SURFACE, font=Theme.FONT_SMALL).grid(row=2, column=2, sticky="w", pady=(10, 0))
        tk.Entry(form_frame, width=15, font=Theme.FONT_BODY).grid(row=2, column=3, sticky="w", padx=5, pady=(10, 0))
        
        tk.Button(form_frame, text="✓ Procesar", bg=Theme.ACCENT, fg="white", font=Theme.FONT_BOLD, relief="flat").grid(row=3, column=3, sticky="ew", pady=(10, 0), padx=5)
        
        # Tabla de Detalles
        table_frame = tk.Frame(parent, bg=Theme.SURFACE, padx=10, pady=10)
        table_frame.pack(fill="both", expand=True)
        
        columns = ("Nota", "Cant.", "Descripción", "Tot.Linea")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        self.tree.heading("Nota", text="Nota")
        self.tree.column("Nota", width=50, anchor="center")
        self.tree.heading("Cant.", text="Cant.")
        self.tree.column("Cant.", width=50, anchor="center")
        self.tree.heading("Descripción", text="Descripción")
        self.tree.column("Descripción", width=200, anchor="w")
        self.tree.heading("Tot.Linea", text="Tot.Linea")
        self.tree.column("Tot.Linea", width=80, anchor="e")
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botones Inferiores Factura
        bottom_buttons = tk.Frame(parent, bg=Theme.SURFACE, padx=10, pady=10)
        bottom_buttons.pack(fill="x")
        
        tk.Button(bottom_buttons, text="✓ Resumir Líneas", bg=Theme.PRIMARY, fg="white", font=Theme.FONT_BOLD, relief="flat").pack(side="left", fill="x", expand=True, padx=2)
        tk.Button(bottom_buttons, text="Saldo", bg="#DDDDDD", fg="black", font=Theme.FONT_BOLD, relief="flat").pack(side="left", fill="x", expand=True, padx=2)

    def _build_right_panel(self, parent):
        # Notebook (Pestañas)
        style = ttk.Style()
        style.configure("TPos.TNotebook", background=Theme.SURFACE)
        style.configure("TPos.TNotebook.Tab", font=Theme.FONT_BOLD, padding=[15, 5])
        
        notebook = ttk.Notebook(parent, style="TPos.TNotebook")
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        tab_grupos = tk.Frame(notebook, bg="white")
        tab_mesas = tk.Frame(notebook, bg="white")
        
        notebook.add(tab_grupos, text="Grupos")
        notebook.add(tab_mesas, text="Mesas")
        
        self._build_grupos_tab(tab_grupos)
        self._build_mesas_tab(tab_mesas)

    def _build_grupos_tab(self, parent):
        # Grilla de Grupos basada en la imagen de referencia
        grupos_data = [
            ("PIZZAS", "#FF8C00"),       # Naranja
            ("HAMBURGUESAS", "#8B4513"), # Marrón
            ("POLLOS", "#4B0082"),       # Morado Oscuro
            ("SOPAS", "#008000"),        # Verde
            ("ENSALADAS", "#FFA07A"),    # Naranja claro
            ("ENTRADAS", "#1E90FF"),     # Azul claro
            ("BEBIDAS", "#FF0000"),      # Rojo
            ("LICORES", "#0000FF"),      # Azul fuerte
            ("PROMOCIONES", "#FF8C00"),  # Naranja
            ("PANADERIA", "#FF1493"),    # Rosa
            ("POSTRES", "#6495ED"),      # Celeste
            ("PASTAS", "#008080"),       # Verde azulado
        ]

        # Crear un canvas y frame para permitir padding interior de grilla (opcional, uso frames)
        grid_frame = tk.Frame(parent, bg="white")
        grid_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Configurar columnas para que se expandan uniformemente (5 columnas máximo)
        for i in range(5):
            grid_frame.columnconfigure(i, weight=1, uniform="group")
        for i in range(4): # 4 filas
            grid_frame.rowconfigure(i, weight=1, uniform="group")
            
        col, row = 0, 0
        for text, color in grupos_data:
            btn = tk.Button(grid_frame, text=text, bg=color, fg="white", font=Theme.FONT_BOLD, relief="flat", wraplength=100)
            btn.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
            
            col += 1
            if col > 4:
                col = 0
                row += 1
                
        # Rellenar casillas vacías
        while row < 4:
            tk.Frame(grid_frame, bg="#F0F0F0", highlightthickness=1, highlightcolor="#DDDDDD").grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
            col += 1
            if col > 4:
                col = 0
                row += 1

    def _build_mesas_tab(self, parent):
        # Grilla de Mesas basada en la imagen de referencia
        grid_frame = tk.Frame(parent, bg="white")
        grid_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        for i in range(5):
            grid_frame.columnconfigure(i, weight=1, uniform="mesa")
        for i in range(5):
            grid_frame.rowconfigure(i, weight=1, uniform="mesa")
            
        mesa_num = 1
        for row in range(5):
            for col in range(5):
                # Simular que la Mesa 1 está ocupada (azul) y las demás libres (blanco)
                bg_color = Theme.PRIMARY if mesa_num == 6 else "white" # Usamos mesa 6 como la ocupada (referencia image 2, col 0 row 1)
                text = f"M0{mesa_num}" if mesa_num == 6 else ""
                fg_color = "white"
                
                btn = tk.Button(grid_frame, text=text, bg=bg_color, fg=fg_color, font=Theme.FONT_BOLD, 
                                relief="solid", bd=1, highlightbackground=Theme.PRIMARY)
                
                # Bottom band on the table buttons (indicates availability or simple design element)
                btn_container = tk.Frame(grid_frame, bg="white", highlightthickness=1, highlightbackground="#DDDDDD")
                btn_container.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
                btn_container.pack_propagate(False)
                
                inner_btn = tk.Button(btn_container, text=text, bg=bg_color, fg=fg_color, font=Theme.FONT_BOLD, relief="flat")
                inner_btn.pack(fill="both", expand=True)
                
                tk.Frame(btn_container, bg=Theme.PRIMARY, height=10).pack(side="bottom", fill="x") # Barra inferior azul clásica de Premium Soft
                
                mesa_num += 1
