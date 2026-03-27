import sys
import os

# Añadir src al path para importar db_manager
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from db_manager import DatabaseManager
from billing_logic import BillingLogic

def seed():
    db = DatabaseManager()
    logic = BillingLogic()
    
    print("Iniciando población de datos genéricos...")
    
    # 1. Insertar Grupos (Basado en la lógica previa pero anónimo)
    grupos = [
        ("01", "PIZZAS", "#FF8C00"),
        ("02", "HAMBURGUESAS", "#8B4513"),
        ("03", "BEBIDAS", "#FF0000"),
        ("04", "POSTRES", "#6495ED")
    ]
    for cod, nom, col in grupos:
        try:
            db.execute_query("INSERT INTO grupos (codigo, nombre, color) VALUES (?, ?, ?)", (cod, nom, col))
        except: pass # Evitar error si ya existen

    # 2. Insertar Productos Genéricos
    productos = [
        ("P01", "PIZZA MARGARITA XL", 12.50, 1),
        ("P02", "HAMBURGUESA CLASICA", 8.00, 2),
        ("P03", "REFRESCO 600ML", 1.50, 3),
        ("P04", "BROWNIE CON HELADO", 4.50, 4)
    ]
    for cod, nom, precio, gid in productos:
        try:
            logic.registrar_producto(cod, nom, precio, gid)
        except: pass

    # 3. Cliente Genérico
    try:
        logic.registrar_cliente("V-00000000", "CLIENTE EVENTUAL", "0000-0000000", "CIUDAD", "info@email.com")
    except: pass

    # 4. Usuario de Prueba Anónimo
    try:
        db.execute_query("INSERT INTO usuarios (username, password_hash, rol) VALUES (?, ?, ?)", 
                         ("admin_01", "hash_simulado", "ADMINISTRADOR"))
    except: pass

    print("Sembrado completado exitosamente con datos 100% anónimos.")

if __name__ == "__main__":
    seed()
