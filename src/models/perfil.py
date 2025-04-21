class Perfil:
    def __init__(self, nombre="", descripcion="", id = None):
        self.nombre = nombre
        self.descripcion = descripcion
        self.id = id
    
    def mostrar(self):
        return f"{self.nombre} {self.descripcion}" #Cadena con el nombre y la descripción del perfil.