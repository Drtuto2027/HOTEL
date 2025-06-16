from modelos.recepcionista import Recepcionista

class RecepcionistaControlador:
    def __init__(self, recepcionista: Recepcionista):
        self.recepcionista = recepcionista

    # Clientes
    def crear_cliente(self, *args, **kwargs):
        return self.recepcionista.crear_cliente(*args, **kwargs)

    def obtener_clientes(self):
        return self.recepcionista.obtener_clientes()

    def actualizar_cliente(self, *args, **kwargs):
        return self.recepcionista.actualizar_cliente(*args, **kwargs)

    def eliminar_cliente(self, cedula):
        return self.recepcionista.eliminar_cliente(cedula)

    # Habitaciones
    def crear_habitacion(self, *args, **kwargs):
        return self.recepcionista.crear_habitacion(*args, **kwargs)

    def obtener_habitaciones(self):
        return self.recepcionista.obtener_habitaciones()

    def actualizar_habitacion(self, *args, **kwargs):
        return self.recepcionista.actualizar_habitacion(*args, **kwargs)

    def eliminar_habitacion(self, habitacion_id):
        return self.recepcionista.eliminar_habitacion(habitacion_id)

    # Reservas
    def crear_reserva(self, *args, **kwargs):
        return self.recepcionista.crear_reserva(*args, **kwargs)

    def obtener_reservas(self):
        return self.recepcionista.obtener_reservas()

    def actualizar_reserva(self, *args, **kwargs):
        return self.recepcionista.actualizar_reserva(*args, **kwargs)

    def cancelar_reserva(self, reserva_id):
        return self.recepcionista.cancelar_reserva(reserva_id)