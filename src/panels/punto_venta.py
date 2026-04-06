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
        tk.Label(self, text="Modo Panel Deshabilitado. Usa la Vista de Mesas.", fg="white", bg=Theme.APP_BG).pack(pady=50)

class PuntoVentaModal(tk.Toplevel):
    def __init__(self, parent, controller, numero_mesa):
        super().__init__(parent)
        self.controller = controller
        self.billing = BillingLogic()
        self.numero_mesa = numero_mesa
        
        # Variables de control
        self.cart = []
        self.tasa_usd = BusinessLogic.get_tasa_usd()
        self.total_str = tk.StringVar(value="$0.00")
        self.search_query = tk.StringVar()
        
        self.category_frames = {}
        self.expanded_category = None
        
        self._setup_window()
        self._build_ui()

    def _setup_window(self):
        self.title(f"Mesa {self.numero_mesa}")
        self.configure(bg="#2d221c") # Fondo exterior
        
        # Quitar decoración estándar para hacer un modal custom si se quiere, 
        # pero es mas seguro mantener la barra de título o usar overrideredirect(True)
        self.overrideredirect(True)
        self.geometry("900x600")
        UIHelpers.center_window(self, 900, 600)
        self.grab_set() # Hacerlo modal
        
        # Border radius simulado con un frame interior (tkinter puro no tiene esquinas redondeadas en ventanas nativas sin hacks)
        self.main_container = tk.Frame(self, bg="#d9d2cb", highlightthickness=2, highlightbackground="#4a3b34")
        self.main_container.pack(fill="both", expand=True)

    def _build_ui(self):
        # Header del modal
        header = tk.Frame(self.main_container, bg="#3b2b24", pady=10, padx=15)
        header.pack(fill="x")
        
        top_row = tk.Frame(header, bg="#3b2b24")
        top_row.pack(fill="x")
        
        tk.Label(top_row, text=f"🍴 Mesa {self.numero_mesa}", font=("Segoe UI", 16, "bold"), bg="#3b2b24", fg="white").pack(side="left")
        
        tk.Button(top_row, text="✕", font=("Segoe UI", 12, "bold"), bg="#d9d2cb", fg="black", relief="flat", command=self.destroy).pack(side="right", padx=5)
        tk.Button(top_row, text="👤 Cliente", font=("Segoe UI", 10), bg="#5c4a40", fg="white", relief="flat").pack(side="right", padx=10)
        
        tk.Label(header, text="Mesero: Rico Pio", font=("Segoe UI", 9), bg="#3b2b24", fg="#a89a91").pack(anchor="w")

        # Layout a dos columnas
        body = tk.Frame(self.main_container, bg="#d9d2cb")
        body.pack(fill="both", expand=True)
        
        # Panel Izquierdo (Categorías y Buscador)
        left_panel = tk.Frame(body, bg="#d9d2cb", padx=15, pady=15)
        left_panel.pack(side="left", fill="both", expand=True)
        
        # Buscador
        search_f = tk.Frame(left_panel, bg="#4a3b34", padx=10, pady=8)
        search_f.pack(fill="x", pady=(0, 15))
        tk.Label(search_f, text="🔍 Buscar productos...", bg="#4a3b34", fg="#a89a91").pack(side="left")
        
        self.scroll_canvas = tk.Canvas(left_panel, bg="#d9d2cb", highlightthickness=0)
        self.scroll_canvas.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(left_panel, orient="vertical", command=self.scroll_canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.scroll_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.products_container = tk.Frame(self.scroll_canvas, bg="#d9d2cb")
        self.scroll_canvas.create_window((0, 0), window=self.products_container, anchor="nw", tags="frame")
        self.products_container.bind("<Configure>", lambda e: self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all")))
        self.scroll_canvas.bind("<Configure>", lambda e: self.scroll_canvas.itemconfig("frame", width=e.width))

        self._render_accordion()

        # Panel Derecho (Carrito)
        right_panel = tk.Frame(body, bg="#e8e4de", width=320, highlightthickness=1, highlightbackground="#c2b8af")
        right_panel.pack(side="right", fill="y")
        right_panel.pack_propagate(False)
        self._build_cart_panel(right_panel)

    def _build_cart_panel(self, parent):
        # Cabecera Carrito
        hdr = tk.Frame(parent, bg="#3b2b24", pady=10, padx=15)
        hdr.pack(fill="x")
        tk.Label(hdr, text="Pedido Actual", font=("Segoe UI", 12, "bold"), bg="#3b2b24", fg="white").pack(anchor="w")
        self.lbl_items_count = tk.Label(hdr, text="0 productos", font=("Segoe UI", 9), bg="#3b2b24", fg="#a89a91")
        self.lbl_items_count.pack(anchor="w")
        
        # Botones facturación superior
        btn_f = tk.Frame(parent, bg="#e8e4de", pady=10, padx=10)
        btn_f.pack(fill="x")
        tk.Button(btn_f, text="🖨️ Comanda", bg=Theme.SUCCESS, fg="white", font=Theme.FONT_BOLD, relief="flat", width=12).pack(side="left", padx=5)
        tk.Button(btn_f, text="📄 Factura", bg=Theme.BLUE, fg="white", font=Theme.FONT_BOLD, relief="flat", width=12).pack(side="right", padx=5)

        # Area Items
        self.cart_canvas = tk.Canvas(parent, bg="#e8e4de", highlightthickness=0)
        self.cart_canvas.pack(side="top", fill="both", expand=True)
        c_scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.cart_canvas.yview)
        c_scrollbar.pack(side="right", fill="y")
        self.cart_canvas.configure(yscrollcommand=c_scrollbar.set)
        
        self.cart_items_frame = tk.Frame(self.cart_canvas, bg="#e8e4de")
        self.cart_canvas.create_window((0, 0), window=self.cart_items_frame, anchor="nw", tags="frame")
        self.cart_items_frame.bind("<Configure>", lambda e: self.cart_canvas.configure(scrollregion=self.cart_canvas.bbox("all")))
        self.cart_canvas.bind("<Configure>", lambda e: self.cart_canvas.itemconfig("frame", width=e.width))

        # Footer de Totales 
        footer = tk.Frame(parent, bg="#ffffff", padx=15, pady=15, highlightthickness=1, highlightbackground="#c2b8af")
        footer.pack(fill="x", side="bottom")
        
        # Totales
        row_sub = tk.Frame(footer, bg="#ffffff", pady=2)
        row_sub.pack(fill="x")
        tk.Label(row_sub, text="Subtotal", font=("Segoe UI", 10, "bold"), bg="#ffffff", fg="#10b981").pack(side="left")
        self.lbl_subtotal = tk.Label(row_sub, text="$0.00", font=("Segoe UI", 10, "bold"), bg="#ffffff", fg="#10b981")
        self.lbl_subtotal.pack(side="right")

        row_prop = tk.Frame(footer, bg="#ffffff", pady=2)
        row_prop.pack(fill="x")
        tk.Label(row_prop, text="% Propina / Descuento", font=("Segoe UI", 10), bg="#ffffff", fg="#10b981").pack(side="left")
        
        row_tot = tk.Frame(footer, bg=Theme.SUCCESS, pady=8, padx=10)
        row_tot.pack(fill="x", pady=(10, 15))
        tk.Label(row_tot, text="Total", font=("Segoe UI", 12, "bold"), bg=Theme.SUCCESS, fg="white").pack(side="left")
        self.lbl_total = tk.Label(row_tot, text="$0.00", font=("Segoe UI", 12, "bold"), bg=Theme.SUCCESS, fg="white")
        self.lbl_total.pack(side="right")
        
        # Botones finales
        btn_bot = tk.Frame(footer, bg="#ffffff")
        btn_bot.pack(fill="x")
        btn_bot.columnconfigure(0, weight=1)
        btn_bot.columnconfigure(1, weight=1)
        
        tk.Button(btn_bot, text="✕ Cancelar", bg=Theme.DANGER, fg="white", font=Theme.FONT_BOLD, relief="flat", command=self.destroy).grid(row=0, column=0, sticky="ew", padx=(0,5))
        tk.Button(btn_bot, text="💳 Fiar", bg=Theme.ORANGE, fg="white", font=Theme.FONT_BOLD, relief="flat").grid(row=0, column=1, sticky="ew", padx=(5,0))
        
        tk.Button(footer, text="✓ Cobrar", bg="#86efac", fg="#166534", font=Theme.FONT_BOLD, relief="flat", pady=8, command=self._on_procesar).pack(fill="x", pady=(10,0))
        
        self._update_cart_ui() # Inicializar empty state

    def _render_accordion(self):
        for w in self.products_container.winfo_children(): w.destroy()
        grupos = self.billing.get_grupos()
        for g in grupos: self._create_category_row(g)

    def _create_category_row(self, grupo):
        # Color oscuro categoria
        frame = tk.Frame(self.products_container, bg="#d9d2cb", pady=5)
        frame.pack(fill="x")
        
        header = tk.Frame(frame, bg="#4a3b34", pady=12, padx=15, cursor="hand2")
        header.pack(fill="x")
        
        # Simular icono/color
        tk.Label(header, text="🍔" if "Hamburguesa" in grupo["nombre"] else "🏷️", font=("Segoe UI", 12), bg="#4a3b34", fg="white").pack(side="left", padx=(0,10))
        tk.Label(header, text=grupo["nombre"], font=("Segoe UI", 11, "bold"), bg="#4a3b34", fg="white").pack(side="left")
        
        arrow = tk.Label(header, text="▼", font=("Segoe UI", 10), bg="#4a3b34", fg="white")
        arrow.pack(side="right")
        
        prod_frame = tk.Frame(frame, bg="#d9d2cb", pady=5)
        self.category_frames[grupo["id"]] = (prod_frame, arrow)
        
        header.bind("<Button-1>", lambda e, gid=grupo["id"]: self._toggle_category(gid))
        for w in header.winfo_children():
            w.bind("<Button-1>", lambda e, gid=grupo["id"]: self._toggle_category(gid))
            w.config(cursor="hand2")
            
        # Grid productos
        productos = self.billing.get_productos_por_grupo(grupo["id"])
        if productos:
            for i in range(2): prod_frame.columnconfigure(i, weight=1, uniform="p")
            for i, p in enumerate(productos):
                self._create_product_card(prod_frame, p, i)

    def _create_product_card(self, parent, prod, index):
        row, col = divmod(index, 2)
        card = tk.Frame(parent, bg="white", highlightthickness=1, highlightbackground="#c2b8af", pady=10, padx=10, cursor="hand2")
        card.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
        
        tk.Label(card, text=prod["nombre"], font=("Segoe UI", 10, "bold"), bg="white", fg="black").pack(anchor="w")
        tk.Label(card, text=f"${prod['precio_usd']:.2f}", font=("Segoe UI", 10, "bold"), bg="white", fg=Theme.PRIMARY).pack(anchor="w")
        
        def on_click(event, p=prod): self._add_item_to_cart(p)
        card.bind("<Button-1>", on_click)
        for w in card.winfo_children(): w.bind("<Button-1>", on_click); w.config(cursor="hand2")

    def _toggle_category(self, gid):
        frame, arrow = self.category_frames[gid]
        if frame.winfo_viewable():
            frame.pack_forget()
            arrow.config(text="▼")
        else:
            frame.pack(fill="x")
            arrow.config(text="▲")

    def _add_item_to_cart(self, prod):
        for item in self.cart:
            if item['id'] == prod['id']:
                item['cantidad'] += 1
                self._update_cart_ui()
                return
        self.cart.append({'id': prod['id'], 'nombre': prod['nombre'], 'precio_usd': prod['precio_usd'], 'cantidad': 1})
        self._update_cart_ui()

    def _update_cart_ui(self):
        for w in self.cart_items_frame.winfo_children(): w.destroy()
            
        if not self.cart:
            tk.Label(self.cart_items_frame, text="📋", font=("Segoe UI", 32), bg="#e8e4de", fg="#c2b8af").pack(pady=(50, 10))
            tk.Label(self.cart_items_frame, text="No hay productos", font=("Segoe UI", 11, "bold"), bg="#e8e4de", fg="#8a7f76").pack()
            tk.Label(self.cart_items_frame, text="Selecciona productos para agregar", font=("Segoe UI", 9), bg="#e8e4de", fg="#8a7f76").pack()
            self._update_totals_display()
            self.lbl_items_count.config(text="0 productos")
            return

        for i, item in enumerate(self.cart): self._create_cart_item_row(item, i)
        self._update_totals_display()
        self.lbl_items_count.config(text=f"{len(self.cart)} productos")

    def _create_cart_item_row(self, item, index):
        row = tk.Frame(self.cart_items_frame, bg="#ebd5c4", pady=10, padx=10, highlightthickness=1, highlightbackground="#d6c1b1")
        row.pack(fill="x", padx=10, pady=5)
        
        hdr = tk.Frame(row, bg="#ebd5c4")
        hdr.pack(fill="x")
        tk.Label(hdr, text=item["nombre"], font=("Segoe UI", 10, "bold"), bg="#ebd5c4", fg="black").pack(side="left")
        tk.Button(hdr, text="🗑️", bg="#ebd5c4", fg=Theme.DANGER, relief="flat", command=lambda idx=index: self._remove_from_cart(idx)).pack(side="right")
        
        bot = tk.Frame(row, bg="#ebd5c4")
        bot.pack(fill="x", pady=5)
        tk.Label(bot, text=f"${item['precio_usd']:.2f}", font=("Segoe UI", 11, "bold"), bg="#ebd5c4", fg="black").pack(side="left")
        
        ctrl = tk.Frame(bot, bg="#ffffff", highlightthickness=1, highlightbackground="#c2b8af")
        ctrl.pack(side="right")
        tk.Button(ctrl, text=" - ", bg="white", relief="flat", command=lambda it=item: self._adjust_qty(it, -1)).pack(side="left")
        tk.Label(ctrl, text=str(item["cantidad"]), bg="white", width=3, font=("Segoe UI", 10, "bold")).pack(side="left")
        tk.Button(ctrl, text=" + ", bg="white", relief="flat", command=lambda it=item: self._adjust_qty(it, 1)).pack(side="left")

    def _adjust_qty(self, item, delta):
        item['cantidad'] += delta
        if item['cantidad'] <= 0: self.cart.remove(item)
        self._update_cart_ui()

    def _remove_from_cart(self, index):
        self.cart.pop(index)
        self._update_cart_ui()

    def _update_totals_display(self):
        subtotal_usd = sum(item['precio_usd'] * item['cantidad'] for item in self.cart)
        self.lbl_subtotal.config(text=f"${subtotal_usd:.2f}")
        self.lbl_total.config(text=f"${subtotal_usd:.2f}")

    def _on_procesar(self):
        if not self.cart: return messagebox.showwarning("Vacio", "Agrega productos primero.")
        messagebox.showinfo("Exito", "Cobro simulado completado.")
        self.destroy()
