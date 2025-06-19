
class Permiso_Perfil:
    def __init__(self,perfil_id:int, tabla:str,ver:bool,crear:bool,editar:bool,eliminar:bool, id:int = None):
        self.id = id
        self.perfil_id = perfil_id
        self.tabla = tabla
        self.ver = ver
        self.crear = crear
        self.editar = editar
        self.eliminar = eliminar
        
    def __repr__(self):
        return f"{self.id} {self.perfil_id} {self.tabla} {self.ver} {self.crear} {self.editar} {self.eliminar}\n"
    # cadena con los detalles del permiso