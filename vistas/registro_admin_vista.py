import tkinter as tk
from tkinter import messagebox

class RegistroAdminVista(tk.Toplevel):
    def __init__(self, admin_controlador):
        super().__init__()
        self.title("Registro de Administrador")
        self.geometry("350x350")
        self.admin_controlador = admin_controlador

        tk.Label(self, text="Nombres*:").pack()
        self.entry_nombre = tk.Entry(self)
        self.entry_nombre.pack()
        tk.Label(self, text="Apellidos*:").pack()
        self.entry_apellido = tk.Entry(self)
        self.entry_apellido.pack()
        tk.Label(self, text="Cédula*:").pack()
        self.entry_cedula = tk.Entry(self)
        self.entry_cedula.pack()
        tk.Label(self, text="Email*:").pack()
        self.entry_email = tk.Entry(self)
        self.entry_email.pack()
        tk.Label(self, text="Teléfono:").pack()
        self.entry_telefono = tk.Entry(self)
        self.entry_telefono.pack()
        tk.Label(self, text="Password*:").pack()
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.pack()

        tk.Button(self, text="Registrar", command=self.registrar).pack(pady=10)
        tk.Button(self, text="Limpiar", command=self.limpiar).pack()
        tk.Button(self, text="Salir", command=self.destroy).pack(pady=5)

    def limpiar(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_apellido.delete(0, tk.END)
        self.entry_cedula.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)

    def registrar(self):
        nombre = self.entry_nombre.get()
        apellido = self.entry_apellido.get()
        cedula = self.entry_cedula.get()
        email = self.entry_email.get()
        telefono = self.entry_telefono.get()
        password = self.entry_password.get()
        if not all([nombre, apellido, cedula, email, password]):
            messagebox.showerror("Error", "Todos los campos marcados con * son obligatorios")
            return
        exito = self.admin_controlador.crear_administrador(
            cedula, nombre, apellido, telefono, email, password
        )
        if exito:
            messagebox.showinfo("Éxito", "Administrador registrado correctamente")
            self.destroy()
        else:
            messagebox.showerror("Error", "No se pudo registrar el administrador")