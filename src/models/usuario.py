#creacion de una clase 
class Usuario:
    def __init__(self, usuario, contrasena):
        self.usuario = usuario
        self.contrasena = contrasena
        
    def mostrar(self):
        return f"Usuario: {self.usuario}, Contraseña: {self.contrasena}"