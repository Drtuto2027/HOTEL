from modelos.cliente import Cliente
from modelos.habitacion import Habitacion
from modelos.reserva import Reserva
from modelos.usuario import Usuario


class Recepcionista(Usuario):
    """
    Clase Recepcionista que hereda de Usuario.
    
    Funcionalidades específicas:
    - Gestionar clientes (CRUD)
    - Gestionar habitaciones (CRUD)
    - Crear, modificar o cancelar reservas
    - Generar facturas
    """
    
    def __init__(self, cedula, nombre, apellido, telefono, email, contraseña='recep123'):
        """
        Inicializa un recepcionista.
        
        Args:
            cedula (str): Cédula del recepcionista
            nombre (str): Nombre del recepcionista
            apellido (str): Apellido del recepcionista
            telefono (str): Teléfono del recepcionista
            email (str): Email del recepcionista
            contraseña (str): Contraseña del recepcionista
        """
        super().__init__(cedula, nombre, apellido, telefono, email, contraseña, 'recepcionista')
    
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
    
    def crear_habitacion(self, numero, tipo, precio):
        """
        Crea una nueva habitación en el sistema.
        
        Args:
            numero (str): Número de la habitación
            tipo (str): Tipo de habitación (individual, doble, suite)
            precio (float): Precio por noche
            
        Returns:
            bool: True si se creó exitosamente, False en caso contrario
        """
        try:
            habitacion = Habitacion(numero, tipo, precio)
            return habitacion.guardar()
            
        except Exception as e:
            print(f"Error al crear habitación: {e}")
            return False
    
    def obtener_habitaciones(self):
        """
        Obtiene todas las habitaciones del sistema.
        
        Returns:
            list: Lista de habitaciones
        """
        try:
            return Habitacion.obtener_todas()
            
        except Exception as e:
            print(f"Error al obtener habitaciones: {e}")
            return []
    
    def actualizar_habitacion(self, habitacion_id, numero, tipo, precio):
        """
        Actualiza los datos de una habitación.
        
        Args:
            habitacion_id (int): ID de la habitación
            numero (str): Nuevo número
            tipo (str): Nuevo tipo
            precio (float): Nuevo precio
            
        Returns:
            bool: True si se actualizó exitosamente, False en caso contrario
        """
        try:
            habitacion = Habitacion.buscar_por_id(habitacion_id)
            if habitacion:
                habitacion.numero = numero
                habitacion.tipo = tipo
                habitacion.precio = precio
                return habitacion.actualizar()
            return False
            
        except Exception as e:
            print(f"Error al actualizar habitación: {e}")
            return False
    
    def eliminar_habitacion(self, habitacion_id):
        """
        Elimina una habitación del sistema.
        
        Args:
            habitacion_id (int): ID de la habitación a eliminar
            
        Returns:
            bool: True si se eliminó exitosamente, False en caso contrario
        """
        try:
            habitacion = Habitacion.buscar_por_id(habitacion_id)
            if habitacion:
                return habitacion.eliminar()
            return False
            
        except Exception as e:
            print(f"Error al eliminar habitación: {e}")
            return False
    
    def crear_reserva(self, cliente_cedula, habitacion_id, fecha_entrada, fecha_salida):
        """
        Crea una nueva reserva en el sistema.
        
        Args:
            cliente_cedula (str): Cédula del cliente
            habitacion_id (int): ID de la habitación
            fecha_entrada (str): Fecha de entrada
            fecha_salida (str): Fecha de salida
            
        Returns:
            bool: True si se creó exitosamente, False en caso contrario
        """
        reserva = Reserva(cliente_cedula, habitacion_id, fecha_entrada, fecha_salida, estado="pendiente")
        exito = reserva.guardar()
        if exito:
            Habitacion.cambiar_estado(habitacion_id, "ocupada")
        return exito
    
    def obtener_reservas(self):
        """
        Obtiene todas las reservas del sistema.
        
        Returns:
            list: Lista de reservas
        """
        try:
            return Reserva.obtener_todas()
            
        except Exception as e:
            print(f"Error al obtener reservas: {e}")
            return []
    
    def actualizar_reserva(self, reserva_id, cliente_cedula, habitacion_id, fecha_entrada, fecha_salida, estado):
        """
        Actualiza una reserva existente.
        
        Args:
            reserva_id (int): ID de la reserva
            cliente_cedula (str): Cédula del cliente
            habitacion_id (int): ID de la habitación
            fecha_entrada (str): Fecha de entrada
            fecha_salida (str): Fecha de salida
            estado (str): Estado de la reserva
            
        Returns:
            bool: True si se actualizó exitosamente, False en caso contrario
        """
        reserva = Reserva.buscar_por_id(reserva_id)
        if reserva:
            reserva.cliente_cedula = cliente_cedula
            reserva.habitacion_id = habitacion_id
            reserva.fecha_entrada = fecha_entrada
            reserva.fecha_salida = fecha_salida
            reserva.estado = estado
            exito = reserva.actualizar()
            if exito:
                if estado == "confirmada":
                    Habitacion.cambiar_estado(habitacion_id, "ocupada")
                elif estado == "cancelada":
                    Habitacion.cambiar_estado(habitacion_id, "disponible")
            return exito
        return False
    
    def cancelar_reserva(self, reserva_id):
        """
        Cancela una reserva.
        
        Args:
            reserva_id (int): ID de la reserva a cancelar
            
        Returns:
            bool: True si se canceló exitosamente, False en caso contrario
        """
        reserva = Reserva.buscar_por_id(reserva_id)
        if reserva:
            exito = reserva.cancelar()
            if exito:
                Habitacion.cambiar_estado(reserva.habitacion_id, "disponible")
            return exito
        return False