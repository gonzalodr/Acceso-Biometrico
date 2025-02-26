from datetime import date

class Persona:
    def __init__(self, nombre: str, apellidos: str, fecha_nacimiento: date, cedula: str, estado_civil: str, correo: str, direccion: str, id: int = 0, foto: bytes = None):
        self.id         = id
        self.foto       = foto
        self.nombre     = nombre
        self.apellidos  = apellidos
        self.fecha_nacimiento = fecha_nacimiento
        self.cedula     = cedula
        self.estado_civil = estado_civil
        self.correo     = correo
        self.direccion  = direccion

    def __str__(self):
        return (f"ID: {self.id}, Nombre: {self.nombre}, Apellidos: {self.apellidos}, "
                f"Cédula: {self.cedula}, Dirección: {self.direccion}, Fecha de Nacimiento: {self.fecha_nacimiento}, "
                f"Estado Civil: {self.estado_civil}, Correo: {self.correo}, Foto: {self.foto}")

    def __repr__(self): 
        return (f"Persona(id={self.id}, nombre='{self.nombre}', apellidos='{self.apellidos}', "
                f"fecha_nacimiento={self.fecha_nacimiento}, cedula='{self.cedula}', estado_civil='{self.estado_civil}', "
                f"correo='{self.correo}', direccion='{self.direccion}', foto={self.foto})")