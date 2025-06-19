"""class Empleado:
    def __init__(self, id_persona=0, id_departamento=0, id = 0):
        self.id_persona = id_persona
        self.id_departamento = id_departamento
        self.id = id
    
    def mostrar(self):
        return f"{self.id_persona} {self.id_departamento}" #Cadena con el nombre y la descripción del perfil.
        """
        
        
class Empleado:
    def __init__(self, id_persona=0, id_departamento=0, id=0, nombre_persona=""):
        self.id_persona = id_persona
        self.id_departamento = id_departamento
        self.id = id
        self.nombre_persona = nombre_persona  #  Agregar este atributo
        
    def mostrar(self):
        return f"{self.id_persona} {self.id_departamento} {self.nombre_persona}" #Cadena con el nombre y la descripción del perfil.
