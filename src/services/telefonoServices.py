from models.telefono import Telefono
from data.telefonoData import TelefonoData

class TelefonoServices:
    def __init__(self):
        self.teldata = TelefonoData()
    
    def crear_telefono(self,telefono:Telefono):
        return self.teldata.create_telefono(telefono)
    
    def actualizar_telefono(self, telefono:Telefono):
        return self.teldata.update_telefono(telefono)
    
    def eliminar_telefono(self, id_telefono:int):
        return self.teldata.delete_telefono(id_telefono)
    
    def verificar_telefono(self,telefono:str,telefono_id:int):
        return self.teldata.verificarExistenciaTelefono(telefono,telefono_id)