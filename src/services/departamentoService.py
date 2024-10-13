from models.departamento import Departamento
from data.departamentoData import DepartamentoData
import re

class DepartamentoServices:
    def __init__(self):
        self.departamento_data = DepartamentoData()
        
           ##
    # Métodos privados de validación
    ##
    def _validar_nombre(self, nombre):
        # Validar que el nombre no esté vacío y cumpla con un patrón (solo letras y espacios, hasta 100 caracteres)
        return bool(re.match(r"^[A-Za-z\s]{1,100}$", nombre))
    
    def _validar_descripcion(self, descripcion):
        # Validar que la descripción sea adecuada (hasta 100 caracteres)
        return isinstance(descripcion, str) and len(descripcion) <= 100
    
    
    def crear_departamento(self, nombre, descripcion):
        # Validar datos antes de pasar a la capa de datos
        if not self._validar_nombre(nombre):
            return {"success": False, "message": "El nombre del departamento no es válido."}
        
        if not self._validar_descripcion(descripcion):
            return {"success": False, "message": "La descripción del departamento no es válida."}
        
        departamento = Departamento(nombre=nombre, descripcion=descripcion)
        resultado = self.departamento_data.create_departamento(departamento)
        return resultado
    
    def eliminar_departamento(self, departamento_id):
        if not isinstance(departamento_id, int) or departamento_id <= 0:
            return {"success": False, "message": "El ID del departamento no es válido."}
        
        resultado = self.departamento_data.delete_departamento(departamento_id)
        return resultado
    
    def listar_departamentos(self, pagina=1, tam_pagina=10, ordenar_por="id", tipo_orden="ASC", busqueda=None):
        # Validar parámetros de paginación y orden
        if pagina <= 0 or tam_pagina <= 0:
            return {"success": False, "message": "Parámetros de paginación no válidos."}
        
        if tipo_orden not in ["ASC", "DESC"]:
            tipo_orden = "ASC"  # Valor por defecto
        
        resultado = self.departamento_data.list_departamentos(pagina, tam_pagina, ordenar_por, tipo_orden, busqueda)
        return resultado

 
