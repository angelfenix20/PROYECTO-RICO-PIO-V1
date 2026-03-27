import tkinter as tk
from tkinter import ttk
from theme import Theme
from ui_helpers import UIHelpers
from logic import BusinessLogic
from billing_logic import BillingLogic

class PuntoVentaPanel(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=Theme.APP_BG)
        self.controller = controller
        self.billing = BillingLogic()
        
        # Variables de control
        self.total_str = tk.StringVar(value="0,00")
        self.tasa_str = tk.StringVar(value=f"({BusinessLogic.get_tasa_usd():.2f})")
        
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
        
        tk.Label(btn_frame, text="Tasa Actual USD$", font=Theme.FONT_SMALL, bg=Theme.PRIMARY, fg="white").pack(side="left", padx=(15, 0))
        tk.Label(btn_frame, textvariable=self.tasa_str, font=Theme.FONT_SMALL, bg=Theme.PRIMARY, fg="white").pack(side="left", padx=(5, 15))
        
        if self.controller.current_frame.__class__.__name__ == "AdminPanel":
            btn_volver = tk.Button(btn_frame, text="Volver al Panel Admin", bg=Theme.DANGER, fg="white", 
                                   font=Theme.FONT_BOLD, relief="flat", command=self.controller.mostrar_panel_admin)
            btn_volver.pack(side="left", padx=5)
        else:
            btn_corte = tk.Button(btn_frame, text="Corte de Caja", bg=Theme.ACCENT, fg="white", 
                                  font=Theme.FONT_BOLD, relief="flat", command=self.controller.mostrar_login)
            btn_corte.pack(side="left", padx=5)

        # Botón Cerrar Sesión (Siempre visible)
        btn_logout = tk.Button(btn_frame, text="Cerrar Sesión", bg=Theme.DANGER, fg="white", 
                               font=Theme.FONT_BOLD, relief="flat", command=self.controller.mostrar_login)
        btn_logout.pack(side="left", padx=5)

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
        
        # Notebook Pestañas Izquierda
        style = ttk.Style()
        style.configure("Left.TNotebook", background=Theme.SURFACE)
        style.configure("Left.TNotebook.Tab", font=Theme.FONT_BOLD, padding=[10, 2])

        left_notebook = ttk.Notebook(parent, style="Left.TNotebook")
        left_notebook.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        tab_operacion = tk.Frame(left_notebook, bg=Theme.SURFACE)
        tab_transito = tk.Frame(left_notebook, bg=Theme.SURFACE)
        tab_procesos = tk.Frame(left_notebook, bg=Theme.SURFACE)
        
        left_notebook.add(tab_operacion, text="F7 - Operación Actual")
        left_notebook.add(tab_transito, text="F6 - En Tránsito")
        left_notebook.add(tab_procesos, text="F10 - Procesos")
        
        self._build_tab_operacion(tab_operacion)
        self._build_tab_transito(tab_transito)
        self._build_tab_procesos(tab_procesos)

    def _build_tab_operacion(self, parent):
        # Formulario de datos
        form_frame = tk.Frame(parent, bg=Theme.SURFACE, padx=10, pady=5)
        form_frame.pack(fill="x")
        
        tk.Label(form_frame, text="CLIENTE: 0 USUARIO FINAL", bg=Theme.SURFACE, fg=Theme.PRIMARY, font=Theme.FONT_BOLD).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 10))
        
        tk.Label(form_frame, text="Mesa:", bg=Theme.SURFACE, font=Theme.FONT_SMALL).grid(row=1, column=0, sticky="w")
        self.entry_mesa = tk.Entry(form_frame, width=15, font=Theme.FONT_BODY)
        self.entry_mesa.grid(row=1, column=1, sticky="w", padx=5)
        self.entry_mesa.bind("<Return>", lambda e: self._on_procesar())
        
        tk.Label(form_frame, text="Vendedor:", bg=Theme.SURFACE, font=Theme.FONT_SMALL).grid(row=1, column=2, sticky="w")
        self.entry_vendedor = tk.Entry(form_frame, width=15, font=Theme.FONT_BODY, fg="blue")
        self.entry_vendedor.grid(row=1, column=3, sticky="w", padx=5)
        self.entry_vendedor.insert(0, "vendedor")
        self.entry_vendedor.config(state="readonly")
        
        tk.Label(form_frame, text="Cód Artículo:", bg=Theme.SURFACE, font=Theme.FONT_SMALL).grid(row=2, column=0, sticky="w", pady=(10, 0))
        tk.Entry(form_frame, width=15, font=Theme.FONT_BODY).grid(row=2, column=1, sticky="w", padx=5, pady=(10, 0))
        
        tk.Label(form_frame, text="Cantidad:", bg=Theme.SURFACE, font=Theme.FONT_SMALL).grid(row=2, column=2, sticky="w", pady=(10, 0))
        tk.Entry(form_frame, width=15, font=Theme.FONT_BODY).grid(row=2, column=3, sticky="w", padx=5, pady=(10, 0))
        
        tk.Button(form_frame, text="✓ Procesar", bg=Theme.ACCENT, fg="white", font=Theme.FONT_BOLD, relief="flat", command=self._on_procesar).grid(row=3, column=3, sticky="ew", pady=(10, 0), padx=5)
        
        # Tabla de Detalles
        table_frame = tk.Frame(parent, bg=Theme.SURFACE, padx=10, pady=10)
        table_frame.pack(fill="both", expand=True)
        
        columns = ("Nota", "Cant.", "Descripción", "Tot.Linea")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        self.tree.heading("Nota", text="Nota")
        self.tree.column("Nota", width=50, anchor="center")
        self.tree.heading("Cant.", text="Cant.")
        self.tree.column("Cant.", width=50, anchor="center")
        self.tree.heading("Descripción", text="Descripción")
        self.tree.column("Descripción", width=180, anchor="w")
        self.tree.heading("Tot.Linea", text="Tot.Linea")
        self.tree.column("Tot.Linea", width=80, anchor="e")
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botones Inferiores Factura
        bottom_buttons = tk.Frame(parent, bg=Theme.SURFACE, padx=10, pady=10)
        bottom_buttons.pack(fill="x", side="bottom")
        
        tk.Button(bottom_buttons, text="✓ Resumir Líneas", bg=Theme.PRIMARY, fg="white", font=Theme.FONT_BOLD, relief="flat").pack(side="left", fill="x", expand=True, padx=2)
        tk.Button(bottom_buttons, text="Saldo", bg="#DDDDDD", fg="black", font=Theme.FONT_BOLD, relief="flat").pack(side="left", fill="x", expand=True, padx=2)

    def _build_tab_transito(self, parent):
        # Tabla de Cuentas Abiertas (En Tránsito)
        table_frame = tk.Frame(parent, bg=Theme.SURFACE, padx=10, pady=10)
        table_frame.pack(fill="both", expand=True)
        
        columns = ("Abrir", "Vendedor", "Cliente", "Mesa", "Monto Neto Bs.", "Status")
        tree_transito = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        widths = {"Abrir": 50, "Vendedor": 80, "Cliente": 120, "Mesa": 50, "Monto Neto Bs.": 100, "Status": 60}
        for col in columns:
            tree_transito.heading(col, text=col)
            tree_transito.column(col, width=widths[col], anchor="center" if col != "Cliente" else "w")
            
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree_transito.yview)
        tree_transito.configure(yscroll=scrollbar.set)
        
        tree_transito.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Footer
        footer = tk.Frame(parent, bg=Theme.SURFACE, padx=10, pady=10)
        footer.pack(fill="x", side="bottom")
        tk.Label(footer, text="Ctas.Abiertas:", bg=Theme.SURFACE, font=Theme.FONT_BOLD).pack(side="left")
        tk.Label(footer, text="0,00 Bs.", bg=Theme.SURFACE, font=Theme.FONT_BOLD).pack(side="right")

    def _build_tab_procesos(self, parent):
        grid_frame = tk.Frame(parent, bg=Theme.SURFACE)
        grid_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        for i in range(2):
            grid_frame.columnconfigure(i, weight=1, uniform="proc")
            
        def create_btn(row, col, text, colspan=1):
            btn = tk.Button(grid_frame, text=text, bg="#E0E0E0", fg="black", font=Theme.FONT_BOLD, relief="flat", height=3)
            btn.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=5, pady=5)
            
        create_btn(0, 0, "Mesas")
        create_btn(0, 1, "") # Filler or empty space (in image 4, 'Mesas' is just a big button)
        
        create_btn(1, 0, "Despachadores")
        create_btn(1, 1, "Tipos de Mesas")
        
        create_btn(2, 0, "Reportes\nF5")
        create_btn(2, 1, "Saldos\nF3")
        
        # Botón grande "Procesos" en el fondo
        btn_proc = tk.Button(grid_frame, text="Procesos", bg="#E0E0E0", fg="black", font=Theme.FONT_BOLD, relief="flat", height=3)
        btn_proc.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        # Ajustar pesos de filas
        for i in range(4):
            grid_frame.rowconfigure(i, weight=1)

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
        self.grupos_view_container = tk.Frame(parent, bg="white")
        self.grupos_view_container.pack(fill="both", expand=True, padx=20, pady=20)
        self._render_grupos_grid()

    def _render_grupos_grid(self):
        # Limpiar
        for w in self.grupos_view_container.winfo_children():
            w.destroy()
            
        grupos_del_sistema = self.billing.get_grupos()
        grupos_data = [(g["id"], g.get("nombre", "DESCONOCIDO"), g.get("color", "#CCCCCC")) for g in grupos_del_sistema]

        # Configurar columnas
        for i in range(5):
            self.grupos_view_container.columnconfigure(i, weight=1, uniform="group")
        for i in range(4): 
            self.grupos_view_container.rowconfigure(i, weight=1, uniform="group")
            
        col, row = 0, 0
        for gid, text, color in grupos_data:
            btn = tk.Button(self.grupos_view_container, text=text, bg=color, fg="white" if int(color[1:3],16)<150 else "black", font=Theme.FONT_BOLD, 
                             relief="flat", wraplength=100, command=lambda g=gid: self._show_productos_grupo(g))
            btn.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
            
            col += 1
            if col > 4:
                col = 0
                row += 1
                
        # Rellenar casillas vacías para mantener alineación
        while row < 4:
            tk.Frame(self.grupos_view_container, bg="#F0F0F0", highlightthickness=1, highlightcolor="#DDDDDD").grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
            col += 1
            if col > 4:
                col = 0
                row += 1

    def _show_productos_grupo(self, grupo_id):
        # Limpiar vista actual de grupos
        for w in self.grupos_view_container.winfo_children():
            w.destroy()
            
        productos = self.billing.get_productos_por_grupo(grupo_id)
        
        # Barra superior con botón volver
        top_bar = tk.Frame(self.grupos_view_container, bg="white")
        top_bar.grid(row=0, column=0, columnspan=5, sticky="ew", pady=(0, 10))
        tk.Button(top_bar, text="← Volver a Grupos", font=Theme.FONT_BOLD, bg=Theme.SECONDARY, fg="white", 
                  relief="flat", command=self._render_grupos_grid, padx=20).pack(side="left")
        
        # Grid para productos
        for i in range(5):
            self.grupos_view_container.columnconfigure(i, weight=1, uniform="prod")
        for i in range(1, 5): 
            self.grupos_view_container.rowconfigure(i, weight=1, uniform="prod")

        col, row = 0, 1
        for p in productos:
            nombre = p.get('nombre', 'DESCONOCIDO')
            precio = p.get('precio_usd', 0.0)
            color = p.get('color') or '#CCCCCC'
            fg_color = "white" if int(color[1:3], 16) < 150 else "black"
            
            # Texto multilinea con precio
            display_text = f"{nombre}\n\n${precio:.2f}"
            
            btn = tk.Button(self.grupos_view_container, text=display_text, bg=color, fg=fg_color, font=("Segoe UI", 10, "bold"), 
                             relief="flat", wraplength=100, command=lambda prod=p: self._add_item_to_receipt(prod))
            btn.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
            
            col += 1
            if col > 4:
                col = 0
                row += 1
                
    def _add_item_to_receipt(self, prod):
        # Aqui conectariamos con el ticket de la izquierda, por ahora un log visual
        print(f"Producto añadido: {prod['nombre']} a {prod['precio_usd']}")
        # Lógica de agregar al recibo para una etapa posterior...

    def _build_mesas_tab(self, parent):
        # Grilla de Mesas dinámica
        self.mesas_container = tk.Frame(parent, bg="white")
        self.mesas_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.refresh_mesas()
        
        # Botones de gestión de mesas (Agregar/Quitar)
        btn_area = tk.Frame(parent, bg="white")
        btn_area.pack(fill="x", side="bottom", pady=10)
        
        tk.Button(btn_area, text="[+] Agregar Mesa", bg=Theme.ACCENT, fg="white", font=Theme.FONT_BOLD, command=self._add_mesa).pack(side="left", padx=10)
        tk.Button(btn_area, text="[-] Quitar Mesa", bg=Theme.DANGER, fg="white", font=Theme.FONT_BOLD, command=self._remove_mesa).pack(side="left", padx=10)

    def refresh_mesas(self):
        for widget in self.mesas_container.winfo_children():
            widget.destroy()
            
        mesas = BusinessLogic.get_mesas()
        
        # Grid dinámico (5 columnas)
        cols = 5
        for i, mesa in enumerate(mesas):
            row, col = divmod(i, cols)
            self.mesas_container.columnconfigure(col, weight=1, uniform="mesa")
            self.mesas_container.rowconfigure(row, weight=1, uniform="mesa")
            
            bg_color = Theme.PRIMARY if mesa["ocupada"] else "white"
            text = f"{mesa['label']}\n{mesa['cliente']}" if mesa["ocupada"] else mesa["label"]
            fg_color = "white" if mesa["ocupada"] else "black"
            
            btn_card = tk.Frame(self.mesas_container, bg="white", highlightthickness=1, highlightbackground="#DDDDDD")
            btn_card.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
            btn_card.pack_propagate(False)
            
            btn = tk.Button(btn_card, text=text, bg=bg_color, fg=fg_color, font=("Segoe UI", 9, "bold"), relief="flat")
            btn.pack(fill="both", expand=True)
            
            # Click en mesa para liberar o ver info
            btn.bind("<Button-1>", lambda e, m=mesa: self._interact_mesa(m))
            
            tk.Frame(btn_card, bg=Theme.PRIMARY, height=10).pack(side="bottom", fill="x")

    def _interact_mesa(self, mesa):
        from tkinter import messagebox, simpledialog
        if mesa["ocupada"]:
            if messagebox.askyesno("Mesa Ocupada", f"¿Desea liberar la {mesa['label']} ({mesa['cliente']})?"):
                mesas = BusinessLogic.get_mesas()
                for m in mesas:
                    if m["id"] == mesa["id"]:
                        m["ocupada"] = False
                        m["cliente"] = ""
                BusinessLogic.set_mesas(mesas)
                self.refresh_mesas()
        else:
            # Opción de renombrar la mesa
            new_label = simpledialog.askstring("Renombrar Mesa", f"Ingrese nuevo nombre para {mesa['label']}:", initialvalue=mesa['label'])
            if new_label:
                mesas = BusinessLogic.get_mesas()
                for m in mesas:
                    if m["id"] == mesa["id"]:
                        m["label"] = new_label.upper()
                BusinessLogic.set_mesas(mesas)
                self.refresh_mesas()

    def _add_mesa(self):
        mesas = BusinessLogic.get_mesas()
        new_id = f"{len(mesas) + 1:02d}"
        mesas.append({"id": new_id, "label": f"M{new_id}", "ocupada": False, "cliente": ""})
        BusinessLogic.set_mesas(mesas)
        self.refresh_mesas()

    def _remove_mesa(self):
        mesas = BusinessLogic.get_mesas()
        if mesas:
            mesas.pop()
            BusinessLogic.set_mesas(mesas)
            self.refresh_mesas()

    def _on_procesar(self):
        nombre_cliente = self.entry_mesa.get().strip()
        if not nombre_cliente:
            return
            
        mesas = BusinessLogic.get_mesas()
        # Buscar primera mesa libre
        mesa_libre = None
        for m in mesas:
            if not m["ocupada"]:
                mesa_libre = m
                break
        
        if mesa_libre:
            mesa_libre["ocupada"] = True
            mesa_libre["cliente"] = nombre_cliente
            BusinessLogic.set_mesas(mesas)
            from tkinter import messagebox
            messagebox.showinfo("Mesa Asignada", f"Se asignó el cliente '{nombre_cliente}' a la {mesa_libre['label']}")
            self.entry_mesa.delete(0, tk.END)
            self.refresh_mesas()
        else:
            from tkinter import messagebox
            messagebox.showwarning("Sin Mesas", "No hay mesas desocupadas disponibles.")
