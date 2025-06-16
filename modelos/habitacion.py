from modelos.database import db

class Habitacion:
    """
    Clase Habitación para gestionar las habitaciones del hotel.
    
    Atributos:
        id (int): ID único de la habitación
        numero (str): Número de la habitación
        tipo (str): Tipo de habitación (individual, doble, suite)
        precio (float): Precio por noche
        estado (str): Estado de la habitación (disponible, ocupada)
    """
    
    def __init__(self, numero, tipo, precio, estado='disponible', habitacion_id=None):
        """
        Inicializa una habitación.
        
        Args:
            numero (str): Número de la habitación
            tipo (str): Tipo de habitación
            precio (float): Precio por noche
            estado (str): Estado de la habitación
            habitacion_id (int): ID de la habitación (opcional)
        """
        self.id = habitacion_id
        self.numero = numero
        self.tipo = tipo
        self.precio = precio
        self.estado = estado
    
    def guardar(self):
        """
        Guarda la habitación en la base de datos.
        
        Returns:
            bool: True si se guardó exitosamente, False en caso contrario
        """
        try:
            query = '''
                INSERT INTO habitaciones (numero, tipo, precio, estado)
                VALUES (?, ?, ?, ?)
            '''
            params = (self.numero, self.tipo, self.precio, self.estado)
            
            result = db.execute_query(query, params)
            return result > 0
            
        except Exception as e:
            print(f"Error al guardar habitación: {e}")
            return False
    
    def actualizar(self):
        """
        Actualiza los datos de la habitación en la base de datos.
        
        Returns:
            bool: True si se actualizó exitosamente, False en caso contrario
        """
        try:
            query = '''
                UPDATE habitaciones 
                SET numero=?, tipo=?, precio=?, estado=?
                WHERE id=?
            '''
            params = (self.numero, self.tipo, self.precio, self.estado, self.id)
            
            result = db.execute_query(query, params)
            return result > 0
            
        except Exception as e:
            print(f"Error al actualizar habitación: {e}")
            return False
    
    def eliminar(self):
        """
        Elimina la habitación de la base de datos.
        
        Returns:
            bool: True si se eliminó exitosamente, False en caso contrario
        """
        try:
            query = 'DELETE FROM habitaciones WHERE id=?'
            result = db.execute_query(query, (self.id,))
            return result > 0
            
        except Exception as e:
            print(f"Error al eliminar habitación: {e}")
            return False
    
    @classmethod
    def cambiar_estado(cls, habitacion_id, nuevo_estado):
        """
        Cambia el estado de la habitación.
        
        Args:
            habitacion_id (int): ID de la habitación
            nuevo_estado (str): Nuevo estado (disponible, ocupada)
            
        Returns:
            bool: True si se cambió exitosamente, False en caso contrario
        """
        try:
            query = "UPDATE habitaciones SET estado=? WHERE id=?"
            db.execute_query(query, (nuevo_estado, habitacion_id))
            return True
        except Exception as e:
            print(f"Error al cambiar estado de la habitación: {e}")
            return False
    
    @classmethod
    def buscar_por_id(cls, habitacion_id):
        """
        Busca una habitación por su ID.
        
        Args:
            habitacion_id (int): ID de la habitación a buscar
            
        Returns:
            Habitacion: Instancia de la habitación encontrada o None
        """
        try:
            query = 'SELECT * FROM habitaciones WHERE id=?'
            result = db.execute_query(query, (habitacion_id,))
            
            if result:
                room_data = result[0]
                return cls(
                    numero=room_data[1],
                    tipo=room_data[2],
                    precio=room_data[3],
                    estado=room_data[4],
                    habitacion_id=room_data[0]
                )
            return None
            
        except Exception as e:
            print(f"Error al buscar habitación: {e}")
            return None
    
    @classmethod
    def buscar_por_numero(cls, numero):
        """
        Busca una habitación por su número.
        
        Args:
            numero (str): Número de la habitación a buscar
            
        Returns:
            Habitacion: Instancia de la habitación encontrada o None
        """
        try:
            query = 'SELECT * FROM habitaciones WHERE numero=?'
            result = db.execute_query(query, (numero,))
            
            if result:
                room_data = result[0]
                return cls(
                    numero=room_data[1],
                    tipo=room_data[2],
                    precio=room_data[3],
                    estado=room_data[4],
                    habitacion_id=room_data[0]
                )
            return None
            
        except Exception as e:
            print(f"Error al buscar habitación por número: {e}")
            return None
    
    @classmethod
    def obtener_todas(cls):
        """
        Obtiene todas las habitaciones del sistema.
        
        Returns:
            list: Lista de todas las habitaciones
        """
        try:
            query = 'SELECT * FROM habitaciones ORDER BY numero'
            results = db.execute_query(query)
            
            habitaciones = []
            for room_data in results:
                habitacion = cls(
                    numero=room_data[1],
                    tipo=room_data[2],
                    precio=room_data[3],
                    estado=room_data[4],
                    habitacion_id=room_data[0]
                )
                habitaciones.append(habitacion)
            
            return habitaciones
            
        except Exception as e:
            print(f"Error al obtener habitaciones: {e}")
            return []
    
    @classmethod
    def obtener_disponibles(cls):
        """
        Obtiene todas las habitaciones disponibles.
        
        Returns:
            list: Lista de habitaciones disponibles
        """
        try:
            query = 'SELECT * FROM habitaciones WHERE estado=? ORDER BY numero'
            results = db.execute_query(query, ('disponible',))
            
            habitaciones = []
            for room_data in results:
                habitacion = cls(
                    numero=room_data[1],
                    tipo=room_data[2],
                    precio=room_data[3],
                    estado=room_data[4],
                    habitacion_id=room_data[0]
                )
                habitaciones.append(habitacion)
            
            return habitaciones
            
        except Exception as e:
            print(f"Error al obtener habitaciones disponibles: {e}")
            return []
    
    @classmethod
    def obtener_por_tipo(cls, tipo):
        """
        Obtiene habitaciones por tipo.
        
        Args:
            tipo (str): Tipo de habitación a buscar
            
        Returns:
            list: Lista de habitaciones del tipo especificado
        """
        try:
            query = 'SELECT * FROM habitaciones WHERE tipo=? ORDER BY numero'
            results = db.execute_query(query, (tipo,))
            
            habitaciones = []
            for room_data in results:
                habitacion = cls(
                    numero=room_data[1],
                    tipo=room_data[2],
                    precio=room_data[3],
                    estado=room_data[4],
                    habitacion_id=room_data[0]
                )
                habitaciones.append(habitacion)
            
            return habitaciones
            
        except Exception as e:
            print(f"Error al obtener habitaciones por tipo: {e}")
            return []
    
    @classmethod
    def obtener_precio_por_id(cls, habitacion_id):
        """
        Obtiene el precio de una habitación por su ID.
        
        Args:
            habitacion_id (int): ID de la habitación
            
        Returns:
            float: Precio de la habitación, 0 si no se encuentra
        """
        query = "SELECT precio FROM habitaciones WHERE id=?"
        result = db.execute_query(query, (habitacion_id,))
        return float(result[0][0]) if result else 0
    
    def __str__(self):
        """Representación en string de la habitación."""
        return f"Habitación {self.numero} - {self.tipo} - ${self.precio} - {self.estado}"
    
    def to_dict(self):
        """
        Convierte la habitación a diccionario.
        
        Returns:
            dict: Datos de la habitación en formato diccionario
        """
        return {
            'id': self.id,
            'numero': self.numero,
            'tipo': self.tipo,
            'precio': self.precio,
            'estado': self.estado
        }