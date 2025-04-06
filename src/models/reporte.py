from datetime import datetime  # Importamos datetime para manejar fechas y horas.

class Reporte:
    
    #clase que tiene los atributos
    def __init__(self, id_empleado=0, fecha_generacion=datetime, tipo_reporte="", contenido="", id = 0, nombre_persona=""):#construstor
        
        self.id_empleado = id_empleado
        self.fecha_generacion = fecha_generacion
        self.tipo_reporte = tipo_reporte
        self.contenido = contenido
        self.id = id #seteamos
        self.nombre_persona = nombre_persona  # Este es el nombre del empleado
        
    # Metodo para mostrar la informacion del reporte en formato de cadena
    def mostrar(self):
        return f"{self.id_empleado}\n{self.fecha_generacion}\n{self.tipo_reporte}\n{self.contenido}{self.id}\n{self.nombre_persona}"
   # Retorna una cadena con los datos del reporte separados por saltos de linea
