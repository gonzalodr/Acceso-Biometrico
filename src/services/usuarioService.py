import bcrypt 
from models.usuario import Usuario #llamando modulo `models` y a un archivo `usuario` para importar la clase `Usuario`

#funcion privada: se inicia con un guion bajo
def _contrasenaHash(contrasena):
    contrasena = str(contrasena)
    if len(contrasena) > 8 and not contrasena.strip():
        return False, "!La contraseña debe ser minimo de 8 caracteres¡" #retorna dos variables
    else:
        contrasena = contrasena.encode("utf-8")
        contrasena_hash = bcrypt.hashpw(contrasena,bcrypt.gensalt())
        return True, contrasena_hash #retorna dos variables

def _verificarContrasenaHash(contrasena, contrasena_hash):
    pass

def insertarUsuario(usuario: Usuario):
    exito, resultado = _contrasenaHash(usuario.contrasena) #recupera las dos variables
    if not exito:
        return exito,resultado
    else:
        usuario.contrasena = resultado.decode("utf-8")
        return exito, f"¡Usuario [{usuario.usuario}], Contraseña [{usuario.contrasena}]!"