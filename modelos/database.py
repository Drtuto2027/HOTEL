"""
Módulo de configuración y conexión a la base de datos SQLite.
"""

import sqlite3
from pathlib import Path

class Database:
    """Clase para manejar la conexión y configuración de la base de datos."""
    
    def __init__(self, db_name="hotel.db"):
        """
        Inicializa la conexión a la base de datos.
        
        Args:
            db_name (str): Nombre del archivo de la base de datos
        """
        self.db_path = Path(__file__).parent / db_name
        self.connection = None
        self.create_database()
    
    def get_connection(self):
        """
        Obtiene una conexión a la base de datos.
        
        Returns:
            sqlite3.Connection: Objeto de conexión a la base de datos
        """
        try:
            return sqlite3.connect(self.db_path)
        except sqlite3.Error as e:
            print(f"Error al conectar con la base de datos: {e}")
            return None
    
    def create_database(self):
        """Crea las tablas necesarias en la base de datos."""
        conn = self.get_connection()
        if conn is None:
            return
        
        try:
            cursor = conn.cursor()
            
            # Tabla de usuarios (base para todos los roles)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    cedula TEXT PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    apellido TEXT NOT NULL,
                    telefono TEXT,
                    email TEXT,
                    contraseña TEXT NOT NULL,
                    rol TEXT NOT NULL CHECK (rol IN ('administrador', 'recepcionista', 'cliente'))
                )
            ''')
            
            # Tabla de habitaciones
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS habitaciones (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    numero TEXT UNIQUE NOT NULL,
                    tipo TEXT NOT NULL CHECK (tipo IN ('individual', 'doble', 'suite')),
                    precio REAL NOT NULL,
                    estado TEXT NOT NULL CHECK (estado IN ('disponible', 'ocupada')) DEFAULT 'disponible'
                )
            ''')
            
            # Tabla de reservas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS reservas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente_cedula TEXT NOT NULL,
                    habitacion_id INTEGER NOT NULL,
                    fecha_entrada TEXT NOT NULL,
                    fecha_salida TEXT NOT NULL,
                    estado TEXT NOT NULL CHECK (estado IN ('pendiente', 'confirmada', 'cancelada')) DEFAULT 'pendiente',
                    FOREIGN KEY (cliente_cedula) REFERENCES usuarios(cedula),
                    FOREIGN KEY (habitacion_id) REFERENCES habitaciones(id)
                )
            ''')
            
            # Tabla de facturas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS facturas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente_cedula TEXT NOT NULL,
                    reserva_id INTEGER,
                    detalles TEXT NOT NULL,
                    monto_total REAL NOT NULL,
                    fecha TEXT NOT NULL,
                    FOREIGN KEY (cliente_cedula) REFERENCES usuarios(cedula),
                    FOREIGN KEY (reserva_id) REFERENCES reservas(id)
                )
            ''')
            
            # Insertar datos de prueba
            self.insert_sample_data(cursor)
            
            conn.commit()
            print("Base de datos creada exitosamente")
            
        except sqlite3.Error as e:
            print(f"Error al crear la base de datos: {e}")
        finally:
            conn.close()
    
    def insert_sample_data(self, cursor):
        """Inserta datos de prueba en la base de datos."""
        try:  
            # Habitaciones de prueba
            sample_rooms = [
                ('101', 'individual', 50000, 'disponible'),
                ('102', 'doble', 80000, 'disponible'),
                ('201', 'suite', 150000, 'disponible'),
                ('202', 'doble', 80000, 'disponible'),
            ]
            
            cursor.executemany('''
                INSERT OR IGNORE INTO habitaciones 
                (numero, tipo, precio, estado)
                VALUES (?, ?, ?, ?)
            ''', sample_rooms)
            
        except sqlite3.Error as e:
            print(f"Error al insertar datos de prueba: {e}")
    
    def execute_query(self, query, params=None):
        """
        Ejecuta una consulta en la base de datos.
        
        Args:
            query (str): Consulta SQL a ejecutar
            params (tuple): Parámetros para la consulta
            
        Returns:
            list: Resultados de la consulta
        """
        conn = self.get_connection()
        if conn is None:
            return []
        
        try:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                return cursor.fetchall()
            else:
                conn.commit()
                return cursor.rowcount
                
        except sqlite3.Error as e:
            print(f"Error al ejecutar consulta: {e}")
            return []
        finally:
            conn.close()

# Instancia global de la base de datos
db = Database()