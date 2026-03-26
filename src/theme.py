class Theme:
    # Colores Base (Sistema Slate/Indigo)
    APP_BG = "#f8fafc"      # Fondo principal ultra claro
    SURFACE = "#ffffff"     # Superficie de tarjetas y paneles
    BORDER = "#e2e8f0"      # Bordes suaves
    
    # Textos
    TEXT_PRIMARY = "#0f172a"  # Títulos y texto fuerte
    TEXT_SECONDARY = "#64748b" # Texto descriptivo
    TEXT_LIGHT = "#ffffff"     # Texto sobre fondos oscuros
    
    # Colores de Acción
    PRIMARY = "#4f46e5"       # Indigo 600
    PRIMARY_HOVER = "#4338ca" # Indigo 700
    ACCENT = "#10b981"        # Emerald 500 (Éxito)
    DANGER = "#ef4444"        # Red 500
    WARNING = "#f59e0b"       # Amber 500
    
    # Navegación y Paneles
    SIDEBAR_BG = "#1e293b"    # Slate 800 (Fondo oscuro profesional)
    HEADER_BG = "#ffffff"
    
    # Tipografías (Referencia)
    FONT_FAMILY = "Segoe UI" # Fuente nativa de Windows que luce moderna
    FONT_H1 = ("Segoe UI", 16, "bold")
    FONT_H2 = ("Segoe UI", 12, "bold")
    FONT_BODY = ("Segoe UI", 10)
    FONT_SMALL = ("Segoe UI", 9)
    FONT_BOLD = ("Segoe UI", 10, "bold")

    # Estática compatible con el código anterior (para no romper nada de golpe)
    BG_DEFAULT = APP_BG
    BG_WHITE = SURFACE
    HEADER_BG_DARK = SIDEBAR_BG
    HEADER_FG_DARK = TEXT_LIGHT
    ACCENT_BLUE = PRIMARY
    ACCENT_RED = DANGER
    BUTTON_GRAY = TEXT_SECONDARY
    MODAL_HEADER_BG = PRIMARY
    ENTRY_HIGHLIGHT = "#fefce8" # Suave amarillo para foco
    SUCCESS_GREEN = ACCENT
    DARK_PANEL = "#334155"
    FOOTER_BG = "#f1f5f9"
    
    # Mapeo de fuentes anteriores
    FONT_NORMAL = FONT_BODY
    FONT_TITLE = FONT_H2
