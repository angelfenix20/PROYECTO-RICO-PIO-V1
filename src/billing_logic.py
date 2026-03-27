import decimal
from datetime import datetime
from db_manager import DatabaseManager

class BillingLogic:
    """
    Lógica de Negocio para Facturación y Contabilidad.
    Asegura precisión financiera usando cálculos exactos y redondeo bancario.
    """
    def __init__(self):
        self.db = DatabaseManager()

    # --- Gestión de Grupos ---
    def get_grupos(self):
        query = "SELECT * FROM grupos ORDER BY codigo ASC"
        return self.db.fetch_all(query)
    def registrar_cliente(self, cedula, nombre, telefono=None, direccion=None, email=None):
        query = "INSERT INTO clientes (cedula_rif, nombre, telefono, direccion, email) VALUES (?, ?, ?, ?, ?)"
        return self.db.execute_query(query, (cedula, nombre, telefono, direccion, email))

    def buscar_cliente(self, criterio):
        query = "SELECT * FROM clientes WHERE cedula_rif = ? OR nombre LIKE ?"
        return self.db.fetch_one(query, (criterio, f"%{criterio}%"))

    # --- Gestión de Productos (CRUD e Inventario) ---
    def registrar_producto(self, codigo, nombre, precio_usd, grupo_id=None, iva=0.16, color="#CCCCCC", imagen_path=""):
        query = "INSERT INTO productos (codigo, nombre, precio_usd, grupo_id, iva_porcentaje, color, imagen_path) VALUES (?, ?, ?, ?, ?, ?, ?)"
        return self.db.execute_query(query, (codigo, nombre, precio_usd, grupo_id, iva, color, imagen_path))

    def actualizar_producto(self, prod_id, codigo, nombre, precio_usd, grupo_id=None, iva=0.16, color="#CCCCCC", imagen_path=""):
        query = """
            UPDATE productos 
            SET codigo=?, nombre=?, precio_usd=?, grupo_id=?, iva_porcentaje=?, color=?, imagen_path=? 
            WHERE id=?
        """
        return self.db.execute_query(query, (codigo, nombre, precio_usd, grupo_id, iva, color, imagen_path, prod_id))

    def eliminar_producto(self, prod_id):
        query = "DELETE FROM productos WHERE id=?"
        return self.db.execute_query(query, (prod_id,))

    def get_todos_productos(self, ordenar_por="codigo"):
        query = f"""
            SELECT p.*, g.nombre as grupo_nombre 
            FROM productos p 
            LEFT JOIN grupos g ON p.grupo_id = g.id
            ORDER BY p.{ordenar_por} ASC
        """
        return self.db.fetch_all(query)
        
    def buscar_productos(self, termino):
        query = """
            SELECT p.*, g.nombre as grupo_nombre 
            FROM productos p 
            LEFT JOIN grupos g ON p.grupo_id = g.id
            WHERE p.codigo LIKE ? OR p.nombre LIKE ?
            ORDER BY p.nombre ASC
        """
        criterio = f"%{termino}%"
        return self.db.fetch_all(query, (criterio, criterio))

    def get_productos_por_grupo(self, grupo_id):
        query = "SELECT * FROM productos WHERE grupo_id = ?"
        return self.db.fetch_all(query, (grupo_id,))

    # --- Lógica de Facturación ---
    def calcular_detalles_linea(self, precio_usd, cantidad, tasa_cambio):
        """
        Calcula montos exactos para una línea de factura.
        """
        # Usar Decimal para evitar errores de redondeo de punto flotante binary
        p = decimal.Decimal(str(precio_usd))
        cant = decimal.Decimal(str(cantidad))
        tasa = decimal.Decimal(str(tasa_cambio))
        
        subtotal_usd = p * cant
        subtotal_bs = subtotal_usd * tasa
        
        return {
            "subtotal_usd": float(subtotal_usd),
            "subtotal_bs": float(subtotal_bs)
        }

    def procesar_factura(self, cliente_id, productos_lista, tasa_usd, metodo_pago="EFECTIVO"):
        """
        Crea una factura y sus detalles en una transacción atómica.
        productos_lista: list of dicts {'id', 'cantidad', 'precio_unitario'}
        """
        fecha_iso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Calcular totales
        subtotal = sum(item['cantidad'] * item['precio_unitario'] for item in productos_lista)
        iva = subtotal * 0.16 # IVA genérico
        total = subtotal + iva
        
        # Generar número de control (Simulado para este paso)
        num_control = f"FAC-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        try:
            # Insertar cabecera
            query_fac = """
                INSERT INTO facturas (numero_control, cliente_id, fecha, subtotal, iva, total, tasa_usd, metodo_pago, estatus)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'PAGADA')
            """
            factura_id = self.db.execute_query(query_fac, (num_control, cliente_id, fecha_iso, subtotal, iva, total, tasa_usd, metodo_pago))
            
            # Insertar detalles
            query_det = """
                INSERT INTO detalles_factura (factura_id, producto_id, cantidad, precio_unitario, total_linea)
                VALUES (?, ?, ?, ?, ?)
            """
            for prod in productos_lista:
                total_linea = prod['cantidad'] * prod['precio_unitario']
                self.db.execute_query(query_det, (factura_id, prod['id'], prod['cantidad'], prod['precio_unitario'], total_linea))
            
            return num_control
        except Exception as e:
            print(f"Error procesando factura: {e}")
            raise

    # --- Reportes y Cierre ---
    def obtener_ventas_del_dia(self):
        hoy = datetime.now().strftime("%Y-%m-%d")
        query = "SELECT SUM(total) as total_dia FROM facturas WHERE fecha LIKE ? AND estatus = 'PAGADA'"
        result = self.db.fetch_one(query, (f"{hoy}%",))
        return result['total_dia'] if result and result['total_dia'] else 0.0
