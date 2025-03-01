class Reporte:
    
    #clase que tiene los atributos
    def __init__(self, id_empleado:int, fecha_generacion="", tipo_reporte="", contenido="", id = 0):#construstor
        self.id = id #seteamos
        self.id_empleado = id_empleado
        self.fecha_generacion = fecha_generacion
        self.tipo_reporte = tipo_reporte
        self.contenido = contenido
        
    def mostrar(self):
        return f"{self.id}\n{self.id_empleado}\n{self.fecha_generacion}\n{self.tipo_reporte}\n{self.contenido}"
    #cadena cpn las cosas de reporte
