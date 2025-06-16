from modelos.database import db
from modelos.factura import Factura
from modelos.habitacion import Habitacion

class Reserva:
    """
    Clase Reserva para gestionar las reservas del hotel.
    """

    def __init__(self, cliente_cedula, habitacion_id, fecha_entrada, fecha_salida, estado='pendiente', reserva_id=None):
        """
        Inicializa una reserva.

        Args:
            cliente_cedula (str): Cédula del cliente
            habitacion_id (int): ID de la habitación
            fecha_entrada (str): Fecha de entrada
            fecha_salida (str): Fecha de salida
            estado (str): Estado de la reserva (pendiente, confirmada, cancelada)
            reserva_id (int): ID de la reserva (opcional)
        """
        self.id = reserva_id
        self.cliente_cedula = cliente_cedula
        self.habitacion_id = habitacion_id
        self.fecha_entrada = fecha_entrada
        self.fecha_salida = fecha_salida
        self.estado = estado

    def guardar(self):
        """
        Guarda la reserva en la base de datos.
        """
        try:
            query = "INSERT INTO reservas (cliente_cedula, habitacion_id, fecha_entrada, fecha_salida, estado) VALUES (?, ?, ?, ?, ?)"
            db.execute_query(query, (self.cliente_cedula, self.habitacion_id, self.fecha_entrada, self.fecha_salida, self.estado))
            query_id = "SELECT id FROM reservas WHERE cliente_cedula=? AND habitacion_id=? AND fecha_entrada=? AND fecha_salida=? ORDER BY id DESC LIMIT 1"
            result = db.execute_query(query_id, (self.cliente_cedula, self.habitacion_id, self.fecha_entrada, self.fecha_salida))
            if result:
                reserva_id = result[0][0]
                              
                detalles = f"Reserva pendiente del {self.fecha_entrada} al {self.fecha_salida}"
                monto_total = Habitacion.obtener_precio_por_id(self.habitacion_id)
                factura = Factura(self.cliente_cedula, reserva_id, detalles, monto_total)
                factura.guardar()
            return True
        except Exception as e:
            print(f"Error al guardar reserva: {e}")
            return False

    def actualizar(self):
        """
        Actualiza los datos de la reserva en la base de datos.
        """
        try:
            query = '''
                UPDATE reservas
                SET cliente_cedula=?, habitacion_id=?, fecha_entrada=?, fecha_salida=?, estado=?
                WHERE id=?
            '''
            params = (self.cliente_cedula, self.habitacion_id, self.fecha_entrada, self.fecha_salida, self.estado, self.id)
            result = db.execute_query(query, params)
            return result > 0
        except Exception as e:
            print(f"Error al actualizar reserva: {e}")
            return False

    def cancelar(self):
        """
        Cancela la reserva.
        """
        try:
            query = "UPDATE reservas SET estado='cancelada' WHERE id=?"
            db.execute_query(query, (self.id,))
            self.estado = "cancelada"
            return True
        except Exception as e:
            print(f"Error al cancelar reserva: {e}")
            return False

    def confirmar_pago(self):
        """
        Confirma el pago de la reserva.
        """
        try:
            query = "UPDATE reservas SET estado='confirmada' WHERE id=?"
            db.execute_query(query, (self.id,))
            self.estado = "confirmada"
            return True
        except Exception as e:
            print(f"Error al confirmar pago de reserva: {e}")
            return False

    @classmethod
    def buscar_por_id(cls, reserva_id):
        """
        Busca una reserva por su ID.
        """
        try:
            query = "SELECT * FROM reservas WHERE id=?"
            result = db.execute_query(query, (reserva_id,))
            if result:
                data = result[0]
                return cls(
                    cliente_cedula=data[1],
                    habitacion_id=data[2],
                    fecha_entrada=data[3],
                    fecha_salida=data[4],
                    estado=data[5],
                    reserva_id=data[0]
                )
            return None
        except Exception as e:
            print(f"Error al buscar reserva: {e}")
            return None

    @classmethod
    def obtener_todas(cls):
        """
        Obtiene todas las reservas del sistema.
        """
        try:
            query = 'SELECT * FROM reservas ORDER BY fecha_entrada DESC'
            results = db.execute_query(query)
            reservas = []
            for data in results:
                reserva = cls(
                    cliente_cedula=data[1],
                    habitacion_id=data[2],
                    fecha_entrada=data[3],
                    fecha_salida=data[4],
                    estado=data[5],
                    reserva_id=data[0]
                )
                reservas.append(reserva)
            return reservas
        except Exception as e:
            print(f"Error al obtener reservas: {e}")
            return []

    @classmethod
    def obtener_por_cliente(cls, cliente_cedula):
        """
        Obtiene todas las reservas de un cliente.
        """
        try:
            query = 'SELECT * FROM reservas WHERE cliente_cedula=? ORDER BY fecha_entrada DESC'
            results = db.execute_query(query, (cliente_cedula,))
            reservas = []
            for data in results:
                reserva = cls(
                    cliente_cedula=data[1],
                    habitacion_id=data[2],
                    fecha_entrada=data[3],
                    fecha_salida=data[4],
                    estado=data[5],
                    reserva_id=data[0]
                )
                reservas.append(reserva)
            return reservas
        except Exception as e:
            print(f"Error al obtener reservas por cliente: {e}")
            return []

    def __str__(self):
        return f"Reserva {self.id}: Cliente {self.cliente_cedula}, Habitación {self.habitacion_id}, {self.fecha_entrada} a {self.fecha_salida}, Estado: {self.estado}"

    def to_dict(self):
        return {
            'id': self.id,
            'cliente_cedula': self.cliente_cedula,
            'habitacion_id': self.habitacion_id,
            'fecha_entrada': self.fecha_entrada,
            'fecha_salida': self.fecha_salida,
            'estado': self.estado
        }