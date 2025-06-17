import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from vistas.registro_admin_vista import RegistroAdminVista
from controladores.admin_controlador import AdminControlador

class LoginVista(tk.Tk):
    def __init__(self, login_controlador, on_login_success):
        super().__init__()
        self.title("Hotel - Login")
        self.geometry("350x250")
        self.resizable(False, False)

        # Intentar cargar el icono de la ventana
        try:
            if os.path.exists("iconos/hotel.ico"):
                self.iconbitmap("iconos/hotel.ico")
        except Exception as e:
            print(f"Advertencia: No se pudo cargar el icono de la ventana. {e}")

        # Contenedor principal para centrar los elementos
        main_frame = tk.Frame(self)
        main_frame.pack(expand=True, pady=10)

        # Imagen de usuario (metáfora visual)
        try:
            if os.path.exists("iconos/user.png"):
                img = Image.open("iconos/user.png")
                img = img.resize((60, 60))
                self.user_img = ImageTk.PhotoImage(img)
                tk.Label(main_frame, image=self.user_img).pack(pady=5)
            else:
                tk.Label(main_frame, font=("Arial", 32)).pack(pady=5)
        except Exception as e:
            print(f"Advertencia: No se pudo cargar la imagen de usuario. {e}")
            tk.Label(main_frame, font=("Arial", 32)).pack(pady=5)

        # Frame para los campos de entrada
        input_frame = tk.Frame(main_frame)
        input_frame.pack(pady=5)

        # Campo de cédula
        tk.Label(input_frame, text="Cédula:").grid(row=0, column=0, sticky="w", pady=2)
        self.cedula_entry = tk.Entry(input_frame)
        self.cedula_entry.grid(row=1, column=0, sticky="ew", pady=2)
        self.cedula_entry.focus()
        self.cedula_entry.bind("<Control-Return>", lambda e: self.login())

        # Campo de contraseña
        tk.Label(input_frame, text="Contraseña:").grid(row=2, column=0, sticky="w", pady=2)
        
        # Frame para la entrada de contraseña y el botón del ojo
        pass_frame = tk.Frame(input_frame)
        pass_frame.grid(row=3, column=0, sticky="ew")
        
        self.pass_entry = tk.Entry(pass_frame, show="*")
        self.pass_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.pass_entry.bind("<Control-Return>", lambda e: self.login())
        
        # Botón de mostrar/ocultar contraseña
        try:
            eye_open_img = Image.open("icons/eye.png")
            eye_open_img = eye_open_img.resize((20, 15))
            self.eye_open = ImageTk.PhotoImage(eye_open_img)
            
            eye_closed_img = Image.open("icons/eye.png")
            eye_closed_img = eye_closed_img.resize((20, 15))
            self.eye_closed = ImageTk.PhotoImage(eye_closed_img)
            
            self.eye_button = tk.Label(pass_frame, image=self.eye_closed, cursor="hand2")
            self.eye_button.pack(side=tk.LEFT, padx=5)
            self.eye_button.bind("<Button-1>", self.toggle_password_visibility)
        except Exception as e:
            print(f"Advertencia: No se pudieron cargar los iconos de ojo. {e}")
            self.eye_button = tk.Label(pass_frame, text="👁", cursor="hand2")
            self.eye_button.pack(side=tk.LEFT, padx=5)
            self.eye_button.bind("<Button-1>", self.toggle_password_visibility)

        # Frame para los botones
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=10)

        login_btn = tk.Button(button_frame, text="Iniciar Sesión", command=self.login)
        login_btn.pack(side=tk.LEFT, padx=5)

        registrar_btn = tk.Button(button_frame, text="Registrarse", command=self.abrir_registro_admin)
        registrar_btn.pack(side=tk.LEFT, padx=5)

        self.login_controlador = login_controlador
        self.on_login_success = on_login_success

    def toggle_password_visibility(self, event):
        if self.pass_entry['show'] == "*":
            self.pass_entry.config(show="")
            self.eye_button.config(image=self.eye_open)
        else:
            self.pass_entry.config(show="*")
            self.eye_button.config(image=self.eye_closed)

    def login(self):
        cedula = self.cedula_entry.get()
        password = self.pass_entry.get()
        try:
            usuario = self.login_controlador.login(cedula, password)
            if usuario:
                self.destroy()
                self.on_login_success(usuario)
            else:
                messagebox.showerror("Error", "Credenciales incorrectas")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def abrir_registro_admin(self):
        admin_controlador = AdminControlador()
        RegistroAdminVista(admin_controlador)