from modelos.database import db

class Usuario:
    """
    Clase base para todos los usuarios del sistema.
    
    Atributos:
        cedula (str): Cédula del usuario
        nombre (str): Nombre del usuario
        apellido (str): Apellido del usuario
        telefono (str): Teléfono del usuario
        email (str): Email del usuario
        contraseña (str): Contraseña del usuario
        rol (str): Rol del usuario (administrador, recepcionista, cliente)
    """
    
    def __init__(self, cedula, nombre, apellido, telefono, email, contraseña, rol):
        """
        Inicializa un usuario.
        
        Args:
            cedula (str): Cédula del usuario
            nombre (str): Nombre del usuario
            apellido (str): Apellido del usuario
            telefono (str): Teléfono del usuario
            email (str): Email del usuario
            contraseña (str): Contraseña del usuario
            rol (str): Rol del usuario
        """
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.email = email
        self.contraseña = contraseña
        self.rol = rol
    
    def guardar(self):
        """
        Guarda el usuario en la base de datos.
        
        Returns:
            bool: True si se guardó exitosamente, False en caso contrario
        """
        try:
            query = '''
                INSERT INTO usuarios (cedula, nombre, apellido, telefono, email, contraseña, rol)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            '''
            params = (self.cedula, self.nombre, self.apellido, self.telefono, 
                     self.email, self.contraseña, self.rol)
            
            result = db.execute_query(query, params)
            return result > 0
            
        except Exception as e:
            print(f"Error al guardar usuario: {e}")
            return False
    
    def actualizar(self):
        """
        Actualiza los datos del usuario en la base de datos.
        
        Returns:
            bool: True si se actualizó exitosamente, False en caso contrario
        """
        try:
            query = '''
                UPDATE usuarios 
                SET nombre=?, apellido=?, telefono=?, email=?, contraseña=?
                WHERE cedula=?
            '''
            params = (self.nombre, self.apellido, self.telefono, 
                     self.email, self.contraseña, self.cedula)
            
            result = db.execute_query(query, params)
            return result > 0
            
        except Exception as e:
            print(f"Error al actualizar usuario: {e}")
            return False
    
    def eliminar(self):
        """
        Elimina el usuario de la base de datos.
        
        Returns:
            bool: True si se eliminó exitosamente, False en caso contrario
        """
        try:
            query = 'DELETE FROM usuarios WHERE cedula=?'
            result = db.execute_query(query, (self.cedula,))
            return result > 0
            
        except Exception as e:
            print(f"Error al eliminar usuario: {e}")
            return False
    
    @classmethod
    def buscar_por_cedula(cls, cedula):
        """
        Busca un usuario por su cédula.
        
        Args:
            cedula (str): Cédula del usuario a buscar
            
        Returns:
            Usuario: Instancia del usuario encontrado o None
        """
        try:
            query = 'SELECT * FROM usuarios WHERE cedula=?'
            result = db.execute_query(query, (cedula,))
            
            if result:
                user_data = result[0]
                return cls(
                    cedula=user_data[0],
                    nombre=user_data[1],
                    apellido=user_data[2],
                    telefono=user_data[3],
                    email=user_data[4],
                    contraseña=user_data[5],
                    rol=user_data[6]
                )
            return None
            
        except Exception as e:
            print(f"Error al buscar usuario: {e}")
            return None
    
    @classmethod
    def validar_login(cls, cedula, contraseña):
        """
        Valida las credenciales de login de un usuario.
        
        Args:
            cedula (str): Cédula del usuario
            contraseña (str): Contraseña del usuario
            
        Returns:
            Usuario: Instancia del usuario si las credenciales son válidas, None en caso contrario
        """
        try:
            query = 'SELECT * FROM usuarios WHERE cedula=? AND contraseña=?'
            result = db.execute_query(query, (cedula, contraseña))
            
            if result:
                user_data = result[0]
                return cls(
                    cedula=user_data[0],
                    nombre=user_data[1],
                    apellido=user_data[2],
                    telefono=user_data[3],
                    email=user_data[4],
                    contraseña=user_data[5],
                    rol=user_data[6]
                )
            return None
            
        except Exception as e:
            print(f"Error al validar login: {e}")
            return None
    
    @classmethod
    def obtener_todos_por_rol(cls, rol):
        """
        Obtiene todos los usuarios de un rol específico.
        
        Args:
            rol (str): Rol de los usuarios a buscar
            
        Returns:
            list: Lista de usuarios del rol especificado
        """
        try:
            query = 'SELECT * FROM usuarios WHERE rol=?'
            results = db.execute_query(query, (rol,))
            
            usuarios = []
            for user_data in results:
                usuario = cls(
                    cedula=user_data[0],
                    nombre=user_data[1],
                    apellido=user_data[2],
                    telefono=user_data[3],
                    email=user_data[4],
                    contraseña=user_data[5],
                    rol=user_data[6]
                )
                usuarios.append(usuario)
            
            return usuarios
            
        except Exception as e:
            print(f"Error al obtener usuarios por rol: {e}")
            return []
    
    def __str__(self):
        """Representación en string del usuario."""
        return f"{self.nombre} {self.apellido} ({self.cedula}) - {self.rol}"
    
    def to_dict(self):
        """
        Convierte el usuario a diccionario.
        
        Returns:
            dict: Datos del usuario en formato diccionario
        """
        return {
            'cedula': self.cedula,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'telefono': self.telefono,
            'email': self.email,
            'rol': self.rol
        }