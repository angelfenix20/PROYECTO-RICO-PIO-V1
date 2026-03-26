"""
Proyecto: Sistema de Facturación "Rico Pío"
Asesoría: Ing. Gabriela
Refactorización: Estructura Modular y Separación de Lógica
"""

import tkinter as tk
from theme import Theme
from ui_helpers import _fix_tcl_tk

# Importar Paneles
from panels.login import LoginPanel
from panels.admin import AdminPanel
from panels.cashier import CashierPanel

# Aplicar parche de Tcl/Tk si es necesario
_fix_tcl_tk()

class RicoPioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Facturación Rico Pío - v0.1 Modular")
        self.root.configure(bg=Theme.BG_DEFAULT)
        self.root.resizable(True, True)

        self.container = tk.Frame(self.root, bg=Theme.BG_DEFAULT)
        self.container.pack(fill="both", expand=True)

        self.current_frame: tk.Frame | None = None
        self.mostrar_login()

    def _switch_frame(self, frame_class, geometry="500x550", **kwargs):
        """Destruye el panel actual y carga uno nuevo."""
        frame = self.current_frame
        if frame is not None:
            frame.destroy()
            self.current_frame = None
            
        self.root.geometry(geometry)
        new_frame = frame_class(self.container, self, **kwargs)
        self.current_frame = new_frame
        new_frame.pack(fill="both", expand=True)

    def mostrar_login(self):
        self._switch_frame(LoginPanel, geometry="500x550")

    def mostrar_panel_admin(self):
        self._switch_frame(AdminPanel, geometry="950x650")

    def mostrar_panel_cajero(self):
        self._switch_frame(CashierPanel, geometry="800x600")


if __name__ == "__main__":
    root = tk.Tk()
    app = RicoPioApp(root)
    root.mainloop()
