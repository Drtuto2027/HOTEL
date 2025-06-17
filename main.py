import tkinter as tk
from controladores.login_controlador import LoginControlador
from controladores.admin_controlador import AdminControlador
from controladores.recepcionista_controlador import RecepcionistaControlador
from controladores.cliente_controlador import ClienteControlador
from vistas.login_vista import LoginVista
from vistas.admin_vista import AdminVista
from vistas.recepcionista_vista import RecepcionistaVista
from vistas.cliente_vista import ClienteVista

def abrir_vista_por_rol(usuario):
    def volver_a_login():
        main()  # Reinicia el flujo de login

    if usuario.rol == "administrador":
        admin_controlador = AdminControlador(usuario)
        AdminVista(admin_controlador, volver_a_login)
    elif usuario.rol == "recepcionista":
        recep_controlador = RecepcionistaControlador(usuario)
        RecepcionistaVista(recep_controlador, volver_a_login)
    elif usuario.rol == "cliente":
        cliente_controlador = ClienteControlador(usuario)
        ClienteVista(cliente_controlador, volver_a_login)
    else:
        tk.messagebox.showerror("Error", "Rol de usuario desconocido.")

def main():
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal

    login_controlador = LoginControlador()

    def on_login_success(usuario):
        abrir_vista_por_rol(usuario)

    # Pasa el callback a la vista de login
    login_vista = LoginVista(login_controlador, on_login_success)
    login_vista.mainloop()

