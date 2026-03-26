import tkinter as tk
from tkinter import ttk
from theme import Theme
from ui_helpers import UIHelpers

class GruposInventarioDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Grupos de inventario")
        self.geometry("850x650")
        self.configure(bg=Theme.SURFACE)
        self.resizable(True, True)
        self.transient(parent)
        self.grab_set()
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
        
        self._field(id_f, "Código del Grupo:", width=10, row=0)
        self._field(id_f, "Nombre Completo:", width=40, row=1)
        self._field(id_f, "Nombre Corto:", width=20, row=2)

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

        # Checks
        tk.Checkbutton(left, text="Mostrar en Punto de Venta (Touch)", bg=Theme.SURFACE, font=Theme.FONT_SMALL).pack(anchor="w", pady=5)
        tk.Checkbutton(left, text="Grupo especial para Licores (Impuestos)", bg=Theme.SURFACE, font=Theme.FONT_SMALL).pack(anchor="w")

        # Botonera Inferior
        btn_bar = tk.Frame(self, bg=Theme.FOOTER_BG, pady=15, padx=25)
        btn_bar.pack(fill="x", side="bottom")
        
        UIHelpers.btn_primary(btn_bar, "🖫 Guardar Grupo").pack(side="right", padx=5)
        
        btn_exit = tk.Button(btn_bar, text="Cancelar", font=Theme.FONT_BOLD, bg="white", fg=Theme.TEXT_SECONDARY, 
                             relief="flat", command=self.destroy)
        btn_exit.pack(side="right", padx=5)
        UIHelpers.apply_hover(btn_exit, "white", Theme.BORDER)

    def _field(self, parent, label, width, row):
        r = tk.Frame(parent, bg=Theme.SURFACE)
        r.pack(fill="x", pady=4)
        tk.Label(r, text=label, font=Theme.FONT_SMALL, bg=Theme.SURFACE, width=18, anchor="w").pack(side="left")
        e = tk.Entry(r, width=width, relief="flat", highlightthickness=1, highlightbackground=Theme.BORDER)
        e.pack(side="left", padx=5, ipady=3)
        return e
