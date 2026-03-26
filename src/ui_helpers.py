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
    def create_header(parent, title, bg_color=Theme.MODAL_HEADER_BG, height=38):
        header = tk.Frame(parent, bg=bg_color, height=height)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text=title, fg="white", bg=bg_color, font=Theme.FONT_TITLE).pack(side="left", padx=12, pady=6)
        return header

    @staticmethod
    def lbl(parent, text, row, col, anchor="e", bg="white", font=Theme.FONT_NORMAL):
        l = tk.Label(parent, text=text, bg=bg, font=font)
        l.grid(row=row, column=col, sticky=anchor, padx=4, pady=3)
        return l

    @staticmethod
    def entry(parent, row, col, width=22, bg="white"):
        e = tk.Entry(parent, width=width, bg=bg, relief="solid", bd=1)
        e.grid(row=row, column=col, sticky="w", padx=4, pady=3)
        return e

    @staticmethod
    def create_status_bar(parent, text_left, text_right):
        status = tk.Frame(parent, bg=Theme.FOOTER_BG, height=22)
        status.pack(fill="x", side="bottom")
        status.pack_propagate(False)
        tk.Label(status, text=text_left, bg=Theme.FOOTER_BG, font=Theme.FONT_SMALL).pack(side="left", padx=6)
        tk.Label(status, text=text_right, bg=Theme.FOOTER_BG, font=Theme.FONT_SMALL).pack(side="right", padx=6)
        return status
