import tkinter as tk
from tkinter import *
from tkinter import messagebox
from Tooltip import Tooltip

class Loggin():
    def mostrarAyuda(self, event):
        messagebox.showinfo("Ayuda","Ingrese nombre de usuario y contraseña asignados\nEl campo")
    def verCaracteres(self,event):
        if(self.bandera== False):
         self.txtPasword.config(show='')
         self.bandera=True
        else:
             self.txtPasword.config(show='')
             self.bandera=False
    


    def _init_(self):
        self.ventana= tk.Tk()
        self.ventana.resizable(0,0)
        self.ventana.title("Loggin")
        self.ventana.config(width=405,height=250)

        self.iconoIngresado = tk.PhotoImage(file=r"icons\door_in.png")
        self.iconoAyuda = tk.PhotoImage(file=r"icons\help.png")
        self.iconoVer = tk.PhotoImage(file=r"icons\eye.png")
        self.Bandera=False
        
        
        

        self.lblTitulo = tk.Label(self.ventana, text="Inicio de Sesion")
        self.lblTitulo.place(width=150, height=25, y=30, relx=0.5, anchor="n")

        self.btnAyuda = tk.Button(self.ventana, image=self.iconoAyuda)
        self.btnAyuda.place(width=25, height=25, x=330, y=30)
        self.btnAyuda.bind("<Button-1>", self.mostrarAyuda)

        self.lblUsuario = tk.Label(self.ventana, text="Nombre de Usuario*:")
        self.lblUsuario.place(width=70,height=25,x=50,y=85)

        self.txtUsuario = tk.Entry(self.ventana)
        self.txtUsuario.place(width=150, height=25, x=150, y=85)
        #Listener

        self.lblPassword = tk.Label(self.ventana, text="Contraseña*:",showe="")
        self.lblPassword.place(width=70,height=25,x=50,y=140)

        self.txtPassword = tk.Entry(self.ventana)
        self.txtPassword.place(width=150, height=25, x=150, y=140)
        #listener

        self.btnVer = tk.Button(self.ventana, image=self.iconoVer)
        self.btnVer.place(width=25,height=25, x=330,y=140)
        self.btnVer.bind("<Enter>"self.ventanaCaracteres)
        self.btnVer.bind("<Leave>"self.ventanaCaracteres)
        
        self.btnIngresar = tk.Button(self.ventana, text="Ingresar" ,image=self.iconoIngresado, compound=LEFT)
        self.btnIngresar.place(width=70, height=25, relx=0.5, y=195, anchor="n")
        #listener

        self.ventana.mainloop()

a = Loggin()