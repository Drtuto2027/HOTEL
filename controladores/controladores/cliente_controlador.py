from modelos.cliente import Cliente
from modelos.reserva import Reserva

class ClienteControlador:
    def __init__(self, cliente: Cliente):
        self.cliente = cliente

    def consultar_habitaciones_disponibles(self):
        return self.cliente.consultar_habitaciones_disponibles()

    def realizar_reserva(self, habitacion_id, fecha_entrada, fecha_salida):
        return self.cliente.realizar_reserva(habitacion_id, fecha_entrada, fecha_salida)

    def obtener_mis_reservas(self):
        return self.cliente.obtener_mis_reservas()

    def realizar_pago_reserva(self, reserva_id):
        return self.cliente.realizar_pago_reserva(reserva_id)

    def cancelar_reserva(self, reserva_id):
        return self.cliente.cancelar_reserva(reserva_id)

    def obtener_facturas(self):
        return self.cliente.obtener_facturas()

    def obtener_estado_reserva(self, reserva_id):
        reserva = Reserva.buscar_por_id(reserva_id)
        return reserva.estado if reserva else "No se encuentra"

    def pagar_factura(self, factura_id, reserva_id):
        reserva = Reserva.buscar_por_id(reserva_id)
        if reserva and reserva.estado != "confirmada":
            return reserva.confirmar_pago()
        return False