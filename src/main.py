from models.usuario import Usuario
from services import usuarioService

usuario = Usuario("Gonzalo","gonzalo")

print(usuarioService.insertarUsuario(usuario))