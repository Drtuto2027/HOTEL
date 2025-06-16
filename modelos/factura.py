from modelos.database import db

class Factura:
    """
    Clase Factura para gestionar las facturas del hotel.
    """

    def __init__(self, cliente_cedula, reserva_id, detalles, monto_total, fecha=None, factura_id=None):
        """
        Inicializa una factura.

        Args:
            cliente_cedula (str): Cédula del cliente
            reserva_id (int): ID de la reserva
            detalles (str): Detalles de la factura
            monto_total (float): Monto total de la factura
            fecha (str): Fecha de emisión (opcional)
            factura_id (int): ID de la factura (opcional)
        """
        self.id = factura_id
        self.cliente_cedula = cliente_cedula
        self.reserva_id = reserva_id
        self.detalles = detalles
        self.monto_total = monto_total
        self.fecha = fecha

    def guardar(self):
        """
        Guarda la factura en la base de datos.
        """
        try:
            query = '''
                INSERT INTO facturas (cliente_cedula, reserva_id, detalles, monto_total, fecha)
                VALUES (?, ?, ?, ?, datetime('now'))
            '''
            params = (self.cliente_cedula, self.reserva_id, self.detalles, self.monto_total)
            db.execute_query(query, params)
            return True
        except Exception as e:
            print(f"Error al guardar factura: {e}")
            return False

    @classmethod
    def obtener_por_cliente(cls, cliente_cedula):
        """
        Obtiene todas las facturas de un cliente.
        """
        try:
            query = """
            SELECT f.*, r.estado FROM facturas f
            JOIN reservas r ON f.reserva_id = r.id
            WHERE f.cliente_cedula=?
            """
            result = db.execute_query(query, (cliente_cedula,))
            facturas = []
            for data in result:
                factura = cls(
                    cliente_cedula=data[1],
                    reserva_id=data[2],
                    detalles=data[3],
                    monto_total=data[4],
                    fecha=data[5],
                    factura_id=data[0]
                )
                factura.estado_reserva = data[6]  # estado de la reserva
                facturas.append(factura)
            return facturas
        except Exception as e:
            print(f"Error al obtener facturas por cliente: {e}")
            return []

    @classmethod
    def obtener_todas(cls):
        """
        Obtiene todas las facturas del sistema.
        """
        try:
            query = 'SELECT * FROM facturas ORDER BY fecha DESC'
            results = db.execute_query(query)
            facturas = []
            for data in results:
                factura = cls(
                    cliente_cedula=data[1],
                    reserva_id=data[2],
                    detalles=data[3],
                    monto_total=data[4],
                    fecha=data[5],
                    factura_id=data[0]
                )
                facturas.append(factura)
            return facturas
        except Exception as e:
            print(f"Error al obtener facturas: {e}")
            return []

    @classmethod
    def existe_para_reserva(cls, reserva_id):
        """
        Verifica si existe una factura para una reserva dada.

        Args:
            reserva_id (int): ID de la reserva

        Returns:
            bool: True si existe una factura para la reserva, False en caso contrario
        """
        query = "SELECT COUNT(*) FROM facturas WHERE reserva_id=?"
        result = db.execute_query(query, (reserva_id,))
        return result and result[0][0] > 0

    @classmethod
    def buscar_por_reserva(cls, reserva_id):
        """
        Busca una factura por el ID de la reserva.

        Args:
            reserva_id (int): ID de la reserva

        Returns:
            Factura: Objeto factura correspondiente a la reserva, o None si no existe
        """
        query = "SELECT * FROM facturas WHERE reserva_id=?"
        result = db.execute_query(query, (reserva_id,))
        if result:
            data = result[0]
            return cls(
                cliente_cedula=data[1],
                reserva_id=data[2],
                detalles=data[3],
                monto_total=data[4],
                fecha=data[5],
                factura_id=data[0]
            )
        return None

    @classmethod
    def buscar_por_id(cls, factura_id):
        """
        Busca una factura por su ID.

        Args:
            factura_id (int): ID de la factura

        Returns:
            Factura: Objeto factura correspondiente a la ID, o None si no existe
        """
        query = "SELECT * FROM facturas WHERE id=?"
        result = db.execute_query(query, (factura_id,))
        if result:
            data = result[0]
            return cls(
                cliente_cedula=data[1],
                reserva_id=data[2],
                detalles=data[3],
                monto_total=data[4],
                fecha=data[5],
                factura_id=data[0]
            )
        return None

    def __str__(self):
        return f"Factura {self.id}: Cliente {self.cliente_cedula}, Reserva {self.reserva_id}, Monto: {self.monto_total}, Fecha: {self.fecha}"

    def to_dict(self):
        return {
            'id': self.id,
            'cliente_cedula': self.cliente_cedula,
            'reserva_id': self.reserva_id,
            'detalles': self.detalles,
            'monto_total': self.monto_total,
            'fecha': self.fecha
        }