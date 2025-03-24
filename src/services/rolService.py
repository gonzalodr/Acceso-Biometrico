import re
from models.rol import Rol
from data.rolData import RolData


class RolServices:
    def __init__(self):
        self.rolData = RolData()

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
            return {"success": False, "message": "El nombre del rol no es válido."}

    def _validarDescripcion(self, descripcion):
        # Validar que la descripción sea adecuada (hasta 100 caracteres)
        if isinstance(descripcion, str) and len(descripcion) <= 100:
            return {"success": True, "message": "Descripción válida."}
        else:
            return {"success": False, "message": "La descripción del rol no es válida."}

    ##
    # Funciones públicas
    ##

    def insertarRol(self, rol: Rol):
        # Validar datos antes de pasar a la capa de datos
        result = self._validarNombre(rol.nombre)
        if not result["success"]:
            return result

        result = self._validarDescripcion(rol.descripcion)
        if not result["success"]:
            return result

        # Inserción en la capa de datos
        return self.rolData.create_rol(rol)

    def modificarRol(self, rol: Rol):
        # Validar datos antes de actualizar en la capa de datos
        result = self._validarNombre(rol.nombre)
        if not result["success"]:
            return result

        result = self._validarDescripcion(rol.descripcion)
        if not result["success"]:
            return result

        # Actualización en la capa de datos
        return self.rolData.update_rol(rol)

    def eliminarRol(self, id):
        # Eliminar rol por ID
        return self.rolData.delete_rol(id)

    def obtenerListaRol(
        self, pagina=1, tam_pagina=10, ordenar_por="id", tipo_orden="ASC", busqueda=None
    ):
        # Obtener lista de roles con paginación y opciones de ordenamiento
        return self.rolData.list_roles(
            pagina, tam_pagina, ordenar_por, tipo_orden, busqueda
        )

    def obtenerRolPorId(self, id):
        # Obtener rol por ID
        return self.rolData.get_rol_by_id(id)

    def obtener_todo_roles(self):
        return self.rolData.obtener_todo_roles()

    # Trae los nombres y id de los registros en Rol
    def obtener_nombre_rol(self):
        return self.rolData.get_all_roles()
