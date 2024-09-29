from models.usuario import Usuario
from services import usuarioService

usuario = Usuario("Gonzalo","1234")

print(usuarioService.insertarUsuario(usuario))