from models.persona import *
from services.personaService import *
from models.usuario import *
from services.usuarioService import *

if __name__ == "__main__":
    print()
    ## crean primero una presona
    # Pservices = PersonaServices()
    # persona:Persona = Persona("Gonzalo","Dormos", "Rodriguez","2002-07-01","605310603","Soltero\\a","gonzalodormos26@gmail.com","Puerto viejo,Sarapiqui")

    # ## lo insertan 
    # print(Pservices.insertarPersona(persona))

    # ## commentan lo anterior lo del insertpersona
    # ## se fija que id tiene el registro persona que hicieron y crean el usuario con ese id
    # Uservices = UsuarioServices()
    # #usuario contraseña e id de la persona
    # user:Usuario = Usuario("gonzalo","12345678",1)
    # #user: Usuario = Usuario("Maik", "Maik0024", 1)
    # print(Uservices.insertarUsuario(user))

