
class Permiso_Rol:
    def __init__(self,rol_id:int, tabla:str,ver:bool,crear:bool,editar:bool,eliminar:bool):
        self.rol_id = rol_id
        self.tabla = tabla
        self.ver = ver
        self.crear = crear
        self.editar = editar
        self.eliminar = eliminar