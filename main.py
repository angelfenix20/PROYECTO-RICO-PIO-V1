import sys
import os

# Agregar la carpeta 'src' al path para poder importar RicoPioApp
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

try:
    from RicoPioApp import RicoPioApp
    import tkinter as tk

    if __name__ == "__main__":
        print("Iniciando Sistema de Facturación Rico Pío...")
        root = tk.Tk()
        app = RicoPioApp(root)
        root.mainloop()
except ImportError as e:
    print(f"Error al importar el módulo principal: {e}")
    input("Presione Enter para salir...")
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")
    input("Presione Enter para salir...")
