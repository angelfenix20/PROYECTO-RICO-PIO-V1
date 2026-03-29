import os

from billing_logic import BillingLogic

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
    """
    Fachada para compatibilidad con la UI anterior, ahora redirigida a BillingLogic (SQLite).
    """
    _billing = BillingLogic()

    @staticmethod
    def get_tasa_usd():
        try:
            val = BusinessLogic._billing.get_config("tasa_usd", "468.51")
            return float(val)
        except Exception:
            return 468.51

    @staticmethod
    def set_tasa_usd(valor):
        return BusinessLogic._billing.set_config("tasa_usd", valor)

    @staticmethod
    def get_grupos():
        return BusinessLogic._billing.get_grupos()

    @staticmethod
    def get_mesas():
        mesas_db = BusinessLogic._billing.get_mesas()
        # Adaptar formato de DB al formato que la UI espera (bool para ocupada)
        return [{"id": m["id"], "label": m["label"], "ocupada": bool(m["ocupada"]), "cliente": m["cliente"]} for m in mesas_db]

    @staticmethod
    def set_mesas(mesas):
        # En esta nueva arquitectura, las mesas se actualizan individualmente, 
        # pero mantenemos esto por retrocompatibilidad si es necesario.
        for m in mesas:
            BusinessLogic._billing.actualizar_mesa(m["id"], m["ocupada"], m.get("cliente", ""))
        return True

    @staticmethod
    def calcular_impuesto(monto, tasa_iva=0.16):
        return monto * tasa_iva

    # Aquí irá la lógica de cálculos, impuestos y gestión de inventario
    @staticmethod
    def calcular_impuesto(monto, tasa_iva=0.16):
        return monto * tasa_iva
