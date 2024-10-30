
class Persona:
    def __init__(self, nombre, apellido1,apellido2, fecha_nacimiento, cedula,estado_civil,correo, direccion, id = 0,foto = None):
        self.id = id
        self.foto = foto
        self.nombre = nombre
        self.apellido1 = apellido1
        self.apellido2 = apellido2
        self.fecha_nacimiento = fecha_nacimiento
        self.cedula = cedula
        self.estado_civil = estado_civil
        self.correo = correo
        self.direccion = direccion
    def __repr__(self):
        return f"""Id: {self.id}\nNombre: {self.nombre}\nApellidos: {self.apellido1} {self.apellido2}\n{self.cedula}\n{self.direccion}\nFecha: {self.fecha_nacimiento}"""