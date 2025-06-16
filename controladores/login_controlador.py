from modelos.usuario import Usuario
from modelos.administrador import Administrador
from modelos.recepcionista import Recepcionista
from modelos.cliente import Cliente

class LoginControlador:
    @staticmethod
    def login(cedula, contraseña):
        usuario = Usuario.validar_login(cedula, contraseña)
        if usuario:
            if usuario.rol == "administrador":
                return Administrador(usuario.cedula, usuario.nombre, usuario.apellido, usuario.telefono, usuario.email, usuario.contraseña)
            elif usuario.rol == "recepcionista":
                return Recepcionista(usuario.cedula, usuario.nombre, usuario.apellido, usuario.telefono, usuario.email, usuario.contraseña)
            elif usuario.rol == "cliente":
                return Cliente(usuario.cedula, usuario.nombre, usuario.apellido, usuario.telefono, usuario.email, usuario.contraseña)
        return None