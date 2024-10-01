
class Persona:
    def __init__(self,nombre, apellido1,apellido2, cedula, estadoCivil):
        self.nombre = nombre
        self.apellido1 = apellido1
        self.apellido2 = apellido2
        self.cedula = cedula
        self.estadoCivil = estadoCivil
    
    def mostrar(self):
        return f"{self.nombre} {self.apellido1} {self.apellido2}, N.Ced: {self.cedula}, {self.estadoCivil} "