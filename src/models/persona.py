
class Persona:
    def __init__(self, nombre, apellidos, fecha_nacimiento, cedula,estado_civil,correo, direccion, id = 0,foto = None):
        self.id = id
        self.foto = foto
        self.nombre = nombre
        self.apellidos = apellidos
        self.fecha_nacimiento = fecha_nacimiento
        self.cedula = cedula
        self.estado_civil = estado_civil
        self.correo = correo
        self.direccion = direccion
    def __repr__(self):
        return f"""Id: {self.id}\nNombre: {self.nombre}\nApellidos: {self.apellidos} \n{self.cedula}\n{self.direccion}\nFecha: {self.fecha_nacimiento}"""