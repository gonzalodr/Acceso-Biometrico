from models.usuario import Usuario
from models.persona import Persona

from services.personaService import PersonaServices

persona = Persona("Javier","Diaz","Urbina","2002-07-01","11111111111111","Soltero","javier@est.una.ac.cr","Puerto Viejo, Sarapiqui, Heredia")

personServices = PersonaServices()

#print(personServices.eliminarPersona(1))


# print(personServices.insertarPersona(persona))

result = personServices.obtenerListaPersonas(1,5)
lista = []
persona = None
if result["success"]:
    lista = result["data"]["listaPersonas"]

if len(lista) != 0:
    persona = lista[0]

print("Mostrando Lista")
for persona in lista:
    print (f" Nombre [{persona.nombre}] Id [{persona.id}]")




