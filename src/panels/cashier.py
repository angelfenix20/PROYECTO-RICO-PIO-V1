import tkinter as tk
from theme import Theme

class CashierPanel(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=Theme.BG_DEFAULT)
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        main_label = tk.Label(self, text="PANEL DE CAJA Y FACTURACIÓN", font=("Arial", 20, "bold"), bg=Theme.BG_DEFAULT, fg=Theme.ACCENT_BLUE)
        main_label.pack(pady=50)

        info = tk.Label(self, text="Opciones de Caja:\n- Facturación de mesas y comandas\n- Cierre de turno", font=("Arial", 12), bg=Theme.BG_DEFAULT)
        info.pack(pady=20)

        tk.Button(self, text="Cerrar Sesión", command=self.controller.mostrar_login, bg="white").pack(side="bottom", pady=20)
