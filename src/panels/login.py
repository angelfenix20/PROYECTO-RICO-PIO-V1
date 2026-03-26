import tkinter as tk
from tkinter import ttk, messagebox
from typing import Any
from theme import Theme
from ui_helpers import UIHelpers
from logic import AuthService

class LoginPanel(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=Theme.APP_BG)
        self.controller = controller
        
        # Inicialización de widgets
        self.empresa_cb: Any = None
        self.sucursal_cb: Any = None
        self.user_cb: Any = None
        self.pass_entry: Any = None
        
        self._build_ui()

    def _build_ui(self):
        # Contenedor Central (Card)
        card = tk.Frame(self, bg=Theme.SURFACE, bd=0, highlightthickness=1, highlightbackground=Theme.BORDER)
        card.place(relx=0.5, rely=0.5, anchor="center", width=420, height=520)

        # Header del Card
        header = tk.Frame(card, bg=Theme.PRIMARY, height=100)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="RICO PÍO", fg="white", bg=Theme.PRIMARY, font=("Segoe UI", 24, "bold")).pack(pady=(20, 0))
        tk.Label(header, text="Sistema de Gestión Gastronómica", fg="white", bg=Theme.PRIMARY, font=Theme.FONT_SMALL).pack()

        # Cuerpo del Formulario
        body = tk.Frame(card, bg=Theme.SURFACE, padx=40, pady=30)
        body.pack(fill="both", expand=True)

        tk.Label(body, text="Bienvenido", font=("Segoe UI", 18, "bold"), bg=Theme.SURFACE, fg=Theme.TEXT_PRIMARY).pack(anchor="w", pady=(0, 20))

        # Campos
        self._create_field(body, "Empresa", ["RICO PIO 2000 C.A"], is_combo=True)
        self._create_field(body, "Sucursal", ["OFICINA PRINCIPAL"], is_combo=True)
        
        # Fila de Usuario y Clave
        cred_frame = tk.Frame(body, bg=Theme.SURFACE)
        cred_frame.pack(fill="x", pady=10)

        u_frame = tk.Frame(cred_frame, bg=Theme.SURFACE)
        u_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        tk.Label(u_frame, text="Usuario", bg=Theme.SURFACE, font=Theme.FONT_SMALL, fg=Theme.TEXT_SECONDARY).pack(anchor="w")
        self.user_cb = ttk.Combobox(u_frame, values=["gaby01", "caja01"], font=Theme.FONT_BODY)
        self.user_cb.pack(fill="x", pady=5)
        self.user_cb.current(0)

        p_frame = tk.Frame(cred_frame, bg=Theme.SURFACE)
        p_frame.pack(side="left", fill="x", expand=True)
        tk.Label(p_frame, text="Contraseña", bg=Theme.SURFACE, font=Theme.FONT_SMALL, fg=Theme.TEXT_SECONDARY).pack(anchor="w")
        self.pass_entry = tk.Entry(p_frame, show="*", font=Theme.FONT_BODY, relief="flat", highlightthickness=1, highlightbackground=Theme.BORDER)
        self.pass_entry.pack(fill="x", pady=5, ipady=3)

        # Botón de Login
        btn_login = UIHelpers.btn_primary(body, "Entrar al Sistema", command=self.validar_login)
        btn_login.pack(fill="x", pady=(30, 0))

        # Footer
        footer = tk.Frame(self, bg=Theme.APP_BG)
        footer.pack(side="bottom", fill="x", pady=20)
        tk.Label(footer, text="Versión 9.1 Modular | Centauro Profesional", fg=Theme.TEXT_SECONDARY, bg=Theme.APP_BG, font=Theme.FONT_SMALL).pack()

    def _create_field(self, parent, label, values=None, is_combo=False):
        frame = tk.Frame(parent, bg=Theme.SURFACE)
        frame.pack(fill="x", pady=8)
        
        tk.Label(frame, text=label, bg=Theme.SURFACE, font=Theme.FONT_SMALL, fg=Theme.TEXT_SECONDARY).pack(anchor="w")
        if is_combo:
            cb = ttk.Combobox(frame, values=values, font=Theme.FONT_BODY)
            cb.pack(fill="x", pady=5)
            cb.current(0)
            return cb
        else:
            e = tk.Entry(frame, font=Theme.FONT_BODY, relief="flat", highlightthickness=1, highlightbackground=Theme.BORDER)
            e.pack(fill="x", pady=5, ipady=3)
            return e

    def validar_login(self):
        usuario = self.user_cb.get()
        clave = self.pass_entry.get()

        user_data = AuthService.validar_login(usuario, clave)

        if user_data:
            rol = user_data["rol"]
            messagebox.showinfo("Éxito", f"Bienvenido, {usuario}")
            if rol == "administrador":
                self.controller.mostrar_panel_admin()
            else:
                self.controller.mostrar_panel_cajero()
        else:
            messagebox.showwarning("Atención", "Usuario o clave incorrecta")
