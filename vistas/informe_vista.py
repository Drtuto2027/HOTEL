import tkinter as tk

class InformeVista(tk.Toplevel):
    def __init__(self, informe):
        super().__init__()
        self.title("Informe Diario")
        self.geometry("350x300")
        self.resizable(False, False)

        tk.Label(self, text="Informe Diario", font=("Arial", 14, "bold")).pack(pady=10)

        frame = tk.Frame(self)
        frame.pack(pady=5)

        # Etiquetas alineadas
        tk.Label(frame, text="Total ingresos:", anchor="w", width=20).grid(row=0, column=0, sticky="w")
        tk.Label(frame, text=f"{informe['total_ingresos']}", anchor="w").grid(row=0, column=1, sticky="w")

        tk.Label(frame, text="Número de facturas:", anchor="w", width=20).grid(row=1, column=0, sticky="w")
        tk.Label(frame, text=f"{informe['numero_facturas']}", anchor="w").grid(row=1, column=1, sticky="w")

        # Detalle de facturas
        tk.Label(self, text="Detalle de facturas:", font=("Arial", 10, "bold")).pack(pady=(10,0))
        detalle = tk.Text(self, height=8, width=40)
        detalle.pack()
        detalle.config(state="normal")
        for f in informe["facturas"]:
            detalle.insert(tk.END, f"{f['fecha']} - {f['cliente']} - {f['monto']}\n")
        detalle.config(state="disabled")

        tk.Button(self, text="Salir", command=self.destroy).pack(pady=10)