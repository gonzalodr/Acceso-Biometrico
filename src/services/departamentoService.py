import re
from models.departamento import Departamento
from data.departamentoData import DepartamentoData


class DepartamentoServices:
    def __init__(self):
        self.departamentoData = DepartamentoData()
        
           ##
    # Métodos privados de validación
    ##
    
    def _validarNombre(self, nombre):
        # Validar que el nombre no esté vacío y cumpla con un patrón (solo letras y espacios, hasta 100 caracteres)
        patron = r"^[A-Za-z\s]{1,100}$"
        result = re.match(patron, nombre)
        if result:
            return {"success": True, "message": "Nombre válido."}
        else:
            return {"success": False, "message": "El nombre del departamento no es válido."}

    def _validarDescripcion(self, descripcion):
        # Validar que la descripción sea adecuada (hasta 100 caracteres)
        if isinstance(descripcion, str) and len(descripcion) <= 100:
            return {"success": True, "message": "Descripción válida."}
        else:
            return {"success": False, "message": "La descripción del departamento no es válida."}

    ##
    # Funciones públicas
    ##

    def insertarDepartamento(self, departamento: Departamento):
        # Validar datos antes de pasar a la capa de datos
        result = self._validarNombre(departamento.nombre)
        if not result["success"]:
            return result

        result = self._validarDescripcion(departamento.descripcion)
        if not result["success"]:
            return result

        # Inserción en la capa de datos
        return self.departamentoData.create_departamento(departamento)

    def modificarDepartamento(self, departamento: Departamento):
        # Validar datos antes de actualizar en la capa de datos
        result = self._validarNombre(departamento.nombre)
        if not result["success"]:
            return result

        result = self._validarDescripcion(departamento.descripcion)
        if not result["success"]:
            return result

        # Actualización en la capa de datos
        return self.departamentoData.update_departamento(departamento)

    def eliminarDepartamento(self, id):
            return self.departamentoData.delete_departamento(id)

    def obtenerListaDepartamento(self, pagina=1, tam_pagina=10, ordenar_por="id", tipo_orden="ASC", busqueda=None):
        return self.departamentoData.list_departamentos(pagina, tam_pagina, ordenar_por, tipo_orden, busqueda)

    def obtenerDepartamentoPorId(self, id):
        return self.departamentoData.get_departamento_by_id(id)
    
    def obtenerTodoDepartamento(self):
        return self.departamentoData.obtener_todo_departamentos()