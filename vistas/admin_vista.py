import tkinter as tk
from tkinter import messagebox, ttk
import os
from vistas.informe_vista import InformeVista

class AdminVista(tk.Toplevel):
    def __init__(self, admin_controlador, on_logout):
        super().__init__()
        self.title("Panel Administrador")
        self.geometry("600x400")
        self.admin_controlador = admin_controlador
        self.on_logout = on_logout

        # Intentar cargar el icono
        try:
            if os.path.exists("iconos/admin.ico"):
                self.iconbitmap("iconos/admin.ico")
        except Exception as e:
            print(f"Advertencia: No se pudo cargar el icono de la ventana. {e}")

        # Barra de menú con hotkeys
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        archivo_menu = tk.Menu(menubar, tearoff=0)
        archivo_menu.add_command(label="Cerrar sesión", accelerator="Ctrl+L", command=self.cerrar_sesion)
        archivo_menu.add_command(label="Salir", accelerator="Ctrl+Q", command=self.destroy)
        menubar.add_cascade(label="Archivo", menu=archivo_menu)
        self.bind_all("<Control-q>", lambda e: self.destroy())
        self.bind_all("<Control-l>", lambda e: self.cerrar_sesion())

        # Botón de cerrar sesión
        btn_logout = tk.Button(self, text="Cerrar sesión", command=self.cerrar_sesion)
        btn_logout.pack(side="bottom", pady=10)

        # Pestañas para gestión
        tabs = ttk.Notebook(self)
        tabs.pack(fill="both", expand=True)

        # Recepcionistas
        frame_recep = ttk.Frame(tabs)
        tabs.add(frame_recep, text="Recepcionistas")
        ttk.Button(frame_recep, text="Agregar Recepcionista", command=self.agregar_recepcionista).pack(pady=5)
        self.tree_recep = ttk.Treeview(frame_recep, columns=("cedula", "nombre", "apellido", "email"), show="headings")
        for col in self.tree_recep["columns"]:
            self.tree_recep.heading(col, text=col.capitalize())
        self.tree_recep.pack(fill="both", expand=True)
        self.tree_recep.tooltip = "Lista de recepcionistas"

        # Clientes
        frame_cli = ttk.Frame(tabs)
        tabs.add(frame_cli, text="Clientes")
        ttk.Button(frame_cli, text="Agregar Cliente", command=self.agregar_cliente).pack(pady=5)
        self.tree_cli = ttk.Treeview(frame_cli, columns=("cedula", "nombre", "apellido", "email"), show="headings")
        for col in self.tree_cli["columns"]:
            self.tree_cli.heading(col, text=col.capitalize())
        self.tree_cli.pack(fill="both", expand=True)
        self.tree_cli.tooltip = "Lista de clientes"

        # Informe de ingresos
        frame_inf = ttk.Frame(tabs)
        tabs.add(frame_inf, text="Informe de Ingresos")
        ttk.Button(frame_inf, text="Generar Informe", command=self.generar_informe).pack(pady=5)
        self.text_inf = tk.Text(frame_inf, height=10)
        self.text_inf.pack(fill="both", expand=True)

        self.cargar_listas()

    def cargar_listas(self):
        try:
            # Recepcionistas
            for i in self.tree_recep.get_children():
                self.tree_recep.delete(i)
            for r in self.admin_controlador.obtener_recepcionistas():
                self.tree_recep.insert("", "end", values=(r.cedula, r.nombre, r.apellido, r.email))
            # Clientes
            for i in self.tree_cli.get_children():
                self.tree_cli.delete(i)
            for c in self.admin_controlador.obtener_clientes():
                self.tree_cli.insert("", "end", values=(c.cedula, c.nombre, c.apellido, c.email))
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar listas: {e}")

    def agregar_recepcionista(self):
        def guardar():
            cedula = entry_cedula.get()
            nombre = entry_nombre.get()
            apellido = entry_apellido.get()
            telefono = entry_telefono.get()
            email = entry_email.get()
            contraseña = entry_contraseña.get()
            if not all([cedula, nombre, apellido, telefono, email, contraseña]):
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            exito = self.admin_controlador.crear_recepcionista(
                cedula, nombre, apellido, telefono, email, contraseña
            )
            if exito:
                messagebox.showinfo("Éxito", "Recepcionista agregado correctamente")
                top.destroy()
                self.cargar_listas()
            else:
                messagebox.showerror("Error", "No se pudo agregar el recepcionista")

        top = tk.Toplevel(self)
        top.title("Agregar Recepcionista")
        top.geometry("300x350")
        tk.Label(top, text="Cédula:").pack()
        entry_cedula = tk.Entry(top)
        entry_cedula.pack()
        tk.Label(top, text="Nombre:").pack()
        entry_nombre = tk.Entry(top)
        entry_nombre.pack()
        tk.Label(top, text="Apellido:").pack()
        entry_apellido = tk.Entry(top)
        entry_apellido.pack()
        tk.Label(top, text="Teléfono:").pack()
        entry_telefono = tk.Entry(top)
        entry_telefono.pack()
        tk.Label(top, text="Email:").pack()
        entry_email = tk.Entry(top)
        entry_email.pack()
        tk.Label(top, text="Contraseña:").pack()
        entry_contraseña = tk.Entry(top, show="*")
        entry_contraseña.pack()
        tk.Button(top, text="Guardar", command=guardar).pack(pady=10)

    def agregar_cliente(self):
        def guardar():
            cedula = entry_cedula.get()
            nombre = entry_nombre.get()
            apellido = entry_apellido.get()
            telefono = entry_telefono.get()
            email = entry_email.get()
            contraseña = entry_contraseña.get()
            if not all([cedula, nombre, apellido, telefono, email, contraseña]):
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            exito = self.admin_controlador.crear_cliente(
                cedula, nombre, apellido, telefono, email, contraseña
            )
            if exito:
                messagebox.showinfo("Éxito", "Cliente agregado correctamente")
                top.destroy()
                self.cargar_listas()
            else:
                messagebox.showerror("Error", "No se pudo agregar el cliente")

        top = tk.Toplevel(self)
        top.title("Agregar Cliente")
        top.geometry("300x350")
        tk.Label(top, text="Cédula:").pack()
        entry_cedula = tk.Entry(top)
        entry_cedula.pack()
        tk.Label(top, text="Nombre:").pack()
        entry_nombre = tk.Entry(top)
        entry_nombre.pack()
        tk.Label(top, text="Apellido:").pack()
        entry_apellido = tk.Entry(top)
        entry_apellido.pack()
        tk.Label(top, text="Teléfono:").pack()
        entry_telefono = tk.Entry(top)
        entry_telefono.pack()
        tk.Label(top, text="Email:").pack()
        entry_email = tk.Entry(top)
        entry_email.pack()
        tk.Label(top, text="Contraseña:").pack()
        entry_contraseña = tk.Entry(top, show="*")
        entry_contraseña.pack()
        tk.Button(top, text="Guardar", command=guardar).pack(pady=10)

    def generar_informe(self):
        try:
            informe = self.admin_controlador.generar_informe_ingresos()
            InformeVista(informe)  # Muestra el informe estilizado
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar informe: {e}")

    def cerrar_sesion(self):
        self.destroy()
        self.on_logout()