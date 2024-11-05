
class Permiso_Rol:
    def __init__(self,rol_id:int, tabla:str,ver:bool,crear:bool,editar:bool,eliminar:bool, id:int=0):
        self.id = id
        self.rol_id = rol_id
        self.tabla = tabla
        self.ver = ver
        self.crear = crear
        self.editar = editar
        self.eliminar = eliminar
        
    def __repr__(self):
        return f"{self.id}\n{self.rol_id}\n{self.tabla}\n{self.ver}\n{self.crear}\n{self.editar}\n{self.eliminar}"