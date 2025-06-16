from modelos.cliente import Cliente
from modelos.factura import Factura
from modelos.recepcionista import Recepcionista
from modelos.usuario import Usuario


class Administrador(Usuario):
    """
    Clase Administrador que hereda de Usuario.
    
    Funcionalidades específicas:
    - Gestionar recepcionistas (CRUD)
    - Gestionar clientes (CRUD)
    - Generar informes de ingresos
    """
    
    def __init__(self, cedula, nombre, apellido, telefono, email, contraseña='admin123'):
        """
        Inicializa un administrador.
        
        Args:
            cedula (str): Cédula del administrador
            nombre (str): Nombre del administrador
            apellido (str): Apellido del administrador
            telefono (str): Teléfono del administrador
            email (str): Email del administrador
            contraseña (str): Contraseña del administrador
        """
        super().__init__(cedula, nombre, apellido, telefono, email, contraseña, 'administrador')
    
    def crear_recepcionista(self, cedula, nombre, apellido, telefono, email, contraseña='recep123'):
        """
        Crea un nuevo recepcionista en el sistema.
        
        Args:
            cedula (str): Cédula del recepcionista
            nombre (str): Nombre del recepcionista
            apellido (str): Apellido del recepcionista
            telefono (str): Teléfono del recepcionista
            email (str): Email del recepcionista
            contraseña (str): Contraseña del recepcionista
            
        Returns:
            bool: True si se creó exitosamente, False en caso contrario
        """
        try:
            recepcionista = Recepcionista(cedula, nombre, apellido, telefono, email, contraseña)
            return recepcionista.guardar()
            
        except Exception as e:
            print(f"Error al crear recepcionista: {e}")
            return False
    
    def obtener_recepcionistas(self):
        """
        Obtiene todos los recepcionistas del sistema.
        
        Returns:
            list: Lista de recepcionistas
        """
        try:
            return Usuario.obtener_todos_por_rol('recepcionista')
            
        except Exception as e:
            print(f"Error al obtener recepcionistas: {e}")
            return []
    
    def actualizar_recepcionista(self, cedula, nombre, apellido, telefono, email):
        """
        Actualiza los datos de un recepcionista.
        
        Args:
            cedula (str): Cédula del recepcionista
            nombre (str): Nuevo nombre
            apellido (str): Nuevo apellido
            telefono (str): Nuevo teléfono
            email (str): Nuevo email
            
        Returns:
            bool: True si se actualizó exitosamente, False en caso contrario
        """
        try:
            recepcionista = Usuario.buscar_por_cedula(cedula)
            if recepcionista and recepcionista.rol == 'recepcionista':
                recepcionista.nombre = nombre
                recepcionista.apellido = apellido
                recepcionista.telefono = telefono
                recepcionista.email = email
                return recepcionista.actualizar()
            return False
            
        except Exception as e:
            print(f"Error al actualizar recepcionista: {e}")
            return False
    
    def eliminar_recepcionista(self, cedula):
        """
        Elimina un recepcionista del sistema.
        
        Args:
            cedula (str): Cédula del recepcionista a eliminar
            
        Returns:
            bool: True si se eliminó exitosamente, False en caso contrario
        """
        try:
            recepcionista = Usuario.buscar_por_cedula(cedula)
            if recepcionista and recepcionista.rol == 'recepcionista':
                return recepcionista.eliminar()
            return False
            
        except Exception as e:
            print(f"Error al eliminar recepcionista: {e}")
            return False
    
    def crear_cliente(self, cedula, nombre, apellido, telefono, email, contraseña='cliente123'):
        """
        Crea un nuevo cliente en el sistema.
        
        Args:
            cedula (str): Cédula del cliente
            nombre (str): Nombre del cliente
            apellido (str): Apellido del cliente
            telefono (str): Teléfono del cliente
            email (str): Email del cliente
            contraseña (str): Contraseña del cliente
            
        Returns:
            bool: True si se creó exitosamente, False en caso contrario
        """
        try:
            cliente = Cliente(cedula, nombre, apellido, telefono, email, contraseña)
            return cliente.guardar()
            
        except Exception as e:
            print(f"Error al crear cliente: {e}")
            return False
    
    def obtener_clientes(self):
        """
        Obtiene todos los clientes del sistema.
        
        Returns:
            list: Lista de clientes
        """
        try:
            return Usuario.obtener_todos_por_rol('cliente')
            
        except Exception as e:
            print(f"Error al obtener clientes: {e}")
            return []
    
    def actualizar_cliente(self, cedula, nombre, apellido, telefono, email):
        """
        Actualiza los datos de un cliente.
        
        Args:
            cedula (str): Cédula del cliente
            nombre (str): Nuevo nombre
            apellido (str): Nuevo apellido
            telefono (str): Nuevo teléfono
            email (str): Nuevo email
            
        Returns:
            bool: True si se actualizó exitosamente, False en caso contrario
        """
        try:
            cliente = Usuario.buscar_por_cedula(cedula)
            if cliente and cliente.rol == 'cliente':
                cliente.nombre = nombre
                cliente.apellido = apellido
                cliente.telefono = telefono
                cliente.email = email
                return cliente.actualizar()
            return False
            
        except Exception as e:
            print(f"Error al actualizar cliente: {e}")
            return False
    
    def eliminar_cliente(self, cedula):
        """
        Elimina un cliente del sistema.
        
        Args:
            cedula (str): Cédula del cliente a eliminar
            
        Returns:
            bool: True si se eliminó exitosamente, False en caso contrario
        """
        try:
            cliente = Usuario.buscar_por_cedula(cedula)
            if cliente and cliente.rol == 'cliente':
                return cliente.eliminar()
            return False
            
        except Exception as e:
            print(f"Error al eliminar cliente: {e}")
            return False
    
    def generar_informe_ingresos(self):
        """
        Genera un informe de ingresos basado en las facturas.
        
        Returns:
            dict: Informe con total de ingresos y detalles
        """
        facturas = Factura.obtener_todas()
        total_ingresos = sum(float(f.monto_total) for f in facturas)
        return {
            'total_ingresos': total_ingresos,
            'numero_facturas': len(facturas),
            'facturas': [
                {
                    'fecha': f.fecha,
                    'cliente': f.cliente_cedula,
                    'monto': float(f.monto_total)
                }
                for f in facturas
            ]
        }