import tkinter as tk
from tkinter import ttk, messagebox, colorchooser, filedialog
from theme import Theme
from ui_helpers import UIHelpers
from billing_logic import BillingLogic
import os

class ArticulosInventarioDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Consulta y Mantenimiento de Inventario")
        self.geometry("1200x850")
        self.minsize(900, 600)
        self.configure(bg=Theme.APP_BG)
        self.resizable(True, True)
        self.transient(parent)
        self.grab_set()

        self.billing = BillingLogic()
        self.grupos = self.billing.get_grupos()
        self.nombres_grupos = [f"{g['codigo']} - {g['nombre']}" for g in self.grupos]
        
        self.current_prod_id = None
        self.is_editing = False # Controla si el formulario está activo
        
        # Filtro Maestro
        self.v_filtro_grupo = tk.StringVar()
        self.v_busqueda_rapida = tk.StringVar()

        # Variables Formulario
        self.v_codigo = tk.StringVar()
        self.v_nombre = tk.StringVar()
        self.v_precio = tk.StringVar(value="0.0")
        self.v_iva = tk.StringVar(value="IVA 16%")
        self.v_color = tk.StringVar(value="#CCCCCC")
        self.v_imagen = tk.StringVar(value="")

        self._build_ui()
        self._set_form_state(tk.DISABLED)
        self._cargar_productos()

    def _build_ui(self):
        UIHelpers.create_header(self, "Consulta y Gestión de Inventario")
        
        main_container = tk.Frame(self, bg=Theme.APP_BG)
        main_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Configure grid for main_container
        main_container.grid_rowconfigure(3, weight=1) # Row for tree_frame
        main_container.grid_columnconfigure(0, weight=1) # Single column for all elements

        # --- BARRA SUPERIOR: FILTRO MAESTRO Y BUSCADOR ---
        filter_bar = tk.Frame(main_container, bg=Theme.DARK_PANEL, pady=10, padx=15)
        filter_bar.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        
        tk.Label(filter_bar, text="Grupo Activo:", font=Theme.FONT_BOLD, bg=Theme.DARK_PANEL, fg="white").pack(side="left")
        
        self.cb_filtro_grupo = ttk.Combobox(filter_bar, textvariable=self.v_filtro_grupo, values=["TODOS LOS GRUPOS"] + self.nombres_grupos, state="readonly", width=35, font=Theme.FONT_BODY)
        self.cb_filtro_grupo.pack(side="left", padx=(10, 30), ipady=4)
        self.cb_filtro_grupo.current(0)
        self.cb_filtro_grupo.bind("<<ComboboxSelected>>", self._on_grupo_changed)
        
        tk.Label(filter_bar, text="Buscador Universal:", font=Theme.FONT_BOLD, bg=Theme.DARK_PANEL, fg="white").pack(side="left")
        self.e_search = tk.Entry(filter_bar, textvariable=self.v_busqueda_rapida, font=Theme.FONT_BODY, width=35, relief="flat", highlightthickness=1)
        self.e_search.pack(side="left", padx=10, ipady=4)
        self.e_search.bind("<KeyRelease>", lambda e: self._cargar_productos())
        
        # --- PANEL CENTRAL: FORMULARIO DE EDICIÓN ---
        self.form_frame = tk.LabelFrame(main_container, text=" Propiedades del Producto ", bg=Theme.SURFACE, font=Theme.FONT_BOLD, padx=15, pady=15)
        self.form_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        
        # Fila 1
        r1 = tk.Frame(self.form_frame, bg=Theme.SURFACE)
        r1.pack(fill="x", pady=5)
        tk.Label(r1, text="Código:", font=Theme.FONT_SMALL, bg=Theme.SURFACE, width=15, anchor="w").pack(side="left")
        self.ent_codigo = tk.Entry(r1, textvariable=self.v_codigo, width=15, relief="flat", highlightbackground=Theme.BORDER, highlightthickness=1)
        self.ent_codigo.pack(side="left", padx=(0, 20), ipady=3)
        
        tk.Label(r1, text="Nombre/Desc.:", font=Theme.FONT_SMALL, bg=Theme.SURFACE, width=15, anchor="w").pack(side="left")
        self.ent_nombre = tk.Entry(r1, textvariable=self.v_nombre, relief="flat", highlightbackground=Theme.BORDER, highlightthickness=1)
        self.ent_nombre.pack(side="left", fill="x", expand=True, ipady=3)
        
        # Fila 2
        r2 = tk.Frame(self.form_frame, bg=Theme.SURFACE)
        r2.pack(fill="x", pady=5)
        tk.Label(r2, text="Precio USD:", font=Theme.FONT_SMALL, bg=Theme.SURFACE, width=15, anchor="w").pack(side="left")
        self.ent_precio = tk.Entry(r2, textvariable=self.v_precio, width=15, relief="flat", highlightbackground=Theme.BORDER, highlightthickness=1)
        self.ent_precio.pack(side="left", padx=(0, 20), ipady=3)
        
        tk.Label(r2, text="Impuesto:", font=Theme.FONT_SMALL, bg=Theme.SURFACE, width=15, anchor="w").pack(side="left")
        self.cb_iva = ttk.Combobox(r2, textvariable=self.v_iva, values=["IVA 16%", "Exento", "Reducido 8%"], width=15, state="readonly")
        self.cb_iva.pack(side="left", ipady=3)

        # Fila 3: Atributos visuales
        r3 = tk.Frame(self.form_frame, bg=Theme.SURFACE)
        r3.pack(fill="x", pady=5)
        tk.Label(r3, text="Color Táctil:", font=Theme.FONT_SMALL, bg=Theme.SURFACE, width=15, anchor="w").pack(side="left")
        self.btn_color = tk.Button(r3, text="Elegir Color", bg="#CCCCCC", fg="black", relief="flat", command=self._elegir_color, highlightbackground=Theme.BORDER, highlightthickness=1)
        self.btn_color.pack(side="left", padx=(0, 20), ipadx=10, ipady=1)
        
        tk.Label(r3, text="Imagen:", font=Theme.FONT_SMALL, bg=Theme.SURFACE, width=15, anchor="w").pack(side="left")
        self.ent_imagen = tk.Entry(r3, textvariable=self.v_imagen, state="readonly", width=40, relief="flat")
        self.ent_imagen.pack(side="left", ipady=3)
        self.btn_sel_imagen = tk.Button(r3, text="Examinar", command=self._elegir_imagen, bg="#E0E0E0", relief="flat")
        self.btn_sel_imagen.pack(side="left", padx=5)
        self.btn_clear_img = tk.Button(r3, text="X", command=lambda: self.v_imagen.set(""), fg="red", bg="#E0E0E0", relief="flat")
        self.btn_clear_img.pack(side="left")

        # --- BOTONERA CRUD ---
        ctrl_frame = tk.Frame(main_container, bg=Theme.APP_BG)
        ctrl_frame.grid(row=2, column=0, sticky="ew", pady=(0, 15))
        
        self.btn_nuevo = tk.Button(ctrl_frame, text="✨ Nuevo Producto", bg=Theme.ACCENT, fg="white", font=Theme.FONT_BOLD, relief="flat", command=self._iniciar_nuevo, padx=20)
        self.btn_nuevo.pack(side="left", padx=5)
        
        self.btn_guardar = tk.Button(ctrl_frame, text="🖫 Guardar/Actualizar", bg=Theme.PRIMARY, fg="white", font=Theme.FONT_BOLD, relief="flat", command=self._guardar, padx=20)
        self.btn_guardar.pack(side="left", padx=5)
        
        self.btn_cancelar = tk.Button(ctrl_frame, text="🚫 Cancelar", bg=Theme.TEXT_SECONDARY, fg="white", font=Theme.FONT_BOLD, relief="flat", command=self._cancelar, padx=20)
        self.btn_cancelar.pack(side="left", padx=5)
        
        self.btn_eliminar = tk.Button(ctrl_frame, text="🗑 Eliminar", bg="white", fg=Theme.DANGER, font=Theme.FONT_BOLD, relief="flat", command=self._eliminar, padx=20)
        self.btn_eliminar.pack(side="right", padx=5)

        # --- TABLA DE INVENTARIO (TREEVIEW) - TOTALMENTE EXPANSIBLE ---
        tree_frame = tk.Frame(main_container, bg="white", highlightthickness=1, highlightbackground=Theme.BORDER)
        tree_frame.grid(row=3, column=0, sticky="nsew")
        # Permitir que el Treeview se expanda dentro del frame
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        cols = ("ID", "Código", "Grupo", "Nombre o Descripción", "Precio USD")
        # Sin height fijo: el grid con nsew controla el tamaño
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings")
        
        self.tree.heading("ID", text="ID")
        self.tree.column("ID", width=0, stretch=tk.NO)  # Oculto
        
        self.tree.heading("Código", text="Código")
        self.tree.column("Código", width=120, anchor="center", minwidth=80)
        
        self.tree.heading("Grupo", text="Grupo")
        self.tree.column("Grupo", width=200, anchor="w", minwidth=120)
        
        self.tree.heading("Nombre o Descripción", text="Nombre del Artículo")
        self.tree.column("Nombre o Descripción", width=450, anchor="w", minwidth=200, stretch=True)
        
        self.tree.heading("Precio USD", text="Precio (USD)")
        self.tree.column("Precio USD", width=140, anchor="e", minwidth=100)
        
        scroll_y = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scroll_x = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        # Usar grid dentro de tree_frame para coordinar scrollbars
        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        
        self.tree.bind("<Double-1>", self._on_tree_select)
        
        # Estilos visuales del treeview
        style = ttk.Style()
        style.configure("Treeview.Heading", font=Theme.FONT_BOLD)
        style.configure("Treeview", font=Theme.FONT_BODY, rowheight=30)
        
        # Footer (siempre al fondo, fuera del grid expansible)
        footer = tk.Frame(self, bg=Theme.FOOTER_BG, pady=10, padx=20)
        footer.pack(fill="x", side="bottom")
        tk.Button(footer, text="Cerrar", font=Theme.FONT_BOLD, bg="white", fg=Theme.TEXT_SECONDARY, relief="flat", command=self.destroy).pack(side="right")

    def _set_form_state(self, state):
        """Activa o desactiva los controles del formulario."""
        self.ent_codigo.config(state=state)
        self.ent_nombre.config(state=state)
        self.ent_precio.config(state=state)
        self.cb_iva.config(state=state if state == tk.DISABLED else "readonly")
        
        if state == tk.DISABLED:
            self.btn_color.config(state=tk.DISABLED)
            self.btn_sel_imagen.config(state=tk.DISABLED)
            self.btn_clear_img.config(state=tk.DISABLED)
            self.btn_guardar.config(state=tk.DISABLED)
            self.btn_cancelar.config(state=tk.DISABLED)
            self.btn_eliminar.config(state=tk.DISABLED)
            self.is_editing = False
        else:
            self.btn_color.config(state=tk.NORMAL)
            self.btn_sel_imagen.config(state=tk.NORMAL)
            self.btn_clear_img.config(state=tk.NORMAL)
            self.btn_guardar.config(state=tk.NORMAL)
            self.btn_cancelar.config(state=tk.NORMAL)
            self.is_editing = True
            
            if self.current_prod_id:
                self.btn_eliminar.config(state=tk.NORMAL)
            else:
                self.btn_eliminar.config(state=tk.DISABLED)

    def _on_grupo_changed(self, event=None):
        grupo_seleccionado = self.v_filtro_grupo.get()
        # Si se cambia el filtro maestro, abortamos cualquier edición en curso
        if self.is_editing:
            res = messagebox.askyesno("Confirmar", "Tiene una edición en curso. ¿Desea descartarla al cambiar de grupo?")
            if res:
                self._cancelar()
            else:
                return
                
        # Habilitar o Deshabilitar "Nuevo Producto" según filtro
        if grupo_seleccionado == "TODOS LOS GRUPOS":
            self.btn_nuevo.config(state=tk.DISABLED, bg=Theme.BORDER)
        else:
            self.btn_nuevo.config(state=tk.NORMAL, bg=Theme.ACCENT)
            
        self._cargar_productos()

    def _cargar_productos(self):
        # Limpiar tree
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        termino = self.v_busqueda_rapida.get().strip()
        filtro_grupo = self.v_filtro_grupo.get()
        
        # Si hay término de búsqueda, ignora el filtro de grupo y busca globalmente
        if termino:
            prods = self.billing.buscar_productos(termino)
        else:
            if filtro_grupo == "TODOS LOS GRUPOS":
                prods = self.billing.get_todos_productos()
            else:
                # Extraer código del grupo ("01 - PIZZAS" -> "01")
                codigo_grupo = filtro_grupo.split(" - ")[0]
                grupo_id = next((g["id"] for g in self.grupos if str(g["codigo"]) == codigo_grupo), None)
                prods = self.billing.get_productos_por_grupo(grupo_id) if grupo_id else []
                
        for p in prods:
            grupo_txt = p.get('grupo_nombre', 'N/A')
            self.tree.insert("", tk.END, values=(p['id'], p['codigo'], grupo_txt, p['nombre'], f"{p['precio_usd']:.2f}"))

    def _iniciar_nuevo(self):
        grupo_seleccionado = self.v_filtro_grupo.get()
        if grupo_seleccionado == "TODOS LOS GRUPOS":
            messagebox.showwarning("Atención", "Debe seleccionar un Grupo específico en la parte superior antes de crear un producto.")
            return

        self.current_prod_id = None
        self.v_codigo.set("")
        self.v_nombre.set("")
        self.v_precio.set("0.0")
        self.v_iva.set("IVA 16%")
        self.v_color.set("#CCCCCC")
        self.v_imagen.set("")
        self.btn_color.configure(bg="#CCCCCC", fg="black")
        
        self._set_form_state(tk.NORMAL)
        self.ent_codigo.focus()

    def _on_tree_select(self, event):
        seleccion = self.tree.selection()
        if not seleccion: return
        
        # Descartar edición previa si es necesario
        if self.is_editing and self.current_prod_id is None:
            if not messagebox.askyesno("Confirmar", "¿Desea descartar la creación del nuevo producto?"):
                return
                
        item = self.tree.item(seleccion[0])
        prod_id = item['values'][0]
        
        prods = self.billing.get_todos_productos()
        prod_db = next((p for p in prods if p['id'] == prod_id), None)
        
        if prod_db:
            self.current_prod_id = prod_db['id']
            # Para editar, igualamos el filtro maestro al grupo del producto temporalmente si no estábamos buscando
            if self.v_busqueda_rapida.get().strip() == "":
                for g_txt in self.nombres_grupos:
                    if g_txt.startswith(f"{prod_db.get('grupo_id', '')} -") or (prod_db.get('grupo_nombre') and prod_db.get('grupo_nombre') in g_txt):
                        self.v_filtro_grupo.set(g_txt)
                        self._on_grupo_changed()
                        break

            self.v_codigo.set(prod_db['codigo'])
            self.v_nombre.set(prod_db['nombre'])
            self.v_precio.set(str(prod_db['precio_usd']))
            
            if prod_db['iva_porcentaje'] == 0: self.v_iva.set("Exento")
            elif prod_db['iva_porcentaje'] == 0.08: self.v_iva.set("Reducido 8%")
            else: self.v_iva.set("IVA 16%")
            
            cc = prod_db.get('color') or '#CCCCCC'
            self.v_color.set(cc)
            self.btn_color.configure(bg=cc, fg="white" if int(cc[1:3],16)<150 else "black")
            
            self.v_imagen.set(prod_db.get('imagen_path') or '')
            
            self._set_form_state(tk.NORMAL)

    def _cancelar(self):
        self._set_form_state(tk.DISABLED)
        self.current_prod_id = None
        self.v_codigo.set("")
        self.v_nombre.set("")
        self.v_precio.set("0.0")
        self.v_color.set("#CCCCCC")
        self.btn_color.configure(bg="#CCCCCC", fg="black")

    def _obtener_grupo_id_actual(self):
        # El grupo SIEMPRE será el que esté seleccionado en el Filtro Maestro
        grupo_str = self.v_filtro_grupo.get()
        if grupo_str == "TODOS LOS GRUPOS": return None
        
        codigo = grupo_str.split(" - ")[0]
        for g in self.grupos:
            if str(g["codigo"]) == codigo:
                return g["id"]
        return None

    def _guardar(self):
        codigo = self.v_codigo.get().strip()
        nombre = self.v_nombre.get().strip()
        precio_str = self.v_precio.get().strip()
        
        if not codigo or not nombre:
            messagebox.showwarning("Incompleto", "Código y Nombre son obligatorios.")
            return
            
        try: precio = float(precio_str)
        except ValueError:
            messagebox.showerror("Error", "Precio inválido.")
            return
            
        grupo_id = self._obtener_grupo_id_actual()
        if not grupo_id:
            messagebox.showerror("Error de Flujo", "No se puede guardar. Asegúrese de tener un Grupo seleccionado en la barra superior.")
            return
        
        iva_val = 0.16
        if "Exento" in self.v_iva.get(): iva_val = 0.0
        elif "8%" in self.v_iva.get(): iva_val = 0.08
        
        color = self.v_color.get()
        img = self.v_imagen.get()
        
        try:
            if self.current_prod_id is None:
                self.billing.registrar_producto(codigo, nombre, precio, grupo_id, iva_val, color, img)
            else:
                self.billing.actualizar_producto(self.current_prod_id, codigo, nombre, precio, grupo_id, iva_val, color, img)
                
            # Limpiar barra de búsqueda al guardar para refrescar listado normal
            self.v_busqueda_rapida.set("")
            self._cargar_productos()
            self._cancelar()
            messagebox.showinfo("Éxito", "Operación Completada.")
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                messagebox.showerror("Código Duplicado", "Ya existe un producto con este código.")
            else:
                messagebox.showerror("Error SQL", f"No se pudo guardar: {e}")

    def _eliminar(self):
        if self.current_prod_id is None: return
        if messagebox.askyesno("Confirmar Peligro", f"¿Eliminar DEFINITIVAMENTE el producto '{self.v_nombre.get()}'?"):
            try:
                self.billing.eliminar_producto(self.current_prod_id)
                self.v_busqueda_rapida.set("")
                self._cargar_productos()
                self._cancelar()
                messagebox.showinfo("Eliminado", "Fila eliminada de la base de datos.")
            except Exception as e:
                messagebox.showerror("Error", f"Verifique integridad SQL:\n{e}")

    def _elegir_color(self):
        color_code = colorchooser.askcolor(title="Elige el color táctil", initialcolor=self.v_color.get())
        if color_code[1]:
            self.v_color.set(color_code[1])
            self.btn_color.configure(bg=color_code[1], fg="white" if int(color_code[1][1:3],16)<150 else "black")

    def _elegir_imagen(self):
        ruta = filedialog.askopenfilename(title="Seleccionar foto", filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.gif")])
        if ruta:
            self.v_imagen.set(ruta)
