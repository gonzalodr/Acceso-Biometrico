from models.persona import *
from services.personaService import *
from models.usuario import *
from services.usuarioService import *

## crean primero una presona
##Pservices = PersonaServices()
##persona:Persona = Persona("Yeiler","Madrigal", "Matamoros","2003-02-05","12312353434","Soltero\\a","yeiler@gmail.com","Puerto viejo")

## lo insertan 
##Pservices.insertarPersona(persona)

## commentan lo anterior lo del insertpersona
## se fija que id tiene el registro persona que hicieron y crean el usuario con ese id
Uservices = UsuarioServices()
#usuario contraseña e id de la persona
user:Usuario = Usuario("yeiler","12345678",4)
#user: Usuario = Usuario("Maik", "Maik0024", 1)
Uservices.insertarUsuario(user)

