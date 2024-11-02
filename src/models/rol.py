
class Rol:
    def __init__(self,nombre, descripcion, id = 0):
        self.nombre = nombre
        self.descripcion = descripcion
        self.id = id

    def mostrar(self):
        return f"{self.nombre} {self.descripcion}"