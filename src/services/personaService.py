import re
from models.persona import Persona
from datetime import datetime
from data.personaData import PersonaData
##
# Funciones privadas
##
class PersonaServices:
        
    def __init__(self):
        self.personaData = PersonaData()
    
    def validar_cedula(self,cedula,id=None):
        result = self.personaData.cedula_exists(cedula=cedula,persona_id=id)

        if result:
            return{"success":False,"message":"La cedula ya esta registrada por otra persona"}
        else:
            return{"success":True,"message":"Cedula valida"}
    
    def _validarFechaNacimiento(self,fecha_str):
        try:
            fecha = datetime.strptime(fecha_str,"%Y-%m-%d")
            if fecha.date() >= datetime.now().date(): # se convierte a un mismo formato y objeto
                return {"success": False, "message":"¡Fecha de nacimiento no validad!"}

            return {"success":True, "fecha":fecha}
        except ValueError:
            return {"success":False,"message":"¡Fecha de nacimiento no validad!"}

    def verificacionCorreo(self,correo,id=None):
        correo = str(correo)
        patron = r'^[a-z0-9_.+-]+@[a-z0-9-]+(\.[a-z0-9-]+)+$'# especifica el formato que se debe seguir
        result = re.match(patron, correo)#verifica si el correo cumple con dichas condiciones para ser correo
        if result:
            if self.personaData.email_exists(correo,persona_id=id):
                return {"success":False, "message":"Este correo ya esta registrado por otra persona"}
            else:
                return {"success":True, "message":"¡Correo Valido!"}
        else:
            return {"success":False,"message":"Asegúrese que el correo sea válido, que no tenga mayusculas y que el dominio este correcto. Ejemplo: empleado@example.com"}
    ##
    # Insertar persona.
    # permite la comunicacion entre UI y Data
    # recive como parametro un objeto persona
    # ##
    def insertarPersona(self, persona: Persona):
        result = self.verificacionCorreo(persona.correo)
        if not result["success"]:
            return result
        
        result = self._validarFechaNacimiento(persona.fecha_nacimiento)
        if result["success"]:
            persona.fecha_nacimiento = result["fecha"]
        else:
            return result
        
        return self.personaData.create_persona(persona)
        
    def modificarPersona(self,persona: Persona):
        result = self.verificacionCorreo(persona.correo,persona.id)
        if not result["success"]:
            return result
        
        result = self._validarFechaNacimiento(str(persona.fecha_nacimiento))
        
        if result:
            persona.fecha_nacimiento = result["fecha"]
        else:
            return result
        
        return self.personaData.update_persona(persona)

    def eliminarPersona(self,id):
        return self.personaData.delete_persona(id)

    def obtenerListaPersonas(self,pagina=1,tam_pagina=10, ordenar_por = "Id", tipo_orden = "ASC",busqueda = None):
        return self.personaData.list_personas(pagina,tam_pagina,ordenar_por,tipo_orden, busqueda)

    def obtenerPersonaPorId(self, id):
        return self.personaData.get_persona_by_id(id)
    
    def obtenerListaPersonasSinUsuario(self, id_persona: int):
        return self.personaData.list_personas_sin_usuario(id_persona)
    
    
