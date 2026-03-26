import tkinter as tk
from theme import Theme
from ui_helpers import UIHelpers
from logic import BusinessLogic
from tkinter import messagebox

class TasaCambioDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Tasa de cambio")
        self.geometry("480x400")
        self.configure(bg=Theme.SURFACE)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        # Cargar tasa actual
        self.tasa_actual = BusinessLogic.get_tasa_usd()
        
        self._build_ui()
    
    def _build_ui(self):
        UIHelpers.create_header(self, "Tasa de cambio")
        
        body = tk.Frame(self, bg=Theme.SURFACE, padx=30, pady=25)
        body.pack(fill="both", expand=True)
        
        # Icono y Título
        top_f = tk.Frame(body, bg=Theme.SURFACE)
        top_f.pack(fill="x", pady=(0, 20))
        tk.Label(top_f, text="USD", font=("Segoe UI", 32, "bold"), fg=Theme.PRIMARY, bg=Theme.SURFACE).pack(side="left")
        
        info_f = tk.Frame(top_f, bg=Theme.SURFACE)
        info_f.pack(side="right")
        tk.Label(info_f, text="Tasa de cambio actual", font=Theme.FONT_SMALL, fg=Theme.TEXT_SECONDARY, bg=Theme.SURFACE).pack(anchor="e")
        
        vcmd = (self.register(self.solo_numeros), '%P')
        self.entry_tasa = tk.Entry(info_f, font=("Segoe UI", 16, "bold"), width=10, justify="right", 
                                relief="flat", highlightthickness=1, highlightbackground=Theme.BORDER, 
                                highlightcolor=Theme.PRIMARY, validate="key", validatecommand=vcmd)
        self.entry_tasa.pack(pady=5, ipady=3)
        self.entry_tasa.insert(0, f"{self.tasa_actual:.2f}")

        tk.Frame(body, bg=Theme.BORDER, height=1).pack(fill="x", pady=20)
        
        # Detalles de Moneda
        details = tk.Frame(body, bg=Theme.SURFACE)
        details.pack(fill="x")
        
        for lbl, val in [("Moneda extranjera:", "DÓLAR ESTADOUNIDENSE"), ("Símbolo:", "$")]:
            row = tk.Frame(details, bg=Theme.SURFACE)
            row.pack(fill="x", pady=5)
            tk.Label(row, text=lbl, font=Theme.FONT_SMALL, fg=Theme.TEXT_SECONDARY, bg=Theme.SURFACE).pack(side="left")
            tk.Label(row, text=val, font=Theme.FONT_BOLD, fg=Theme.TEXT_PRIMARY, bg=Theme.SURFACE).pack(side="right")
        
        desc = "Este proceso actualizará los precios según el factor de cambio configurado."
        tk.Label(body, text=desc, font=Theme.FONT_SMALL, fg=Theme.TEXT_SECONDARY, bg=Theme.SURFACE, wraplength=400, justify="center").pack(side="bottom", pady=20)
        
        # Botonera
        btn_f = tk.Frame(self, bg=Theme.APP_BG, pady=15, padx=30)
        btn_f.pack(fill="x", side="bottom")
        
        UIHelpers.btn_primary(btn_f, "✓ Procesar Tasa", command=self.save_tasa).pack(side="right", padx=5)
        
        btn_exit = tk.Button(btn_f, text="Cancelar", font=Theme.FONT_BOLD, bg="white", fg=Theme.TEXT_SECONDARY, 
                             relief="flat", bd=0, command=self.destroy, cursor="hand2")
        btn_exit.pack(side="right", padx=5)
        UIHelpers.apply_hover(btn_exit, "white", Theme.BORDER)

    def save_tasa(self):
        nueva_tasa = self.entry_tasa.get()
        try:
            if BusinessLogic.set_tasa_usd(nueva_tasa):
                messagebox.showinfo("Éxito", f"Tasa de cambio actualizada a {nueva_tasa}")
                self.destroy()
            else:
                messagebox.showerror("Error", "No se pudo guardar la tasa de cambio")
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese un valor numérico válido")

    def solo_numeros(self, nuevo_texto):
        return nuevo_texto == "" or nuevo_texto.replace(".", "", 1).isdigit()
