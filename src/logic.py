import json
import os

class AuthService:
    # Simulación de base de datos de usuarios
    _USUARIOS = {
        "gaby01": {"clave": "1", "rol": "administrador"},
        "caja01": {"clave": "2", "rol": "cajero"}
    }

    @staticmethod
    def validar_login(usuario, clave):
        if usuario in AuthService._USUARIOS and AuthService._USUARIOS[usuario]["clave"] == clave:
            return AuthService._USUARIOS[usuario]
        return None

class BusinessLogic:
    _CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "config.json")

    @staticmethod
    def get_tasa_usd():
        try:
            if os.path.exists(BusinessLogic._CONFIG_PATH):
                with open(BusinessLogic._CONFIG_PATH, "r") as f:
                    data = json.load(f)
                    return data.get("tasa_usd", 468.51)
        except Exception:
            pass
        return 468.51

    @staticmethod
    def set_tasa_usd(valor):
        try:
            data = {"tasa_usd": float(valor)}
            # Mantener otros datos si existen
            if os.path.exists(BusinessLogic._CONFIG_PATH):
                with open(BusinessLogic._CONFIG_PATH, "r") as f:
                    old_data = json.load(f)
                    old_data["tasa_usd"] = float(valor)
                    data = old_data
                    
            os.makedirs(os.path.dirname(BusinessLogic._CONFIG_PATH), exist_ok=True)
            with open(BusinessLogic._CONFIG_PATH, "w") as f:
                json.dump(data, f, indent=4)
            return True
        except Exception:
            return False

    @staticmethod
    def get_grupos():
        default_grupos = [
            {"codigo": "01", "nombre": "PIZZAS", "color": "#FF8C00"},
            {"codigo": "02", "nombre": "HAMBURGUESAS", "color": "#8B4513"},
            {"codigo": "03", "nombre": "POLLOS", "color": "#4B0082"},
            {"codigo": "04", "nombre": "SOPAS", "color": "#008000"},
            {"codigo": "05", "nombre": "ENSALADAS", "color": "#FFA07A"},
            {"codigo": "06", "nombre": "ENTRADAS", "color": "#1E90FF"},
            {"codigo": "07", "nombre": "BEBIDAS", "color": "#FF0000"},
            {"codigo": "08", "nombre": "LICORES", "color": "#0000FF"},
            {"codigo": "09", "nombre": "PROMOCIONES", "color": "#FF8C00"},
            {"codigo": "10", "nombre": "PANADERIA", "color": "#FF1493"},
            {"codigo": "11", "nombre": "POSTRES", "color": "#6495ED"},
            {"codigo": "12", "nombre": "PASTAS", "color": "#008080"},
        ]
        try:
            if os.path.exists(BusinessLogic._CONFIG_PATH):
                with open(BusinessLogic._CONFIG_PATH, "r") as f:
                    data = json.load(f)
                    if "grupos" in data:
                        return data["grupos"]
                    else:
                        data["grupos"] = default_grupos
                        with open(BusinessLogic._CONFIG_PATH, "w") as fw:
                            json.dump(data, fw, indent=4)
                        return default_grupos
            else:
                BusinessLogic.set_grupos(default_grupos)
                return default_grupos
        except Exception:
            return default_grupos

    @staticmethod
    def set_grupos(grupos):
        try:
            data = {}
            if os.path.exists(BusinessLogic._CONFIG_PATH):
                with open(BusinessLogic._CONFIG_PATH, "r") as f:
                    data = json.load(f)
            data["grupos"] = grupos
            os.makedirs(os.path.dirname(BusinessLogic._CONFIG_PATH), exist_ok=True)
            with open(BusinessLogic._CONFIG_PATH, "w") as f:
                json.dump(data, f, indent=4)
            return True
        except Exception:
            return False

    @staticmethod
    def get_mesas():
        # Inicializar 25 mesas por defecto
        default_mesas = [{"id": f"{i:02d}", "label": f"M{i:02d}", "ocupada": False, "cliente": ""} for i in range(1, 26)]
        try:
            if os.path.exists(BusinessLogic._CONFIG_PATH):
                with open(BusinessLogic._CONFIG_PATH, "r") as f:
                    data = json.load(f)
                    if "mesas" in data:
                        return data["mesas"]
                    else:
                        data["mesas"] = default_mesas
                        with open(BusinessLogic._CONFIG_PATH, "w") as fw:
                            json.dump(data, fw, indent=4)
                        return default_mesas
            else:
                BusinessLogic.set_mesas(default_mesas)
                return default_mesas
        except Exception:
            return default_mesas

    @staticmethod
    def set_mesas(mesas):
        try:
            data = {}
            if os.path.exists(BusinessLogic._CONFIG_PATH):
                with open(BusinessLogic._CONFIG_PATH, "r") as f:
                    data = json.load(f)
            data["mesas"] = mesas
            os.makedirs(os.path.dirname(BusinessLogic._CONFIG_PATH), exist_ok=True)
            with open(BusinessLogic._CONFIG_PATH, "w") as f:
                json.dump(data, f, indent=4)
            return True
        except Exception:
            return False

    # Aquí irá la lógica de cálculos, impuestos y gestión de inventario
    @staticmethod
    def calcular_impuesto(monto, tasa_iva=0.16):
        return monto * tasa_iva
