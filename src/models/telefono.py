
class Telefono:
    def __init__(self,id_persona:int=0,numero:str='',tipo_contacto:str='', id:int = 0):
        self.id = id
        self.id_persona = id_persona
        self.numero = numero
        self.tipo = tipo_contacto
    
    def __str__(self):
        return f'{self.numero} - {self.tipo} - {self.id_persona} - {self.id}'