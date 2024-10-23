from services.usuarioService import UsuarioServices
from models.usuario import Usuario

user = Usuario(usuario="gonzalo",contrasena="12345678",id_persona=1)

data = UsuarioServices()

# print(data.insertarUsuario(user))

print(data.iniciar_sesion("gonzalodormos26@gmail.com","12345678"))
