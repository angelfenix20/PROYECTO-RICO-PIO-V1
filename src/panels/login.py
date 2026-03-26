import tkinter as tk
from tkinter import ttk, messagebox
from typing import Any
from theme import Theme
from logic import AuthService

class LoginPanel(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=Theme.BG_DEFAULT)
        self.controller = controller
        
        # Inicialización de widgets
        self.empresa_cb: Any = None
        self.sucursal_cb: Any = None
        self.user_cb: Any = None
        self.pass_entry: Any = None
        self.estacion_entry: Any = None
        
        self._build_ui()

    def _build_ui(self):
        header_frame = tk.Frame(self, bg=Theme.HEADER_BG_DARK, height=80)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, text="Inicio de Sesión", fg=Theme.HEADER_FG_DARK, bg=Theme.HEADER_BG_DARK, font=("Arial", 14, "bold")).place(x=20, y=10)
        tk.Label(header_frame, text="Administrativo 9.1", fg=Theme.ACCENT_BLUE, bg=Theme.HEADER_BG_DARK, font=("Arial", 10)).place(x=20, y=35)
        tk.Label(header_frame, text="Versión en desarrollo", fg="white", bg="orange", font=("Arial", 9, "bold")).place(x=150, y=35)

        logo_frame = tk.Frame(self, bg=Theme.BG_DEFAULT)
        logo_frame.pack(pady=20)
        tk.Label(logo_frame, text="Prototipo", font=("Arial", 25, "bold"), fg="#2c3e50", bg=Theme.BG_DEFAULT).pack(side="left")
        tk.Label(logo_frame, text="SOFTWARE", font=("Arial", 8), fg="#7f8c8d", bg=Theme.BG_DEFAULT).pack(side="bottom")

        form_frame = tk.LabelFrame(self, text=" Entrada al Sistema ", font=("Arial", 10, "bold"), bg="#f5f5f5", padx=20, pady=20)
        form_frame.pack(padx=30, fill="x")

        tk.Label(form_frame, text="Seleccione la empresa a operar", bg="#f5f5f5").pack(anchor="w")
        self.empresa_cb = ttk.Combobox(form_frame, values=["RICO PIO 2000 C.A"], width=50)
        self.empresa_cb.current(0)
        self.empresa_cb.pack(pady=(0, 10))

        tk.Label(form_frame, text="Seleccione la sucursal de la empresa", bg="#f5f5f5").pack(anchor="w")
        self.sucursal_cb = ttk.Combobox(form_frame, values=["OFICINA PRINCIPAL"], width=50)
        self.sucursal_cb.current(0)
        self.sucursal_cb.pack(pady=(0, 10))

        cred_frame = tk.Frame(form_frame, bg="#f5f5f5")
        cred_frame.pack(fill="x")

        user_frame = tk.Frame(cred_frame, bg="#f5f5f5")
        user_frame.pack(side="left", fill="x", expand=True)
        tk.Label(user_frame, text="Seleccione el usuario", bg="#f5f5f5").pack(anchor="w")
        self.user_cb = ttk.Combobox(user_frame, values=["gaby01", "caja01"])
        self.user_cb.pack(fill="x", padx=(0, 10))
        self.user_cb.current(0)

        pass_frame = tk.Frame(cred_frame, bg="#f5f5f5")
        pass_frame.pack(side="left", fill="x", expand=True)
        tk.Label(pass_frame, text="Indique la clave", bg="#f5f5f5").pack(anchor="w")
        self.pass_entry = tk.Entry(pass_frame, show="*")
        self.pass_entry.pack(fill="x")

        tk.Label(form_frame, text="Estación", bg="#f5f5f5").pack(anchor="w", pady=(10, 0))
        self.estacion_entry = tk.Entry(form_frame, width=10)
        self.estacion_entry.insert(0, "001")
        self.estacion_entry.pack(anchor="w")

        btn_frame = tk.Frame(self, bg=Theme.BG_DEFAULT)
        btn_frame.pack(pady=20, padx=30, fill="x")

        tk.Button(btn_frame, text="Login al sistema", bg=Theme.ACCENT_RED, fg="white", font=("Arial", 10, "bold"), command=self.validar_login, height=2).pack(side="left", fill="x", expand=True, padx=(0, 5))
        tk.Button(btn_frame, text="Salir", bg="white", font=("Arial", 10), command=self.controller.root.destroy, height=2).pack(side="left", fill="x", expand=True, padx=(5, 0))

        tk.Label(self, text="Refactorizado con Mentalidad de Ingeniería | Rico Pio App", fg="#7f8c8d", bg=Theme.BG_DEFAULT, font=("Arial", 8, "italic")).pack(side="bottom", pady=10)

    def validar_login(self):
        usuario = self.user_cb.get()
        clave = self.pass_entry.get()

        user_data = AuthService.validar_login(usuario, clave)

        if user_data:
            rol = user_data["rol"]
            messagebox.showinfo("Éxito", f"Bienvenido al sistema, {usuario} ({rol.capitalize()})")
            if rol == "administrador":
                self.controller.mostrar_panel_admin()
            else:
                self.controller.mostrar_panel_cajero()
        else:
            messagebox.showwarning("Atención", "Usuario o clave incorrecta")
