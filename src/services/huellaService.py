from data.huellaData import HuellaData
from models.huella import Huella

class HuellaService:

    def __init__(self):
        self.huellaData = HuellaData()

    def insertarHuella(self, huella: Huella):
        # Inserción en la capa de datos
        return self.huellaData.create_huella(huella)
    
    def listar_huellas(self, pagina=1, tam_pagina=10, ordenar_por="Id", tipo_orden="DESC", busqueda=None):
        """
        Llama al método de la capa de datos para listar las huellas.
        """
        return self.huellaData.listar_huellas(pagina, tam_pagina, ordenar_por, tipo_orden, busqueda)

    def obtener_huella_por_id(self, id_huella: int):
        """
        Llama al método de la capa de datos para obtener una huella por su ID.
        """
        return self.huellaData.get_huella_by_id(id_huella)
    
    def buscar_huellas_por_empleado(self, id_empleado: int):
        """
        Llama al método de la capa de datos para buscar huellas de un empleado.
        """
        return self.huellaData.buscar_huella_por_empleado(id_empleado)

    
    
    def eliminarHuella(self, id_huella):
        return self.huellaData.eliminar_huella(id_huella)
    

