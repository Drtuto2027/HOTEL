import tkinter as tk
from tkinter import messagebox, ttk
import os
from modelos.habitacion import Habitacion
from modelos.reserva import Reserva
from modelos.factura import Factura

class RecepcionistaVista(tk.Toplevel):
    def __init__(self, recep_controlador, on_logout):
        super().__init__()
        self.title("Panel Recepcionista")
        self.geometry("700x500")
        self.recep_controlador = recep_controlador
        self.on_logout = on_logout

        # Intentar cargar el icono
        try:
            if os.path.exists("iconos/recep.ico"):
                self.iconbitmap("iconos/recep.ico")
        except Exception as e:
            print(f"Advertencia: No se pudo cargar el icono de la ventana. {e}")

        # Barra de menú
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        archivo_menu = tk.Menu(menubar, tearoff=0)
        archivo_menu.add_command(label="Cerrar sesión", accelerator="Ctrl+L", command=self.cerrar_sesion)
        archivo_menu.add_command(label="Salir", accelerator="Ctrl+Q", command=self.destroy)
        menubar.add_cascade(label="Archivo", menu=archivo_menu)
        self.bind_all("<Control-q>", lambda e: self.destroy())
        self.bind_all("<Control-l>", lambda e: self.cerrar_sesion())

        # Pestañas
        tabs = ttk.Notebook(self)
        tabs.pack(fill="both", expand=True)

        # Clientes
        frame_cli = ttk.Frame(tabs)
        tabs.add(frame_cli, text="Clientes")
        ttk.Button(frame_cli, text="Agregar Cliente", command=self.agregar_cliente).pack(pady=5)
        self.tree_cli = ttk.Treeview(frame_cli, columns=("cedula", "nombre", "apellido", "email"), show="headings")
        for col in self.tree_cli["columns"]:
            self.tree_cli.heading(col, text=col.capitalize())
        self.tree_cli.pack(fill="both", expand=True)

        # Habitaciones
        frame_hab = ttk.Frame(tabs)
        tabs.add(frame_hab, text="Habitaciones")
        ttk.Button(frame_hab, text="Agregar Habitación", command=self.agregar_habitacion).pack(pady=5)
        self.tree_hab = ttk.Treeview(frame_hab, columns=("id", "numero", "tipo", "precio", "estado"), show="headings")
        for col in self.tree_hab["columns"]:
            self.tree_hab.heading(col, text=col.capitalize())
        self.tree_hab.pack(fill="both", expand=True)

        # Reservas
        frame_res = ttk.Frame(tabs)
        tabs.add(frame_res, text="Reservas")
        ttk.Button(frame_res, text="Crear Reserva", command=self.crear_reserva).pack(padx=5, pady=5)
        ttk.Button(frame_res, text="Modificar Reserva", command=self.modificar_reserva).pack(padx=5, pady=5)
        ttk.Button(frame_res, text="Ver Factura", command=self.ver_factura).pack(padx=5, pady=5)
        self.tree_res = ttk.Treeview(frame_res, columns=("id", "cliente", "habitacion", "entrada", "salida", "estado"), show="headings")
        for col in self.tree_res["columns"]:
            self.tree_res.heading(col, text=col.capitalize())
        self.tree_res.pack(fill="both", expand=True)

        # Botón de cerrar sesión
        btn_logout = tk.Button(self, text="Cerrar sesión", command=self.cerrar_sesion)
        btn_logout.pack(side="bottom", pady=10)

        self.cargar_listas()

    def cargar_listas(self):
        try:
            # Clientes
            for i in self.tree_cli.get_children():
                self.tree_cli.delete(i)
            for c in self.recep_controlador.obtener_clientes():
                self.tree_cli.insert("", "end", values=(c.cedula, c.nombre, c.apellido, c.email))
            # Habitaciones
            for i in self.tree_hab.get_children():
                self.tree_hab.delete(i)
            for h in self.recep_controlador.obtener_habitaciones():
                self.tree_hab.insert("", "end", values=(h.id, h.numero, h.tipo, h.precio, h.estado))
            # Reservas
            for i in self.tree_res.get_children():
                self.tree_res.delete(i)
            for r in self.recep_controlador.obtener_reservas():
                self.tree_res.insert("", "end", values=(r.id, r.cliente_cedula, r.habitacion_id, r.fecha_entrada, r.fecha_salida, r.estado))
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar listas: {e}")

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
            exito = self.recep_controlador.crear_cliente(
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

    def agregar_habitacion(self):
        def guardar():
            numero = entry_numero.get()
            tipo = entry_tipo.get()
            precio = entry_precio.get()
            if not all([numero, tipo, precio]):
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            try:
                precio = float(precio)
            except ValueError:
                messagebox.showerror("Error", "El precio debe ser un número")
                return
            exito = self.recep_controlador.crear_habitacion(
                numero, tipo, precio
            )
            if exito:
                messagebox.showinfo("Éxito", "Habitación agregada correctamente")
                top.destroy()
                self.cargar_listas()
            else:
                messagebox.showerror("Error", "No se pudo agregar la habitación")

        top = tk.Toplevel(self)
        top.title("Agregar Habitación")
        top.geometry("300x250")
        tk.Label(top, text="Número:").pack()
        entry_numero = tk.Entry(top)
        entry_numero.pack()
        tk.Label(top, text="Tipo (individual/doble/suite):").pack()
        entry_tipo = tk.Entry(top)
        entry_tipo.pack()
        tk.Label(top, text="Precio:").pack()
        entry_precio = tk.Entry(top)
        entry_precio.pack()
        tk.Button(top, text="Guardar", command=guardar).pack(pady=10)

    def crear_reserva(self):
        def guardar():
            cedula_cliente = entry_cedula_cliente.get()
            numero_habitacion = entry_numero_habitacion.get()
            fecha_inicio = entry_fecha_inicio.get()
            fecha_fin = entry_fecha_fin.get()
            if not all([cedula_cliente, numero_habitacion, fecha_inicio, fecha_fin]):
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            # Buscar el ID de la habitación por su número
            habitacion = Habitacion.buscar_por_numero(numero_habitacion)
            if not habitacion:
                messagebox.showerror("Error", "No existe una habitación con ese número")
                return
            exito = self.recep_controlador.crear_reserva(
                cedula_cliente, habitacion.id, fecha_inicio, fecha_fin
            )
            if exito:
                messagebox.showinfo("Éxito", "Reserva creada correctamente")
                top.destroy()
                self.cargar_listas()
            else:
                messagebox.showerror("Error", "No se pudo crear la reserva")

        top = tk.Toplevel(self)
        top.title("Crear Reserva")
        top.geometry("300x300")
        tk.Label(top, text="Cédula Cliente:").pack()
        entry_cedula_cliente = tk.Entry(top)
        entry_cedula_cliente.pack()
        tk.Label(top, text="Número Habitación:").pack()
        entry_numero_habitacion = tk.Entry(top)
        entry_numero_habitacion.pack()
        tk.Label(top, text="Fecha Inicio (YYYY-MM-DD):").pack()
        entry_fecha_inicio = tk.Entry(top)
        entry_fecha_inicio.pack()
        tk.Label(top, text="Fecha Fin (YYYY-MM-DD):").pack()
        entry_fecha_fin = tk.Entry(top)
        entry_fecha_fin.pack()
        tk.Button(top, text="Guardar", command=guardar).pack(pady=10)

    def modificar_reserva(self):
        selected = self.tree_res.selection()
        if not selected:
            messagebox.showerror("Error", "Selecciona una reserva para modificar")
            return
        reserva = self.tree_res.item(selected[0])["values"]
        reserva_id = reserva[0]
        cliente_cedula = reserva[1]
        habitacion_id = reserva[2]  # Este debe ser el ID de la habitación

        def guardar():
            fecha_entrada = entry_fecha_entrada.get()
            fecha_salida = entry_fecha_salida.get()
            estado = estado_var.get()
            if not all([fecha_entrada, fecha_salida, estado]):
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            exito = self.recep_controlador.actualizar_reserva(
                reserva_id, cliente_cedula, habitacion_id, fecha_entrada, fecha_salida, estado
            )
            if exito:
                messagebox.showinfo("Éxito", "Reserva modificada correctamente")
                top.destroy()
                self.cargar_listas()
            else:
                messagebox.showerror("Error", "No se pudo modificar la reserva")

        top = tk.Toplevel(self)
        top.title("Modificar Reserva")
        top.geometry("300x250")
        tk.Label(top, text="Fecha Entrada (YYYY-MM-DD):").pack()
        entry_fecha_entrada = tk.Entry(top)
        entry_fecha_entrada.insert(0, reserva[3])
        entry_fecha_entrada.pack()
        tk.Label(top, text="Fecha Salida (YYYY-MM-DD):").pack()
        entry_fecha_salida = tk.Entry(top)
        entry_fecha_salida.insert(0, reserva[4])
        entry_fecha_salida.pack()
        tk.Label(top, text="Estado:").pack()
        estado_var = tk.StringVar(value=reserva[5])
        estado_menu = tk.OptionMenu(top, estado_var, "pendiente", "confirmada", "cancelada")
        estado_menu.pack()
        tk.Button(top, text="Guardar", command=guardar).pack(pady=10)

    def cerrar_sesion(self):
        self.destroy()
        self.on_logout()

    def actualizar_reserva(self, reserva_id, cliente_cedula, habitacion_id, fecha_entrada, fecha_salida, estado):
        
        exito = Reserva(...).actualizar()
        if exito and estado == "confirmada":
            Habitacion.cambiar_estado(habitacion_id, "ocupada")
        return exito

    def ver_factura(self):
        selected = self.tree_res.selection()
        if not selected:
            messagebox.showerror("Error", "Selecciona una reserva para ver la factura")
            return
        reserva = self.tree_res.item(selected[0])["values"]
        reserva_id = reserva[0]

        factura = Factura.buscar_por_reserva(reserva_id)
        if not factura:
            messagebox.showinfo("Factura", "No existe factura para esta reserva")
            return

        # Muestra los datos de la factura en una ventana emergente
        top = tk.Toplevel(self)
        top.title("Factura")
        top.geometry("350x250")
        tk.Label(top, text=f"Factura ID: {factura.id}").pack()
        tk.Label(top, text=f"Cliente: {factura.cliente_cedula}").pack()
        tk.Label(top, text=f"Reserva ID: {factura.reserva_id}").pack()
        tk.Label(top, text=f"Detalles: {factura.detalles}").pack()
        tk.Label(top, text=f"Monto Total: {factura.monto_total}").pack()
        tk.Label(top, text=f"Fecha: {factura.fecha}").pack()
        tk.Button(top, text="Cerrar", command=top.destroy).pack(pady=10)