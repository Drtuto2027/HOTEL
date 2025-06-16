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

        # Imagen de usuario (metáfora visual)
        try:
            if os.path.exists("iconos/user.png"):
                img = Image.open("iconos/user.png")
                img = img.resize((60, 60))
                self.user_img = ImageTk.PhotoImage(img)
                tk.Label(self, image=self.user_img).pack(pady=5)
            else:
                tk.Label(self, font=("Arial", 32)).pack(pady=5)
        except Exception as e:
            print(f"Advertencia: No se pudo cargar la imagen de usuario. {e}")
            tk.Label(self, font=("Arial", 32)).pack(pady=5)

        tk.Label(self, text="Cédula:").pack()
        self.cedula_entry = tk.Entry(self)
        self.cedula_entry.pack()
        self.cedula_entry.focus()
        self.cedula_entry.bind("<Control-Return>", lambda e: self.login())

        tk.Label(self, text="Contraseña:").pack()
        
        # Frame para contener la entrada de contraseña y el botón del ojito
        self.pass_frame = tk.Frame(self)
        self.pass_frame.pack()
        
        self.pass_entry = tk.Entry(self.pass_frame, show="*")
        self.pass_entry.pack(side=tk.LEFT)
        self.pass_entry.bind("<Control-Return>", lambda e: self.login())
        
        # Cargar imágenes para el botón de mostrar/ocultar contraseña
        try:
            # Imagen de ojo abierto (mostrar contraseña)
            eye_open_img = Image.open("icons\eye.png")
            eye_open_img = eye_open_img.resize((20, 15))
            self.eye_open = ImageTk.PhotoImage(eye_open_img)
            
            # Imagen de ojo cerrado (ocultar contraseña)
            eye_closed_img = Image.open("icons\eye.png")
            eye_closed_img = eye_closed_img.resize((20, 15))
            self.eye_closed = ImageTk.PhotoImage(eye_closed_img)
            
            # Botón del ojito
            self.eye_button = tk.Label(self.pass_frame, image=self.eye_closed, cursor="hand2")
            self.eye_button.pack(side=tk.LEFT, padx=5)
            self.eye_button.bind("<Button-1>", self.toggle_password_visibility)
        except Exception as e:
            print(f"Advertencia: No se pudieron cargar los iconos de ojo. {e}")
            # Fallback a texto si no se cargan las imágenes
            self.eye_button = tk.Label(self.pass_frame, text="👁", cursor="hand2")
            self.eye_button.pack(side=tk.LEFT, padx=5)
            self.eye_button.bind("<Button-1>", self.toggle_password_visibility)

        login_btn = tk.Button(self, text="Iniciar Sesión", command=self.login)
        login_btn.pack(pady=10)

        # Botón para registrar administrador
        registrar_btn = tk.Button(self, text="Registrarse", command=self.abrir_registro_admin)
        registrar_btn.pack(pady=5)

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