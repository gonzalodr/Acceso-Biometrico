#creacion de una clase 
class Usuario:
    def __init__(self, usuario, contrasena, id=0, id_persona=0):
        self.id = id
        self.id_persona = id_persona
        self.usuario = usuario
        self.contrasena = contrasena
        
    def mostrar(self):
        return f"ID: {self.id}, ID Persona: {self.id_persona}, Usuario: {self.usuario}, Contraseña: {self.contrasena}"
