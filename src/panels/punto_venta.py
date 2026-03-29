import tkinter as tk
from tkinter import ttk, messagebox
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
        self.cart = []
        self.tasa_usd = BusinessLogic.get_tasa_usd()
        self.total_str = tk.StringVar(value="0,00")
        self.total_usd_str = tk.StringVar(value="0,00 $")
        self.tasa_str = tk.StringVar(value=f"({self.tasa_usd:.2f})")
        self.search_query = tk.StringVar()
        
        # Tracking de UI
        self.category_frames = {} # {id: frame_de_productos}
        self.expanded_category = None
        
        self._build_ui()

    def _build_ui(self):
        # Header (Top Bar)
        header = tk.Frame(self, bg=Theme.SURFACE, height=60, highlightthickness=1, highlightbackground=Theme.BORDER)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="RICO PÍO", font=("Segoe UI", 18, "bold"), bg=Theme.SURFACE, fg=Theme.PRIMARY).pack(side="left", padx=20)
        tk.Label(header, text="Punto de Venta", font=Theme.FONT_H3, bg=Theme.SURFACE, fg=Theme.TEXT_SECONDARY).pack(side="left")
        
        # Botones de Acción Derecha
        btn_frame = tk.Frame(header, bg=Theme.SURFACE)
        btn_frame.pack(side="right", padx=10)
        
        # Tasa USD
        tasa_container = tk.Frame(btn_frame, bg=Theme.SURFACE_LIGHT, padx=10, pady=5)
        tasa_container.pack(side="left", padx=10)
        tk.Label(tasa_container, text="TASA USD", font=Theme.FONT_SMALL, bg=Theme.SURFACE_LIGHT, fg=Theme.TEXT_SECONDARY).pack()
        tk.Label(tasa_container, textvariable=self.tasa_str, font=Theme.FONT_BOLD, bg=Theme.SURFACE_LIGHT, fg=Theme.ACCENT).pack()

        # Botón Logout
        tk.Button(btn_frame, text="Cerrar Sesión", bg=Theme.DANGER, fg="white", font=Theme.FONT_BOLD, 
                  relief="flat", padx=15, pady=8, command=self.controller.mostrar_login).pack(side="left", padx=5)

        # Contenedor Principal (2 Columnas)
        main_body = tk.Frame(self, bg=Theme.APP_BG)
        main_body.pack(fill="both", expand=True, padx=10, pady=10)
        
        # --- COLUMNA DERECHA (Selección de Productos - Mayor peso) ---
        selection_panel = tk.Frame(main_body, bg=Theme.APP_BG)
        selection_panel.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # Buscador
        search_frame = tk.Frame(selection_panel, bg=Theme.SURFACE, padx=10, pady=10, highlightthickness=1, highlightbackground=Theme.BORDER)
        search_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(search_frame, text="🔍", bg=Theme.SURFACE, font=Theme.FONT_H2).pack(side="left", padx=(5, 10))
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_query, font=Theme.FONT_H2, 
                                     bg=Theme.SURFACE, fg=Theme.TEXT_PRIMARY, relief="flat", insertbackground="white")
        self.search_entry.pack(side="left", fill="x", expand=True)
        self.search_query.trace_add("write", lambda *args: self._on_search())
        
        # Scrollable Area para Categorías/Productos
        self.scroll_canvas = tk.Canvas(selection_panel, bg=Theme.APP_BG, highlightthickness=0)
        self.scroll_canvas.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(selection_panel, orient="vertical", command=self.scroll_canvas.yview)
        scrollbar.pack(side="right", fill="y")
        
        self.scroll_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.products_container = tk.Frame(self.scroll_canvas, bg=Theme.APP_BG)
        self.scroll_canvas.create_window((0, 0), window=self.products_container, anchor="nw", tags="frame")
        
        self.products_container.bind("<Configure>", lambda e: self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all")))
        self.scroll_canvas.bind("<Configure>", lambda e: self.scroll_canvas.itemconfig("frame", width=e.width))

        self._render_accordion()

        # --- COLUMNA IZQUIERDA (Carrito - Menor peso pero fijo) ---
        cart_panel = tk.Frame(main_body, bg=Theme.SURFACE, width=380, highlightthickness=1, highlightbackground=Theme.BORDER)
        cart_panel.pack(side="left", fill="y", padx=(0, 5))
        cart_panel.pack_propagate(False)
        
        self._build_cart_panel(cart_panel)

    def _build_cart_panel(self, parent):
        # Cabecera Carrito
        tk.Label(parent, text="PEDIDO ACTUAL", font=Theme.FONT_H2, bg=Theme.SURFACE, fg=Theme.TEXT_SECONDARY, pady=15).pack()
        
        # Area de Items (Scrollable)
        items_outer = tk.Frame(parent, bg=Theme.SURFACE)
        items_outer.pack(fill="both", expand=True, padx=5)
        
        self.cart_canvas = tk.Canvas(items_outer, bg=Theme.SURFACE, highlightthickness=0)
        self.cart_canvas.pack(side="left", fill="both", expand=True)
        
        c_scrollbar = ttk.Scrollbar(items_outer, orient="vertical", command=self.cart_canvas.yview)
        c_scrollbar.pack(side="right", fill="y")
        
        self.cart_canvas.configure(yscrollcommand=c_scrollbar.set)
        self.cart_items_frame = tk.Frame(self.cart_canvas, bg=Theme.SURFACE)
        self.cart_canvas.create_window((0, 0), window=self.cart_items_frame, anchor="nw", tags="frame")
        
        self.cart_items_frame.bind("<Configure>", lambda e: self.cart_canvas.configure(scrollregion=self.cart_canvas.bbox("all")))
        self.cart_canvas.bind("<Configure>", lambda e: self.cart_canvas.itemconfig("frame", width=e.width))

        # Footer de Totales (Sticky)
        footer = tk.Frame(parent, bg=Theme.SURFACE_LIGHT, padx=20, pady=20)
        footer.pack(fill="x", side="bottom")
        
        row_sub = tk.Frame(footer, bg=Theme.SURFACE_LIGHT)
        row_sub.pack(fill="x")
        tk.Label(row_sub, text="Subtotal", font=Theme.FONT_BODY, bg=Theme.SURFACE_LIGHT, fg=Theme.TEXT_SECONDARY).pack(side="left")
        self.lbl_subtotal = tk.Label(row_sub, text="0,00 $", font=Theme.FONT_BOLD, bg=Theme.SURFACE_LIGHT, fg=Theme.TEXT_PRIMARY)
        self.lbl_subtotal.pack(side="right")

        row_iva = tk.Frame(footer, bg=Theme.SURFACE_LIGHT, pady=5)
        row_iva.pack(fill="x")
        tk.Label(row_iva, text="I.V.A (16%)", font=Theme.FONT_BODY, bg=Theme.SURFACE_LIGHT, fg=Theme.TEXT_SECONDARY).pack(side="left")
        self.lbl_iva = tk.Label(row_iva, text="0,00 $", font=Theme.FONT_BOLD, bg=Theme.SURFACE_LIGHT, fg=Theme.TEXT_PRIMARY)
        self.lbl_iva.pack(side="right")

        tk.Frame(footer, bg=Theme.BORDER, height=1).pack(fill="x", pady=10)

        row_total = tk.Frame(footer, bg=Theme.SURFACE_LIGHT)
        row_total.pack(fill="x")
        tk.Label(row_total, text="TOTAL", font=Theme.FONT_H2, bg=Theme.SURFACE_LIGHT, fg=Theme.PRIMARY).pack(side="left")
        
        totals_stack = tk.Frame(row_total, bg=Theme.SURFACE_LIGHT)
        totals_stack.pack(side="right", anchor="e")
        tk.Label(totals_stack, textvariable=self.total_str, font=("Segoe UI", 24, "bold"), bg=Theme.SURFACE_LIGHT, fg=Theme.PRIMARY).pack(anchor="e")
        tk.Label(totals_stack, textvariable=self.total_usd_str, font=Theme.FONT_BOLD, bg=Theme.SURFACE_LIGHT, fg=Theme.ACCENT).pack(anchor="e")

        # Botón Cobrar
        btn_pay = tk.Button(footer, text="Finalizar y Cobrar", bg=Theme.PRIMARY, fg="white", font=Theme.FONT_H2, 
                            relief="flat", pady=12, command=self._on_procesar)
        btn_pay.pack(fill="x", pady=(20, 0))

    def _render_accordion(self):
        # Limpiar
        for w in self.products_container.winfo_children():
            w.destroy()
        
        grupos = self.billing.get_grupos()
        for g in grupos:
            self._create_category_row(g)

    def _create_category_row(self, grupo):
        frame = tk.Frame(self.products_container, bg=Theme.SURFACE, pady=2, highlightthickness=1, highlightbackground=Theme.BORDER)
        frame.pack(fill="x", pady=2)
        
        # Header del acordeón
        header = tk.Frame(frame, bg=Theme.SURFACE, cursor="hand2")
        header.pack(fill="x", padx=15, pady=10)
        
        color_dot = tk.Frame(header, bg=grupo.get("color", Theme.TEXT_SECONDARY), width=12, height=12)
        color_dot.pack(side="left", padx=(0, 10))
        color_dot.pack_propagate(False)

        tk.Label(header, text=grupo["nombre"].upper(), font=Theme.FONT_BOLD, bg=Theme.SURFACE, fg=Theme.TEXT_PRIMARY).pack(side="left")
        
        arrow = tk.Label(header, text="▼", font=Theme.FONT_SMALL, bg=Theme.SURFACE, fg=Theme.TEXT_SECONDARY)
        arrow.pack(side="right")
        
        # Contenedor de productos (oculto por defecto)
        prod_frame = tk.Frame(frame, bg=Theme.APP_BG, pady=10)
        self.category_frames[grupo["id"]] = (prod_frame, arrow)
        
        # Eventos de toggle
        for widget in [header, color_dot]:
            widget.bind("<Button-1>", lambda e, gid=grupo["id"]: self._toggle_category(gid))
        
        # Grid para productos dentro de la categoría
        productos = self.billing.get_productos_por_grupo(grupo["id"])
        if not productos:
            tk.Label(prod_frame, text="No hay productos en esta categoría", font=Theme.FONT_SMALL, bg=Theme.APP_BG, fg=Theme.TEXT_SECONDARY).pack()
        else:
            grid_cont = tk.Frame(prod_frame, bg=Theme.APP_BG)
            grid_cont.pack(fill="x", padx=10)
            for i in range(4): grid_cont.columnconfigure(i, weight=1, uniform="gp")
            
            for i, p in enumerate(productos):
                self._create_product_card(grid_cont, p, i)

    def _create_product_card(self, parent, prod, index):
        row, col = divmod(index, 4)
        card = tk.Frame(parent, bg=Theme.SURFACE_LIGHT, highlightthickness=1, highlightbackground=Theme.BORDER, cursor="hand2")
        card.grid(row=row, column=col, sticky="nsew", padx=4, pady=4)
        
        lbl_nombre = tk.Label(card, text=prod["nombre"], font=Theme.FONT_BOLD, bg=Theme.SURFACE_LIGHT, fg=Theme.TEXT_PRIMARY, wraplength=120, cursor="hand2")
        lbl_nombre.pack(pady=(15, 5))
        lbl_precio = tk.Label(card, text=f"${prod['precio_usd']:.2f}", font=Theme.FONT_H3, bg=Theme.SURFACE_LIGHT, fg=Theme.ACCENT, cursor="hand2")
        lbl_precio.pack(pady=(0, 15))
        
        # Al hacer clic en la tarjeta o etiquetas, agregar al carrito
        def on_click(event, p=prod):
            self._add_item_to_cart(p)
            
        card.bind("<Button-1>", on_click)
        lbl_nombre.bind("<Button-1>", on_click)
        lbl_precio.bind("<Button-1>", on_click)

    def _toggle_category(self, gid):
        frame, arrow = self.category_frames[gid]
        if frame.winfo_viewable():
            frame.pack_forget()
            arrow.config(text="▼")
        else:
            # Cerrar anterior si queremos comportamiento acordeón único (opcional)
            # if self.expanded_category and self.expanded_category != gid:
            #     f, a = self.category_frames[self.expanded_category]
            #     f.pack_forget()
            #     a.config(text="▼")
            
            frame.pack(fill="x")
            arrow.config(text="▲")
            self.expanded_category = gid

    def _on_search(self, *args):
        query = self.search_query.get().lower().strip()
        if not query:
            self._render_accordion()
            return
        
        # Mostrar resultados de búsqueda (aplanado)
        for w in self.products_container.winfo_children():
            w.destroy()
            
        resultados = self.billing.buscar_productos(query)
        if not resultados:
            tk.Label(self.products_container, text="No se encontraron productos", font=Theme.FONT_H2, bg=Theme.APP_BG, fg=Theme.TEXT_SECONDARY, pady=50).pack()
            return

        grid_cont = tk.Frame(self.products_container, bg=Theme.APP_BG)
        grid_cont.pack(fill="x", padx=20, pady=20)
        for i in range(4): grid_cont.columnconfigure(i, weight=1, uniform="search")
        
        for i, p in enumerate(resultados):
            self._create_product_card(grid_cont, p, i)

    def _add_item_to_cart(self, prod):
        for item in self.cart:
            if item['id'] == prod['id']:
                item['cantidad'] += 1
                self._update_cart_ui()
                return
        
        self.cart.append({
            'id': prod['id'],
            'nombre': prod['nombre'],
            'precio_usd': prod['precio_usd'],
            'cantidad': 1,
            'iva_porcentaje': prod.get('iva_porcentaje', 0.16)
        })
        self._update_cart_ui()

    def _update_cart_ui(self):
        # Limpiar items actuales
        for w in self.cart_items_frame.winfo_children():
            w.destroy()
            
        if not self.cart:
            tk.Label(self.cart_items_frame, text="El carrito está vacío", bg=Theme.SURFACE, fg=Theme.TEXT_SECONDARY, pady=50).pack()
            self._update_totals_display()
            return

        for i, item in enumerate(self.cart):
            self._create_cart_item_row(item, i)
        
        self._update_totals_display()

    def _create_cart_item_row(self, item, index):
        row = tk.Frame(self.cart_items_frame, bg=Theme.SURFACE, pady=8)
        row.pack(fill="x", padx=5)
        
        # Info Producto
        info = tk.Frame(row, bg=Theme.SURFACE)
        info.pack(side="left", fill="both", expand=True)
        tk.Label(info, text=item["nombre"], font=Theme.FONT_BOLD, bg=Theme.SURFACE, fg=Theme.TEXT_PRIMARY, anchor="w").pack(fill="x")
        tk.Label(info, text=f"${item['precio_usd']:.2f} c/u", font=Theme.FONT_SMALL, bg=Theme.SURFACE, fg=Theme.TEXT_SECONDARY, anchor="w").pack(fill="x")
        
        # Controles de Cantidad
        ctrl = tk.Frame(row, bg=Theme.SURFACE)
        ctrl.pack(side="right")
        
        # Botones circulares simulados
        tk.Button(ctrl, text="-", font=Theme.FONT_BOLD, bg=Theme.SURFACE_LIGHT, fg=Theme.TEXT_PRIMARY, relief="flat", width=2, 
                  command=lambda it=item: self._adjust_qty(it, -1)).pack(side="left", padx=2)
        
        tk.Label(ctrl, text=str(item["cantidad"]), font=Theme.FONT_BOLD, bg=Theme.SURFACE, fg=Theme.PRIMARY, width=3).pack(side="left")
        
        tk.Button(ctrl, text="+", font=Theme.FONT_BOLD, bg=Theme.SURFACE_LIGHT, fg=Theme.TEXT_PRIMARY, relief="flat", width=2, 
                  command=lambda it=item: self._adjust_qty(it, 1)).pack(side="left", padx=2)
        
        # Botón eliminar
        tk.Button(ctrl, text="✕", font=Theme.FONT_SMALL, bg=Theme.SURFACE, fg=Theme.DANGER, relief="flat", 
                  command=lambda idx=index: self._remove_from_cart(idx)).pack(side="left", padx=(10, 0))

        tk.Frame(self.cart_items_frame, bg=Theme.BORDER, height=1).pack(fill="x", padx=10)

    def _adjust_qty(self, item, delta):
        item['cantidad'] += delta
        if item['cantidad'] <= 0:
            self.cart.remove(item)
        self._update_cart_ui()

    def _remove_from_cart(self, index):
        self.cart.pop(index)
        self._update_cart_ui()

    def _update_totals_display(self):
        subtotal_usd = sum(item['precio_usd'] * item['cantidad'] for item in self.cart)
        iva_usd = sum(item['precio_usd'] * item['cantidad'] * item['iva_porcentaje'] for item in self.cart)
        total_usd = subtotal_usd + iva_usd
        total_bs = total_usd * self.tasa_usd
        
        self.total_str.set(f"{total_bs:,.2f}")
        self.total_usd_str.set(f"{total_usd:,.2f} $")
        
        self.lbl_subtotal.config(text=f"{subtotal_usd:,.2f} $")
        self.lbl_iva.config(text=f"{iva_usd:,.2f} $")

    def _on_procesar(self):
        if not self.cart:
            messagebox.showwarning("Carrito Vacío", "No hay productos para procesar.")
            return
        
        if messagebox.askyesno("Confirmar Pago", f"¿Desea finalizar la venta por un total de {self.total_str.get()} Bs?"):
            # Aquí iría la lógica de guardar factura en DB...
            messagebox.showinfo("Venta Exitosa", "La venta ha sido procesada correctamente.")
            self.cart = []
            self._update_cart_ui()
            self._render_accordion() # Reset view

    # Dummy methods for compatibility if called from elsewhere
    def refresh_mesas(self): pass
    def _render_grupos_grid(self): self._render_accordion()
