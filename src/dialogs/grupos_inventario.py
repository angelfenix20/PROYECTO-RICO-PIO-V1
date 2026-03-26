import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
from theme import Theme
from ui_helpers import UIHelpers
from logic import BusinessLogic
import random

class ListaGruposDialog(tk.Toplevel):
    def __init__(self, parent, on_select):
        super().__init__(parent)
        self.title("Lista de Grupos")
        self.geometry("500x400")
        self.configure(bg=Theme.SURFACE)
        self.transient(parent)
        self.grab_set()
        self.on_select = on_select
        
        UIHelpers.create_header(self, "Lista de Grupos")
        
        table_frame = tk.Frame(self, bg=Theme.SURFACE, padx=10, pady=10)
        table_frame.pack(fill="both", expand=True)
        
        columns = ("Nombre de Grupo", "Código")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.tree.heading("Nombre de Grupo", text="Nombre de Grupo")
        self.tree.column("Nombre de Grupo", width=300)
        self.tree.heading("Código", text="Código")
        self.tree.column("Código", width=100, anchor="center")
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.grupos = BusinessLogic.get_grupos()
        for g in self.grupos:
            self.tree.insert("", "end", values=(g.get("nombre", ""), g.get("codigo", "")))
            
        self.tree.bind("<Double-1>", self.on_double_click)
        
        btn_bar = tk.Frame(self, bg=Theme.FOOTER_BG, pady=10)
        btn_bar.pack(fill="x", side="bottom")
        tk.Button(btn_bar, text="Salir", bg=Theme.DANGER, fg="white", font=Theme.FONT_BOLD, relief="flat", command=self.destroy).pack(side="right", padx=10)

    def on_double_click(self, event):
        item = self.tree.selection()
        if item:
            val = self.tree.item(item[0], "values")
            self.on_select({"nombre": val[0], "codigo": val[1]})
            self.destroy()

class GruposInventarioDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Grupos de inventario")
        self.geometry("850x650")
        self.configure(bg=Theme.SURFACE)
        self.resizable(True, True)
        self.transient(parent)
        self.grab_set()
        
        self.color_seleccionado = "#CCCCCC" # Color por defecto
        
        self._build_ui()

    def _build_ui(self):
        UIHelpers.create_header(self, "Gestión de Grupos de Inventario")
        
        # Contenedor con Scroll (opcional, por ahora flexible)
        container = tk.Frame(self, bg=Theme.SURFACE, padx=25, pady=20)
        container.pack(fill="both", expand=True)

        # Dividir en Izquierda (Datos) y Derecha (Utilidad/Imagen)
        left = tk.Frame(container, bg=Theme.SURFACE)
        left.pack(side="left", fill="both", expand=True, padx=(0, 20))

        # Sección de Identificación
        id_f = tk.LabelFrame(left, text=" Identificación ", font=Theme.FONT_BOLD, bg=Theme.SURFACE, padx=15, pady=10)
        id_f.pack(fill="x", pady=(0, 15))
        
        self.e_codigo = self._field(id_f, "Código del Grupo:", width=10, row=0, with_search=True)
        self.e_nombre = self._field(id_f, "Nombre Completo:", width=40, row=1)
        self.e_corto = self._field(id_f, "Nombre Corto:", width=20, row=2)

        # Sección Contable
        cc_f = tk.LabelFrame(left, text=" Configuración Contable ", font=Theme.FONT_BOLD, bg=Theme.SURFACE, padx=15, pady=10)
        cc_f.pack(fill="x")
        
        ctas = ["Cta. Inventario", "Cta. Costos", "Cta. Ingresos", "Cta. Devoluciones"]
        for i, cta in enumerate(ctas):
            row = tk.Frame(cc_f, bg=Theme.SURFACE)
            row.pack(fill="x", pady=2)
            tk.Label(row, text=f"{cta}:", font=Theme.FONT_SMALL, bg=Theme.SURFACE, width=15, anchor="w").pack(side="left")
            e = tk.Entry(row, relief="flat", highlightthickness=1, highlightbackground=Theme.BORDER, bg=Theme.ENTRY_HIGHLIGHT)
            e.pack(side="left", fill="x", expand=True, padx=5, ipady=2)
            tk.Button(row, text="...", font=Theme.FONT_SMALL, bg=Theme.BORDER, relief="flat").pack(side="left")

        # Derecha (Imagen y Utilidad)
        right = tk.Frame(container, bg=Theme.SURFACE, width=220)
        right.pack(side="right", fill="y")

        # Imagen
        tk.Label(right, text="Imagen del Grupo", font=Theme.FONT_BOLD, bg=Theme.SURFACE).pack(pady=(0, 5))
        img_box = tk.Frame(right, width=180, height=140, bg=Theme.APP_BG, highlightthickness=1, highlightbackground=Theme.BORDER)
        img_box.pack()
        img_box.pack_propagate(False)
        tk.Label(img_box, text="📸\nSin Imagen", font=Theme.FONT_SMALL, bg=Theme.APP_BG, fg=Theme.TEXT_SECONDARY).place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Button(right, text="Subir Imagen", font=Theme.FONT_SMALL, bg="white", relief="flat", padx=10).pack(pady=10)
        
        # Color del Grupo
        tk.Label(right, text="Color del Grupo", font=Theme.FONT_BOLD, bg=Theme.SURFACE).pack(pady=(10, 5))
        self.color_preview = tk.Frame(right, width=50, height=30, bg=self.color_seleccionado, highlightthickness=1, highlightbackground=Theme.BORDER)
        self.color_preview.pack(pady=5)
        
        tk.Button(right, text="Cambiar Color", font=Theme.FONT_SMALL, bg="white", relief="flat", padx=10, command=self.escoger_color).pack(pady=5)

        # Checks
        tk.Checkbutton(left, text="Mostrar en Punto de Venta (Touch)", bg=Theme.SURFACE, font=Theme.FONT_SMALL).pack(anchor="w", pady=5)
        tk.Checkbutton(left, text="Grupo especial para Licores (Impuestos)", bg=Theme.SURFACE, font=Theme.FONT_SMALL).pack(anchor="w")

        # Botonera Inferior
        btn_bar = tk.Frame(self, bg=Theme.FOOTER_BG, pady=15, padx=25)
        btn_bar.pack(fill="x", side="bottom")
        
        btn_exit = tk.Button(btn_bar, text="Salir", font=Theme.FONT_BOLD, bg=Theme.DANGER, fg="white", 
                             relief="flat", command=self.destroy)
        btn_exit.pack(side="right", padx=5)
        
        btn_borrar = tk.Button(btn_bar, text="🗑 Borrar", font=Theme.FONT_BOLD, bg="#6c757d", fg="white", 
                             relief="flat", command=self.borrar_grupo)
        btn_borrar.pack(side="right", padx=5)

        UIHelpers.btn_primary(btn_bar, "🖫 Guardar Grupo", command=self.guardar_grupo).pack(side="right", padx=5)

    def _field(self, parent, label, width, row, with_search=False):
        r = tk.Frame(parent, bg=Theme.SURFACE)
        r.pack(fill="x", pady=4)
        tk.Label(r, text=label, font=Theme.FONT_SMALL, bg=Theme.SURFACE, width=18, anchor="w").pack(side="left")
        e = tk.Entry(r, width=width, relief="flat", highlightthickness=1, highlightbackground=Theme.BORDER)
        e.pack(side="left", padx=5, ipady=3)
        if with_search:
            tk.Button(r, text="Buscar", font=Theme.FONT_SMALL, command=self.abrir_busqueda).pack(side="left", padx=5)
        return e

    def abrir_busqueda(self):
        ListaGruposDialog(self, self.on_grupo_seleccionado)
        
    def on_grupo_seleccionado(self, grupo):
        self.e_codigo.delete(0, 'end')
        self.e_codigo.insert(0, grupo["codigo"])
        self.e_nombre.delete(0, 'end')
        self.e_nombre.insert(0, grupo["nombre"])
        
        # Buscar color del grupo seleccionado
        grupos = BusinessLogic.get_grupos()
        for g in grupos:
            if g["codigo"] == grupo["codigo"]:
                self.color_seleccionado = g.get("color", "#CCCCCC")
                self.color_preview.configure(bg=self.color_seleccionado)
                break

    def escoger_color(self):
        color = colorchooser.askcolor(initialcolor=self.color_seleccionado, title="Seleccione un color para el grupo")
        if color[1]:
            self.color_seleccionado = color[1]
            self.color_preview.configure(bg=self.color_seleccionado)
        
    def guardar_grupo(self):
        codigo = self.e_codigo.get().strip()
        nombre = self.e_nombre.get().strip()
        
        if not codigo or not nombre:
            messagebox.showerror("Error", "Código y Nombre son obligatorios")
            return
            
        grupos = BusinessLogic.get_grupos()
        found = False
        for g in grupos:
            if g["codigo"] == codigo:
                g["nombre"] = nombre
                g["color"] = self.color_seleccionado # Actualizar color
                found = True
                break
                
        if not found:
            grupos.append({"codigo": codigo, "nombre": nombre, "color": self.color_seleccionado})
            
        if BusinessLogic.set_grupos(grupos):
            messagebox.showinfo("Éxito", "Grupo guardado correctamente")
        else:
            messagebox.showerror("Error", "No se pudo guardar")

    def borrar_grupo(self):
        codigo = self.e_codigo.get().strip()
        if not codigo: return
        
        if messagebox.askyesno("Confirmar", f"¿Desea borrar el grupo {codigo}?"):
            grupos = BusinessLogic.get_grupos()
            # Delete if exists
            new_grupos = [g for g in grupos if g["codigo"] != codigo]
            if len(new_grupos) == len(grupos):
                messagebox.showerror("Error", "No se encontró el grupo")
                return
                
            if BusinessLogic.set_grupos(new_grupos):
                messagebox.showinfo("Éxito", "Grupo borrado")
                self.e_codigo.delete(0, 'end')
                self.e_nombre.delete(0, 'end')
            else:
                messagebox.showerror("Error", "No se pudo borrar")
