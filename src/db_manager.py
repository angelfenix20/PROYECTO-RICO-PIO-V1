import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    """
    Gestor de Base de Datos SQLite para el Proyecto Rico Pio.
    Sigue el patrón Singleton para asegurar una única conexión base.
    Aplica integridad referencial estricta y formato ISO 8601.
    """
    _instance = None
    _DB_NAME = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "ricopio.db")

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._init_db()
        return cls._instance

    def _get_connection(self):
        # Asegurar que la carpeta data existe
        os.makedirs(os.path.dirname(self._DB_NAME), exist_ok=True)
        conn = sqlite3.connect(self._DB_NAME)
        # Habilitar claves fóraneas en cada conexión
        conn.execute("PRAGMA foreign_keys = ON;")
        # Permitir acceso por nombre de columna
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """Inicializa las tablas siguiendo el esquema 3NF (Tercera Forma Normal)."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # 1. Tabla Clientes (Anonimización: No nombres reales en el código)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cedula_rif TEXT UNIQUE NOT NULL,
                    nombre TEXT NOT NULL,
                    telefono TEXT,
                    direccion TEXT,
                    email TEXT
                )
            """)

            # 2. Tabla Grupos (Categorías de productos)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS grupos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    codigo TEXT UNIQUE NOT NULL,
                    nombre TEXT NOT NULL,
                    color TEXT
                )
            """)

            # 3. Tabla Productos (Precios en USD para estabilidad financiera)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    codigo TEXT UNIQUE NOT NULL,
                    nombre TEXT NOT NULL,
                    precio_usd REAL NOT NULL,
                    grupo_id INTEGER,
                    iva_porcentaje REAL DEFAULT 0.16,
                    color TEXT DEFAULT '#CCCCCC',
                    imagen_path TEXT DEFAULT '',
                    FOREIGN KEY (grupo_id) REFERENCES grupos (id)
                )
            """)

            # 4. Tabla Facturas (Maestro de Ventas)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS facturas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    numero_control TEXT UNIQUE NOT NULL,
                    cliente_id INTEGER NOT NULL,
                    fecha TEXT NOT NULL, -- Formato ISO 8601: YYYY-MM-DD HH:MM:SS
                    subtotal REAL NOT NULL,
                    iva REAL NOT NULL,
                    total REAL NOT NULL,
                    tasa_usd REAL NOT NULL,
                    metodo_pago TEXT, -- 'EFECTIVO', 'PUNTO', 'TRANSFERENCIA', 'PAGO_MOVIL'
                    estatus TEXT DEFAULT 'PENDIENTE', -- 'PAGADA', 'ANULADA', 'PENDIENTE'
                    FOREIGN KEY (cliente_id) REFERENCES clientes (id)
                )
            """)

            # 5. Tabla Detalles Factura (Detalle de Ventas)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS detalles_factura (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    factura_id INTEGER NOT NULL,
                    producto_id INTEGER NOT NULL,
                    cantidad REAL NOT NULL,
                    precio_unitario REAL NOT NULL,
                    total_linea REAL NOT NULL,
                    FOREIGN KEY (factura_id) REFERENCES facturas (id) ON DELETE CASCADE,
                    FOREIGN KEY (producto_id) REFERENCES productos (id)
                )
            """)

            # 6. Tabla Cierre de Caja (Reporte Diario)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cierre_caja (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha_apertura TEXT NOT NULL,
                    fecha_cierre TEXT,
                    monto_inicial REAL NOT NULL,
                    monto_final REAL,
                    ventas_totales REAL DEFAULT 0.0,
                    usuario TEXT NOT NULL,
                    FOREIGN KEY (usuario) REFERENCES usuarios (username)
                )
            """)
            
            # 7. Tabla Usuarios
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    rol TEXT NOT NULL
                )
            """)

            # 8. Tabla Mesas (Centralización)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS mesas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    label TEXT UNIQUE NOT NULL,
                    ocupada INTEGER DEFAULT 0, -- 0: Libre, 1: Ocupada
                    cliente TEXT DEFAULT ''
                )
            """)

            # 9. Tabla Configuración (Tasa USD, etc.)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS configuracion (
                    clave TEXT PRIMARY KEY,
                    valor TEXT NOT NULL
                )
            """)
            
            conn.commit()
            self._migrate_initial_data(conn)

    def _migrate_initial_data(self, conn):
        """Migra datos iniciales desde config.json si existen y la base de datos está vacía."""
        cursor = conn.cursor()
        
        config_path = os.path.join(os.path.dirname(self._DB_NAME), "config.json")
        config_data = {}
        if os.path.exists(config_path):
            import json
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    config_data = json.load(f)
            except Exception as e:
                print(f"Error leyendo config.json: {e}")

        # Migrar Grupos
        cursor.execute("SELECT COUNT(*) FROM grupos")
        if cursor.fetchone()[0] == 0:
            if "grupos" in config_data:
                for g in config_data["grupos"]:
                    cursor.execute("INSERT INTO grupos (codigo, nombre, color) VALUES (?, ?, ?)", 
                                   (g.get("codigo"), g.get("nombre"), g.get("color", "#CCCCCC")))
            else:
                default_grupos = [
                    ("01", "PIZZAS", "#FF8C00"), ("02", "HAMBURGUESAS", "#8B4513"),
                    ("03", "BEBIDAS", "#FF0000"), ("04", "POSTRES", "#6495ED")
                ]
                for cod, nom, col in default_grupos:
                    cursor.execute("INSERT INTO grupos (codigo, nombre, color) VALUES (?, ?, ?)", (cod, nom, col))

        # Migrar Mesas
        cursor.execute("SELECT COUNT(*) FROM mesas")
        if cursor.fetchone()[0] == 0:
            if "mesas" in config_data:
                for m in config_data["mesas"]:
                    cursor.execute("INSERT INTO mesas (label, ocupada, cliente) VALUES (?, ?, ?)", 
                                   (m.get("label"), 1 if m.get("ocupada") else 0, m.get("cliente", "")))
            else:
                for i in range(1, 26):
                    cursor.execute("INSERT INTO mesas (label) VALUES (?)", (f"M{i:02d}",))

        # Migrar Tasa USD
        cursor.execute("SELECT COUNT(*) FROM configuracion WHERE clave = 'tasa_usd'")
        if cursor.fetchone()[0] == 0:
            tasa = config_data.get("tasa_usd", "468.51")
            cursor.execute("INSERT INTO configuracion (clave, valor) VALUES (?, ?)", ("tasa_usd", str(tasa)))

        # Semillar Productos si la tabla está vacía
        cursor.execute("SELECT COUNT(*) FROM productos")
        if cursor.fetchone()[0] == 0:
            productos_semilla = [
                ("P001", "Pizza Margarita", 8.50, 1, 0.16, "#FF8C00"),
                ("P002", "Pizza Pepperoni", 10.00, 1, 0.16, "#FF8C00"),
                ("H001", "Hamburguesa Clásica", 5.50, 2, 0.16, "#8B4513"),
                ("B001", "Refresco Familiar", 2.00, 3, 0.16, "#FF0000"),
            ]
            for cod, nom, pre, gid, iva, col in productos_semilla:
                cursor.execute("INSERT INTO productos (codigo, nombre, precio_usd, grupo_id, iva_porcentaje, color) VALUES (?, ?, ?, ?, ?, ?)",
                               (cod, nom, pre, gid, iva, col))

        # Migración de Esquema V2
        try:
            cursor.execute("SELECT color FROM productos LIMIT 1")
        except sqlite3.OperationalError:
            cursor.execute("ALTER TABLE productos ADD COLUMN color TEXT DEFAULT '#CCCCCC'")
            
        try:
            cursor.execute("SELECT imagen_path FROM productos LIMIT 1")
        except sqlite3.OperationalError:
            cursor.execute("ALTER TABLE productos ADD COLUMN imagen_path TEXT DEFAULT ''")
        
        conn.commit()

    def execute_query(self, query, params=()):
        """Ejecuta una consulta de escritura (INSERT, UPDATE, DELETE)."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            # Manejo de errores según requerimientos del Pront Maestro
            print(f"CRITICAL SQL ERROR: {e} | Query: {query}")
            raise

    def fetch_all(self, query, params=()):
        """Retorna todos los resultados de una consulta SELECT."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"SQL SELECT ERROR: {e}")
            return []

    def fetch_one(self, query, params=()):
        """Retorna un único resultado de una consulta SELECT."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                row = cursor.fetchone()
                return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"SQL SELECT ONE ERROR: {e}")
            return None
