from modelos.administrador import Administrador

class AdminControlador:
    def __init__(self, admin: Administrador = None):
        self.admin = admin

    def crear_recepcionista(self, *args, **kwargs):
        return self.admin.crear_recepcionista(*args, **kwargs)

    def obtener_recepcionistas(self):
        return self.admin.obtener_recepcionistas()

    def actualizar_recepcionista(self, *args, **kwargs):
        return self.admin.actualizar_recepcionista(*args, **kwargs)

    def eliminar_recepcionista(self, cedula):
        return self.admin.eliminar_recepcionista(cedula)

    def crear_cliente(self, *args, **kwargs):
        return self.admin.crear_cliente(*args, **kwargs)

    def obtener_clientes(self):
        return self.admin.obtener_clientes()

    def actualizar_cliente(self, *args, **kwargs):
        return self.admin.actualizar_cliente(*args, **kwargs)

    def eliminar_cliente(self, cedula):
        return self.admin.eliminar_cliente(cedula)

    def generar_informe_ingresos(self):
        return self.admin.generar_informe_ingresos()

    def crear_administrador(self, cedula, nombre, apellido, telefono, email, contraseña='admin123'):
        admin = Administrador(cedula, nombre, apellido, telefono, email, contraseña)
        return admin.guardar()