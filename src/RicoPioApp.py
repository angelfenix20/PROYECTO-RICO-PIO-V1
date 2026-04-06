"""
Proyecto: Sistema de Facturación "Rico Pío"
Asesoría: Ing. Gabriela
Refactorización: Estructura Modular y Separación de Lógica
"""

import tkinter as tk
from theme import Theme
from ui_helpers import _fix_tcl_tk, UIHelpers

# Importar Paneles
from panels.login import LoginPanel
from panels.admin import AdminPanel
from panels.cashier import CashierPanel
from panels.punto_venta import PuntoVentaPanel

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
            
        # Extraer ancho y alto de la geometría (formato "anchoxalto")
        width, height = map(int, geometry.split("x"))
        UIHelpers.center_window(self.root, width, height)

        new_frame = frame_class(self.container, self, **kwargs)
        self.current_frame = new_frame
        new_frame.pack(fill="both", expand=True)

    def mostrar_login(self):
        self._switch_frame(LoginPanel, geometry="500x550")

    def mostrar_panel_admin(self):
        self._switch_frame(AdminPanel, geometry="950x650")

    def mostrar_panel_cajero(self):
        self.mostrar_punto_venta()

    def mostrar_punto_venta(self):
        # En la nueva UI central, Punto Venta es un Modal sobre la vista de mesas. 
        # Cargar la vista de Mesas por defecto
        from panels.mesas_view import MesasView
        self._switch_frame(MesasView, geometry="1024x720")


if __name__ == "__main__":
    root = tk.Tk()
    app = RicoPioApp(root)
    root.mainloop()
