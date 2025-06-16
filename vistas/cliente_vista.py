import tkinter as tk
from tkinter import messagebox, ttk
import os
from modelos.factura import Factura

class ClienteVista(tk.Toplevel):
    def __init__(self, cliente_controlador, on_logout):
        super().__init__()
        self.title("Panel Cliente")
        self.geometry("600x400")
        self.cliente_controlador = cliente_controlador
        self.on_logout = on_logout

        # Intentar cargar el icono
        try:
            if os.path.exists("iconos/cliente.ico"):
                self.iconbitmap("iconos/cliente.ico")
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

        # Botón de cerrar sesión
        btn_logout = tk.Button(self, text="Cerrar sesión", command=self.cerrar_sesion)
        btn_logout.pack(side="bottom", pady=10)

        # Pestañas
        tabs = ttk.Notebook(self)
        tabs.pack(fill="both", expand=True)

        # Habitaciones disponibles
        frame_hab = ttk.Frame(tabs)
        tabs.add(frame_hab, text="Habitaciones Disponibles")
        ttk.Button(frame_hab, text="Realizar Reserva", command=self.realizar_reserva).pack(pady=5)
        self.tree_hab = ttk.Treeview(frame_hab, columns=("id", "numero", "tipo", "precio", "estado"), show="headings")
        for col in self.tree_hab["columns"]:
            self.tree_hab.heading(col, text=col.capitalize())
        self.tree_hab.pack(fill="both", expand=True)
        

        # Reservas
        frame_res = ttk.Frame(tabs)
        tabs.add(frame_res, text="Mis Reservas")
        ttk.Button(frame_res, text="Cancelar Reserva", command=self.cancelar_reserva).pack(pady=5)
        self.tree_res = ttk.Treeview(frame_res, columns=("id", "habitacion", "entrada", "salida", "estado"), show="headings")
        for col in self.tree_res["columns"]:
            self.tree_res.heading(col, text=col.capitalize())
        self.tree_res.pack(fill="both", expand=True)

        # Facturas
        frame_fac = ttk.Frame(tabs)
        tabs.add(frame_fac, text="Mis Facturas")
        ttk.Button(frame_fac, text="Ver/Pagar Factura", command=self.ver_pagar_factura).pack(pady=5)
        self.tree_fac = ttk.Treeview(frame_fac, columns=("id", "reserva", "monto_total", "fecha", "estado_reserva"), show="headings")
        self.tree_fac.heading("id", text="ID")
        self.tree_fac.heading("reserva", text="Reserva")
        self.tree_fac.heading("monto_total", text="Monto Total")
        self.tree_fac.heading("fecha", text="Fecha")
        self.tree_fac.heading("estado_reserva", text="Estado Reserva")
        self.tree_fac.pack(fill="both", expand=True)

        self.cargar_habitaciones()
        self.cargar_reservas()
        self.cargar_facturas()

    def cargar_habitaciones(self):
        try:
            for i in self.tree_hab.get_children():
                self.tree_hab.delete(i)
            for h in self.cliente_controlador.consultar_habitaciones_disponibles():
                self.tree_hab.insert("", "end", values=(h.id, h.numero, h.tipo, h.precio, h.estado))
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar habitaciones: {e}")

    def cargar_reservas(self):
        try:
            for i in self.tree_res.get_children():
                self.tree_res.delete(i)
            for r in self.cliente_controlador.obtener_mis_reservas():
                self.tree_res.insert("", "end", values=(r.id, r.habitacion_id, r.fecha_entrada, r.fecha_salida, r.estado))
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar reservas: {e}")

    def cargar_facturas(self):
        self.tree_fac.delete(*self.tree_fac.get_children())
        
        facturas = Factura.obtener_por_cliente(self.cliente_controlador.cliente.cedula)
        for factura in facturas:
            self.tree_fac.insert(
                "", "end",
                values=(
                    factura.id,
                    factura.reserva_id,
                    factura.monto_total,
                    factura.fecha,
                    factura.estado_reserva
                )
            )

    def cerrar_sesion(self):
        self.destroy()
        self.on_logout()

    def realizar_reserva(self):
        selected = self.tree_hab.selection()
        if not selected:
            messagebox.showerror("Error", "Selecciona una habitación para reservar")
            return
        habitacion = self.tree_hab.item(selected[0])["values"]
        habitacion_id = habitacion[0]

        def guardar():
            fecha_entrada = entry_fecha_entrada.get()
            fecha_salida = entry_fecha_salida.get()
            if not all([fecha_entrada, fecha_salida]):
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            exito = self.cliente_controlador.realizar_reserva(
                habitacion_id, fecha_entrada, fecha_salida
            )
            if exito:
                messagebox.showinfo("Éxito", "Reserva realizada correctamente")
                top.destroy()
                self.cargar_habitaciones()
                self.cargar_reservas()
            else:
                messagebox.showerror("Error", "No se pudo realizar la reserva")

        top = tk.Toplevel(self)
        top.title("Realizar Reserva")
        top.geometry("300x200")
        tk.Label(top, text="Fecha Entrada (YYYY-MM-DD):").pack()
        entry_fecha_entrada = tk.Entry(top)
        entry_fecha_entrada.pack()
        tk.Label(top, text="Fecha Salida (YYYY-MM-DD):").pack()
        entry_fecha_salida = tk.Entry(top)
        entry_fecha_salida.pack()
        tk.Button(top, text="Reservar", command=guardar).pack(pady=10)

    def cancelar_reserva(self):
        selected = self.tree_res.selection()
        if not selected:
            messagebox.showerror("Error", "Selecciona una reserva para cancelar")
            return
        reserva = self.tree_res.item(selected[0])["values"]
        reserva_id = reserva[0]
        estado = reserva[4]
        if estado == "cancelada":
            messagebox.showinfo("Info", "La reserva ya está cancelada")
            return
        confirmar = messagebox.askyesno("Confirmar", "¿Seguro que deseas cancelar esta reserva?")
        if confirmar:
            exito = self.cliente_controlador.cancelar_reserva(reserva_id)
            if exito:
                messagebox.showinfo("Éxito", "Reserva cancelada correctamente")
                self.cargar_reservas()
                self.cargar_habitaciones()
            else:
                messagebox.showerror("Error", "No se pudo cancelar la reserva")

    def ver_pagar_factura(self):
        selected = self.tree_fac.selection()
        if not selected:
            messagebox.showerror("Error", "Selecciona una factura para ver o pagar")
            return
        factura = self.tree_fac.item(selected[0])["values"]
        factura_id = factura[0]
        reserva_id = factura[1]

        factura_obj = Factura.buscar_por_id(factura_id)
        if not factura_obj:
            messagebox.showerror("Error", "No se encontró la factura seleccionada")
            return

        estado_reserva = self.cliente_controlador.obtener_estado_reserva(reserva_id)

        top = tk.Toplevel(self)
        top.title("Factura")
        top.geometry("350x250")
        tk.Label(top, text=f"Factura ID: {factura_obj.id}").pack()
        tk.Label(top, text=f"Reserva ID: {factura_obj.reserva_id}").pack()
        tk.Label(top, text=f"Detalles: {factura_obj.detalles}").pack()
        tk.Label(top, text=f"Monto Total: {factura_obj.monto_total}").pack()
        tk.Label(top, text=f"Fecha: {factura_obj.fecha}").pack()
        tk.Label(top, text=f"Estado de Reserva: {estado_reserva}").pack()

        if estado_reserva != "confirmada":
            def pagar():
                exito = self.cliente_controlador.pagar_factura(factura_obj.id, factura_obj.reserva_id)
                if exito:
                    messagebox.showinfo("Éxito", "Factura pagada y reserva confirmada")
                    top.destroy()
                    self.cargar_facturas()
                    self.cargar_reservas()
                else:
                    messagebox.showerror("Error", "No se pudo realizar el pago")
            tk.Button(top, text="Pagar", command=pagar).pack(pady=10)
        else:
            tk.Label(top, text="Reserva ya confirmada.").pack(pady=10)

        tk.Button(top, text="Cerrar", command=top.destroy).pack(pady=5)