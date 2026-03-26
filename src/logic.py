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
    # Aquí irá la lógica de cálculos, impuestos y gestión de inventario
    @staticmethod
    def calcular_impuesto(monto, tasa_iva=0.16):
        return monto * tasa_iva
