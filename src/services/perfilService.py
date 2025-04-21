import re
from models.perfil import Perfil
from data.perfilData import PerfilData

class PerfilServices:
    def __init__(self):
        self.perfilData = PerfilData()
        
        
    ##
    # Métodos privados de validación
    ##
    
    def _validarNombre(self, nombre):
        # Validar que el nombre no esté vacío y cumpla con un patrón (solo letras y espacios, hasta 100 caracteres)
        patron = r"^[A-Za-z\s]{1,100}$" # Expresión regular que permite solo letras y espacios.
        result = re.match(patron, nombre)
        if result:
            return {"success": True, "message": "Nombre válido."}
        else:
            return {"success": False, "message": "El nombre del perfil no es válido."}

    def _validarDescripcion(self, descripcion):
        # Validar que la descripción sea adecuada (hasta 100 caracteres)
        if isinstance(descripcion, str) and len(descripcion) <= 100:
            return {"success": True, "message": "Descripción válida."}
        else:
            return {"success": False, "message": "La descripción del perfil no es válida."}

    def existeNombreRegistrado(self, nombre, idPerfil = None):
        return self.perfilData.verificar_nombre_perfil(nombre,idPerfil)
    ##
    # Funciones públicas
    ##

    def insertarPerfil(self, perfil: Perfil, listaPermisos):
        # Validar datos antes de pasar a la capa de datos
        result = self._validarNombre(perfil.nombre)
        if not result["success"]:
            return result

        result = self._validarDescripcion(perfil.descripcion)
        if not result["success"]:
            return result

        # Inserción en la capa de datos
        return self.perfilData.create_perfil(perfil,listaPermisos)

    def modificarPerfil(self, perfil: Perfil, listaPermisos):
        # Validar datos antes de actualizar en la capa de datos
        result = self._validarNombre(perfil.nombre)
        if not result["success"]:
            return result

        result = self._validarDescripcion(perfil.descripcion)
        if not result["success"]:
            return result

        # Actualización en la capa de datos
        return self.perfilData.update_perfil(perfil, listaPermisos)

    def eliminarPerfil(self, id):
        # Eliminar rol por ID
        return self.perfilData.delete_perfil(id)

    def obtenerListaPerfil(self, pagina=1, tam_pagina=10, ordenar_por="id", tipo_orden="ASC", busqueda=None):
        # Obtener lista de roles con paginación y opciones de ordenamiento
        return self.perfilData.list_perfiles(pagina, tam_pagina, ordenar_por, tipo_orden, busqueda)
    
    def obtenerListaPerfilCB(self):
        return self.perfilData.list_perfilesComboBox()

    def obtenerPerfilPorId(self, id):
        # Obtener rol por ID
        return self.perfilData.get_perfil_by_id(id)

    def obtener_todo_perfiles(self):
        return self.perfilData.obtener_todo_perfiles()