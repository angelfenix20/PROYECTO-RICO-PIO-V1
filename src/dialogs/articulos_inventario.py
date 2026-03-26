import tkinter as tk
from tkinter import ttk
from theme import Theme
from ui_helpers import UIHelpers

class ArticulosInventarioDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Artículos de inventario y servicios")
        self.geometry("900x640")
        self.configure(bg=Theme.BG_WHITE)
        self.resizable(True, True)
        self.transient(parent)
        self.grab_set()
        self._build_ui()

    def _build_ui(self):
        UIHelpers.create_header(self, "Artículos de inventario y servicios")
        UIHelpers.create_status_bar(self, "Indique el CODIGO DEL ARTICULO", "Ant:TAR   NUEVO")

        btn_bar = tk.Frame(self, bg=Theme.BG_DEFAULT, pady=6)
        btn_bar.pack(fill="x", side="bottom")
        tk.Button(btn_bar, text="Campos Adic.", font=Theme.FONT_NORMAL, relief="solid", bd=1, padx=8, pady=3).pack(side="left", padx=8)
        tk.Button(btn_bar, text="Histórico", font=Theme.FONT_NORMAL, relief="solid", bd=1, padx=8, pady=3).pack(side="left", padx=2)
        tk.Button(btn_bar, text="🖫  Grabar", bg=Theme.BUTTON_GRAY, fg="white", font=Theme.FONT_BOLD, padx=8, pady=3).pack(side="right", padx=3)
        tk.Button(btn_bar, text="🗑  Borrar", bg=Theme.BUTTON_GRAY, fg="white", font=Theme.FONT_BOLD, padx=8, pady=3).pack(side="right", padx=3)
        tk.Button(btn_bar, text="📈  Estad.", bg=Theme.BUTTON_GRAY, fg="white", font=Theme.FONT_BOLD, padx=8, pady=3).pack(side="right", padx=3)
        tk.Button(btn_bar, text="⮐  Salir", bg=Theme.ACCENT_RED, fg="white", font=Theme.FONT_BOLD, padx=8, pady=3, command=self.destroy).pack(side="right", padx=3)

        body = tk.Frame(self, bg=Theme.BG_WHITE)
        body.pack(fill="both", expand=True, padx=8, pady=4)

        r_cod = tk.Frame(body, bg=Theme.BG_WHITE)
        r_cod.pack(fill="x", pady=2)
        tk.Label(r_cod, text="Código", bg=Theme.BG_WHITE, font=Theme.FONT_BOLD).pack(side="left")
        tk.Entry(r_cod, width=30, relief="solid", bd=1).pack(side="left", padx=4)
        tk.Button(r_cod, text="Buscar", font=Theme.FONT_SMALL, relief="solid", bd=1, padx=6).pack(side="left")
        tk.Button(r_cod, text="Importar", font=Theme.FONT_SMALL, relief="solid", bd=1, padx=6).pack(side="left", padx=6)

        r_grp = tk.Frame(body, bg=Theme.BG_WHITE)
        r_grp.pack(fill="x", pady=2)
        tk.Label(r_grp, text="Grupo:", bg=Theme.BG_WHITE, font=Theme.FONT_NORMAL).pack(side="left")
        tk.Entry(r_grp, width=6, relief="solid", bd=1).pack(side="left", padx=2)
        tk.Button(r_grp, text="Buscar", font=Theme.FONT_SMALL, relief="solid", bd=1, padx=4).pack(side="left", padx=2)
        tk.Entry(r_grp, width=16, bg=Theme.ENTRY_HIGHLIGHT, relief="solid", bd=1).pack(side="left", padx=4)
        tk.Button(r_grp, text="📋", font=Theme.FONT_NORMAL, relief="solid", bd=1).pack(side="left", padx=2)
        tk.Label(r_grp, text="Sub. Grupo:", bg=Theme.BG_WHITE, font=Theme.FONT_NORMAL).pack(side="left", padx=(10,2))
        tk.Entry(r_grp, width=6, relief="solid", bd=1).pack(side="left", padx=2)
        tk.Button(r_grp, text="Buscar", font=Theme.FONT_SMALL, relief="solid", bd=1, padx=4).pack(side="left", padx=2)
        tk.Entry(r_grp, width=16, bg=Theme.ENTRY_HIGHLIGHT, relief="solid", bd=1).pack(side="left", padx=4)

        r_nom = tk.Frame(body, bg=Theme.BG_WHITE)
        r_nom.pack(fill="x", pady=2)
        tk.Label(r_nom, text="Nombre o descripción del artículo", bg=Theme.BG_WHITE, font=Theme.FONT_NORMAL).pack(anchor="w")
        tk.Entry(r_nom, relief="solid", bd=1).pack(fill="x", pady=2)

        top_nb = ttk.Notebook(body)
        top_nb.pack(fill="x", pady=2)
        for tab_name in ["F8-Componentes", "F9-Cód. Alternativos", "F10-Proveedores", "F11-Cod.Contables", "Escalas"]:
            top_nb.add(tk.Frame(top_nb, bg=Theme.BG_WHITE, height=1), text=tab_name)

        main_nb = ttk.Notebook(body)
        main_nb.pack(fill="both", expand=True, pady=2)

        f2 = tk.Frame(main_nb, bg=Theme.BG_WHITE)
        main_nb.add(f2, text="F2-Datos generales")
        for tn in ["F3-Descripción", "F4-Existencias y Equivalentes", "F5-Precios Nacionales", "F7-Precios del grupo", "F6-Precios Importados"]:
            main_nb.add(tk.Frame(main_nb, bg=Theme.BG_WHITE), text=tn)

        self._build_f2_tab(f2)

    def _build_f2_tab(self, f2):
        f2_left = tk.Frame(f2, bg=Theme.BG_WHITE, width=170)
        f2_left.pack(side="left", fill="y", padx=6, pady=6)
        f2_left.pack_propagate(False)

        tk.Label(f2_left, text="Foto del Artículo", bg=Theme.BG_WHITE, font=Theme.FONT_BOLD).pack()
        img_f = tk.Frame(f2_left, width=140, height=100, bg="#f0f0f0", relief="sunken", bd=1)
        img_f.pack(pady=4)
        img_f.pack_propagate(False)
        tk.Label(img_f, text="SIN IMAGEN", bg="#f0f0f0", fg="#aaaaaa", font=Theme.FONT_NORMAL).place(relx=0.5, rely=0.5, anchor="center")
        tk.Button(f2_left, text="Buscar Imagen", font=Theme.FONT_SMALL, relief="solid", bd=1, padx=4).pack(pady=4)

        orig_var = tk.StringVar(value="Nacional")
        orig_r = tk.Frame(f2_left, bg=Theme.BG_WHITE)
        orig_r.pack(anchor="w")
        tk.Label(orig_r, text="Origen:", bg=Theme.BG_WHITE, font=Theme.FONT_NORMAL).pack(side="left")
        for v in ["Nacional", "Importado"]:
            tk.Radiobutton(orig_r, text=v, variable=orig_var, value=v, bg=Theme.BG_WHITE, font=Theme.FONT_NORMAL).pack(side="left")

        mant_var = tk.StringVar(value="Utilidad")
        mant_r = tk.Frame(f2_left, bg=Theme.BG_WHITE)
        mant_r.pack(anchor="w")
        tk.Label(mant_r, text="Mantener:", bg=Theme.BG_WHITE, font=Theme.FONT_NORMAL).pack(side="left")
        for v in ["Utilidad", "Precios"]:
            tk.Radiobutton(mant_r, text=v, variable=mant_var, value=v, bg=Theme.BG_WHITE, font=Theme.FONT_NORMAL).pack(side="left")

        tk.Label(f2_left, text="Nombre Corto p/ Touch Screen", bg=Theme.BG_WHITE, font=Theme.FONT_SMALL).pack(anchor="w", pady=(6,0))
        tk.Entry(f2_left, width=22, relief="solid", bd=1).pack(anchor="w")
        tk.Checkbutton(f2_left, text="Es un Medicamento", bg=Theme.BG_WHITE, font=Theme.FONT_NORMAL).pack(anchor="w", pady=2)
        tk.Checkbutton(f2_left, text="Aplica Descto. Medicament.", bg=Theme.BG_WHITE, font=Theme.FONT_NORMAL).pack(anchor="w")

        f2_mid = tk.Frame(f2, bg=Theme.BG_WHITE, width=180)
        f2_mid.pack(side="left", fill="y", padx=4, pady=6)
        f2_mid.pack_propagate(False)

        self._radio_yesno(f2_mid, "Usa Existencia")
        self._radio_yesno(f2_mid, "Es Integrado")
        tk.Checkbutton(f2_mid, text="Es dinámico?", bg=Theme.BG_WHITE, font=Theme.FONT_NORMAL).pack(anchor="w", padx=8)
        self._radio_yesno(f2_mid, "Es agrupado")
        self._radio_yesno(f2_mid, "Fraccionable")
        self._radio_yesno(f2_mid, "Usa seriales")

        f2_imp = tk.Frame(f2, bg=Theme.BG_WHITE, relief="groove", bd=1)
        f2_imp.pack(side="left", fill="y", padx=6, pady=6)

        tk.Label(f2_imp, text="IMPUESTOS", bg=Theme.BG_WHITE, font=Theme.FONT_BOLD).pack(pady=(6,2))
        tk.Checkbutton(f2_imp, text="Utiliza alícuota de percibidos", bg=Theme.BG_WHITE, font=Theme.FONT_NORMAL).pack()

        iva_row = tk.Frame(f2_imp, bg=Theme.BG_WHITE)
        iva_row.pack(pady=4)
        for lbl_text, vals in [("I.V.A. Venta:", ["16.00","8.00","0%"]), ("I.V.A. Compra:", ["16.00","8.00","0%"])]:
            col = tk.Frame(iva_row, bg=Theme.BG_WHITE)
            col.pack(side="left", padx=6)
            tk.Label(col, text=lbl_text, bg=Theme.BG_WHITE, font=Theme.FONT_NORMAL).pack()
            cb = ttk.Combobox(col, values=vals, width=7)
            cb.set(vals[0])
            cb.pack()

        for lbl_text in ["Monto Impuesto Nacional:", "Monto Impuesto Producción:"]:
            tk.Label(f2_imp, text=lbl_text, bg=Theme.BG_WHITE, font=Theme.FONT_NORMAL).pack(pady=(4,0))
            e = tk.Entry(f2_imp, width=16, justify="right", relief="solid", bd=1)
            e.insert(0, "0,00")
            e.pack(pady=2)

        f2_right = tk.Frame(f2, bg=Theme.BG_WHITE)
        f2_right.pack(side="left", fill="both", expand=True, padx=4, pady=6)

        checks_right = [
            "Usa lotes", "Usa controles legales?", "Es pesado en Balanza", "Suspendido para venta", "Suspendido para compra", 
            "Uso interno?", "Es flotante?", "Usa vencimiento?", "NO permite crédito?", "NO permite descuentos?", "Es vehículo", 
            "Usa Talla/Color?", "Se vende por escala?", "Contenido en Bulto?", "Exento de ISLR", "Genera puntos", 
            "Es canjeable por puntos", "No se usa en Web", "Usa Servidor?"
        ]
        for txt in checks_right:
            tk.Checkbutton(f2_right, text=txt, bg=Theme.BG_WHITE, font=Theme.FONT_SMALL).pack(anchor="w", pady=1)

    def _radio_yesno(self, parent, label):
        v = tk.StringVar(value="Si")
        tk.Label(parent, text=label, bg=Theme.BG_WHITE, font=Theme.FONT_NORMAL).pack(anchor="w", pady=(6,0))
        rf = tk.Frame(parent, bg=Theme.BG_WHITE)
        rf.pack(anchor="w")
        tk.Radiobutton(rf, text="Si", variable=v, value="Si", bg=Theme.BG_WHITE).pack(side="left")
        tk.Radiobutton(rf, text="No", variable=v, value="No", bg=Theme.BG_WHITE).pack(side="left")
        return v
