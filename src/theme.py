class Theme:
    # --- Colores Base (Gestim Inspired - Deep Dark) ---
    APP_BG = "#0c0a09"       # Stone 950 (Fondo profundo)
    SURFACE = "#1c1917"      # Stone 900 (Panel elevado)
    SURFACE_LIGHT = "#292524" # Stone 800 (Hover/Selección)
    BORDER = "#44403c"       # Stone 700 (Bordes sutiles)
    
    # --- Textos ---
    TEXT_PRIMARY = "#fafaf9"   # Stone 50 (Blanco roto)
    TEXT_SECONDARY = "#a8a29e" # Stone 400 (Gris suave)
    TEXT_LIGHT = "#ffffff"     
    
    # --- Colores de Acción ---
    PRIMARY = "#10b981"       # Emerald 500 (Gestim Green)
    PRIMARY_HOVER = "#059669" # Emerald 600
    SECONDARY = "#78350f"     # Amber 900 (Acento marrón Gestim)
    ACCENT = "#f59e0b"        # Amber 500 (Alertas)
    DANGER = "#ef4444"        # Rose 500
    SUCCESS = "#10b981"
    
    # --- Tipografías (Moderna) ---
    FONT_FAMILY = "Segoe UI"
    FONT_H1 = ("Segoe UI", 18, "bold")
    FONT_H2 = ("Segoe UI", 14, "bold")
    FONT_H3 = ("Segoe UI", 11, "bold")
    FONT_BODY = ("Segoe UI", 10)
    FONT_BOLD = ("Segoe UI", 10, "bold")
    FONT_SMALL = ("Segoe UI", 9)

    # --- Alias para compatibilidad ---
    BG_DEFAULT = APP_BG
    BG_WHITE = SURFACE
    HEADER_BG = SURFACE
    SIDEBAR_BG = "#0c0a09"
    FOOTER_BG = "#1c1917"

    # Estática compatible con el código anterior
    HEADER_BG_DARK = SIDEBAR_BG
    HEADER_FG_DARK = TEXT_LIGHT
    ACCENT_BLUE = PRIMARY
    ACCENT_RED = DANGER
    BUTTON_GRAY = TEXT_SECONDARY
    MODAL_HEADER_BG = SECONDARY
    ENTRY_HIGHLIGHT = "#3f3f46" # Zinc 700
    SUCCESS_GREEN = SUCCESS
    DARK_PANEL = SURFACE
    
    # Mapeo de fuentes anteriores
    FONT_NORMAL = FONT_BODY
    FONT_TITLE = FONT_H2
