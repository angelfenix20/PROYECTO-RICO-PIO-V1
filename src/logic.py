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
