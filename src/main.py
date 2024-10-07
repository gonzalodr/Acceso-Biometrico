from models.usuario import Usuario
from models.persona import Persona

from services.personaService import PersonaServices

persona = Persona("Gonzalo","Dormos","Rodriguez","2002-07-01","605310603","Soltero","gonzalo.dormos.rodriguez@est.una.ac.cr","Puerto Viejo, Sarapiqui, Heredia")

personServices = PersonaServices()

#print(personServices.eliminarPersona(1))


#print(personServices.insertarPersona(persona))

result = personServices.obtenerListaPersonas(1,5)
lista = []
persona = None
if result["success"]:
    lista = result["data"]["listaPersonas"]

if len(lista) != 0:
    persona = lista[0]
    
print (f" NOMBRE [{persona.nombre}] Id [{persona.id}]")

if persona != None:
    persona.nombre = "Alberto"
    # print(personServices.modificarPersona(persona))



