import tkinter as tk
from theme import Theme
from ui_helpers import UIHelpers

class TasaCambioDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Tasa de cambio")
        self.geometry("480x350")
        self.configure(bg=Theme.BG_WHITE)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self._build_ui()
    
    def _build_ui(self):
        UIHelpers.create_header(self, "Tasa de cambio", height=40)
        
        body = tk.Frame(self, bg=Theme.BG_WHITE)
        body.pack(fill="both", expand=True, padx=20, pady=10)
        
        left_frame = tk.Frame(body, bg=Theme.BG_WHITE)
        left_frame.pack(side="left", fill="y", padx=(10, 20))
        tk.Label(left_frame, text="$", font=("Arial", 36, "bold"), fg="#2c3e50", bg=Theme.BG_WHITE).pack(pady=20)
        
        right_frame = tk.Frame(body, bg=Theme.BG_WHITE)
        right_frame.pack(side="left", fill="both", expand=True)
        tk.Label(right_frame, text="Tasa de cambio actual", font=("Arial", 11, "bold"), bg=Theme.BG_WHITE, fg="#333333").pack(anchor="e")
        
        vcmd = (self.register(self.solo_numeros), '%P')

        entry_frame = tk.Frame(right_frame, bg=Theme.BG_WHITE, bd=1, relief="ridge")
        entry_frame.pack(anchor="e", pady=(2, 10))
        tk.Label(entry_frame, text="🔍", bg=Theme.BG_WHITE, font=("Arial", 10)).pack(side="left", padx=2)
        tk.Label(entry_frame, text="Bs ", bg=Theme.BG_WHITE, font=("Arial", 12)).pack(side="left", padx=2)
        
        entry_tasa = tk.Entry(entry_frame, font=("Arial", 12), width=14, justify="right", bd=0, validate="key", validatecommand=vcmd)
        entry_tasa.pack(side="left", padx=2, pady=2)
        entry_tasa.insert(0, "500")
        
        tk.Frame(right_frame, bg="#bdc3c7", height=1).pack(fill="x", pady=5)
        
        tk.Label(right_frame, text="Moneda extranjera", font=Theme.FONT_NORMAL, fg=Theme.ACCENT_BLUE, bg=Theme.BG_WHITE).pack()
        tk.Label(right_frame, text="DOLAR", font=("Arial", 11, "bold"), fg="#333333", bg=Theme.BG_WHITE).pack()
        
        tk.Label(right_frame, text="Símbolo", font=Theme.FONT_NORMAL, fg=Theme.ACCENT_BLUE, bg=Theme.BG_WHITE).pack(pady=(5, 0))
        tk.Label(right_frame, text="$", font=("Arial", 12, "bold"), fg="#333333", bg=Theme.BG_WHITE).pack()
        
        info_text = "Este proceso se aplicará sobre los artículos importados y sobre los nacionales que posee factor de cambio"
        tk.Label(body, text=info_text, bg=Theme.BG_WHITE, fg="#555555", font=Theme.FONT_NORMAL, justify="center").pack(side="bottom", pady=10)
        
        btn_wrapper = tk.Frame(self, bg=Theme.BG_WHITE)
        btn_wrapper.pack(side="bottom", fill="x", pady=(0, 15))
        
        btn_frame = tk.Frame(btn_wrapper, bg=Theme.BG_WHITE)
        btn_frame.pack(side="right", padx=15)
        
        tk.Button(btn_frame, text="✓ Procesar", font=Theme.FONT_BOLD, bg="#f5f5f5", fg="#7f8c8d", bd=1, relief="solid").pack(side="left", padx=5)
        tk.Button(btn_frame, text="⮐ Salir", font=Theme.FONT_BOLD, bg=Theme.ACCENT_RED, fg="white", bd=0, command=self.destroy, padx=10, pady=2).pack(side="left", padx=5)

    def solo_numeros(self, nuevo_texto):
        return nuevo_texto == "" or nuevo_texto.isdigit()
