#creacion de una clase 
class Usuario_Perfil:
    def __init__(self, id_perfil=0, id_Usuario=0, id=0):
        self.id = id
        self.id_perfil = id_perfil
        self.id_Usuario = id_Usuario
        
    def mostrar(self):
        return f"ID: {self.id}, ID Perfil: {self.id_perfil}, ID Usuario: {self.id_Usuario}"