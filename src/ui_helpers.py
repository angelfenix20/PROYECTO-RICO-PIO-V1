import tkinter as tk
import sys
import os
from theme import Theme

def _fix_tcl_tk():
    try:
        if sys.platform == "win32":
            bases = [
                os.path.dirname(sys.executable),
                os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "Python", "Python314"),
                os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "Python", "Python313"),
                "C:\\Python314"
            ]
            
            for base in bases:
                tcl_dir = os.path.join(base, "tcl", "tcl8.6")
                tk_dir = os.path.join(base, "tcl", "tk8.6")
                if os.path.exists(tcl_dir):
                    os.environ["TCL_LIBRARY"] = tcl_dir
                    if os.path.exists(tk_dir):
                        os.environ["TK_LIBRARY"] = tk_dir
                    return
    except Exception:
        pass

class UIHelpers:
    @staticmethod
    def create_header(parent, title, bg_color=Theme.PRIMARY, height=45):
        header = tk.Frame(parent, bg=bg_color, height=height)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text=title, fg="white", bg=bg_color, font=Theme.FONT_H2).pack(side="left", padx=15, pady=8)
        return header

    @staticmethod
    def lbl(parent, text, row, col, anchor="e", bg=Theme.SURFACE, font=None):
        if font is None: font = Theme.FONT_BODY
        l = tk.Label(parent, text=text, bg=bg, font=font, fg=Theme.TEXT_PRIMARY)
        l.grid(row=row, column=col, sticky=anchor, padx=6, pady=4)
        return l

    @staticmethod
    def entry(parent, row, col, width=22, bg="white"):
        e = tk.Entry(parent, width=width, bg=bg, relief="flat", highlightthickness=1, 
                     highlightbackground=Theme.BORDER, highlightcolor=Theme.PRIMARY)
        e.grid(row=row, column=col, sticky="w", padx=6, pady=4, ipady=3)
        return e

    @staticmethod
    def create_status_bar(parent, text_left, text_right):
        status = tk.Frame(parent, bg=Theme.FOOTER_BG, height=25, bd=0)
        status.pack(fill="x", side="bottom")
        status.pack_propagate(False)
        tk.Label(status, text=text_left, bg=Theme.FOOTER_BG, font=Theme.FONT_SMALL, fg=Theme.TEXT_SECONDARY).pack(side="left", padx=10)
        tk.Label(status, text=text_right, bg=Theme.FOOTER_BG, font=Theme.FONT_SMALL, fg=Theme.TEXT_SECONDARY).pack(side="right", padx=10)
        return status

    @staticmethod
    def apply_hover(button, normal_bg, hover_bg):
        """Aplica un efecto visual cuando el mouse pasa sobre el botón."""
        button.bind("<Enter>", lambda e: button.configure(bg=hover_bg))
        button.bind("<Leave>", lambda e: button.configure(bg=normal_bg))

    @staticmethod
    def btn_primary(parent, text, command=None, width=None):
        btn = tk.Button(parent, text=text, bg=Theme.PRIMARY, fg="white", 
                        font=Theme.FONT_BOLD, relief="flat", bd=0, 
                        padx=15, pady=8, command=command, cursor="hand2")
        if width: btn.configure(width=width)
        UIHelpers.apply_hover(btn, Theme.PRIMARY, Theme.PRIMARY_HOVER)
        return btn
