from modelos.factura import Factura
from modelos.habitacion import Habitacion
from modelos.reserva import Reserva
from modelos.usuario import Usuario

class Cliente(Usuario):
    """
    Clase Cliente que hereda de Usuario.
    
    Funcionalidades específicas:
    - Consultar habitaciones disponibles
    - Realizar reservas
    - Realizar pagos de reservas
    - Cancelar reservas
    """
    
    def __init__(self, cedula, nombre, apellido, telefono, email, contraseña='cliente123'):
        """
        Inicializa un cliente.
        
        Args:
            cedula (str): Cédula del cliente
            nombre (str): Nombre del cliente
            apellido (str): Apellido del cliente
            telefono (str): Teléfono del cliente
            email (str): Email del cliente
            contraseña (str): Contraseña del cliente
        """
        super().__init__(cedula, nombre, apellido, telefono, email, contraseña, 'cliente')
    
    def consultar_habitaciones_disponibles(self):
        """
        Consulta las habitaciones disponibles en el hotel.
        
        Returns:
            list: Lista de habitaciones disponibles
        """
        try:
            return Habitacion.obtener_disponibles()
            
        except Exception as e:
            print(f"Error al consultar habitaciones disponibles: {e}")
            return []
    
    def realizar_reserva(self, habitacion_id, fecha_entrada, fecha_salida):
        """
        Realiza una reserva en una habitación disponible.
        
        Args:
            habitacion_id (int): ID de la habitación
            fecha_entrada (str): Fecha de entrada
            fecha_salida (str): Fecha de salida
            
        Returns:
            bool: True si se realizó exitosamente, False en caso contrario
        """
        reserva = Reserva(self.cedula, habitacion_id, fecha_entrada, fecha_salida, estado="pendiente")
        exito = reserva.guardar()
        if exito:
            Habitacion.cambiar_estado(habitacion_id, "ocupada")
        return exito
    
    def obtener_mis_reservas(self):
        """
        Obtiene todas las reservas del cliente.
        
        Returns:
            list: Lista de reservas del cliente
        """
        try:
            return Reserva.obtener_por_cliente(self.cedula)
            
        except Exception as e:
            print(f"Error al obtener reservas: {e}")
            return []
    
    def realizar_pago_reserva(self, reserva_id):
        """
        Realiza el pago de una reserva, confirmándola.
        
        Args:
            reserva_id (int): ID de la reserva a pagar
            
        Returns:
            bool: True si se realizó el pago exitosamente, False en caso contrario
        """
        try:
            reserva = Reserva.buscar_por_id(reserva_id)
            
            if reserva and reserva.cliente_cedula == self.cedula:
                return reserva.confirmar_pago()
            
            return False
            
        except Exception as e:
            print(f"Error al realizar pago: {e}")
            return False
    
    def cancelar_reserva(self, reserva_id):
        """
        Cancela una reserva del cliente.
        
        Args:
            reserva_id (int): ID de la reserva a cancelar
            
        Returns:
            bool: True si se canceló exitosamente, False en caso contrario
        """
        reserva = Reserva.buscar_por_id(reserva_id)
        if reserva and reserva.estado != "cancelada":
            exito = reserva.cancelar()
            if exito:
                Habitacion.cambiar_estado(reserva.habitacion_id, "disponible")
            return exito
        return False
    
    def obtener_facturas(self):
        """
        Obtiene todas las facturas del cliente.
        
        Returns:
            list: Lista de facturas del cliente
        """
        try:
            return Factura.obtener_por_cliente(self.cedula)
            
        except Exception as e:
            print(f"Error al obtener facturas: {e}")
            return []