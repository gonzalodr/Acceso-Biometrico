import bcrypt 
from models.usuario import Usuario #llamando modulo `models` y a un archivo `usuario` para importar la clase `Usuario`
from data.usuarioData import UsuarioData
#funcion privada: se inicia con un guion bajo
class UsuarioServices:
    
    def __init__(self):
        self.Usuariodata = UsuarioData()
        
    def _contrasenaHash(contrasena):
        contrasena = str(contrasena)
        if len(contrasena) < 8 :
            return False, f"¡La contraseña debe ser minimo de 8 caracteres!" #retorna dos variables
        elif not contrasena.strip() or contrasena.find(' ') != -1:
            return False, "¡La contraseña no debe llevar espacios!"
        else:
            contrasena = contrasena.encode("utf-8")
            contrasena_hash = bcrypt.hashpw(contrasena,bcrypt.gensalt())
            return True, contrasena_hash #retorna dos variables
        
    ## Verificacion de contraseña
    def _verificarUsuarioYContrasena(self, usuario:Usuario):
        result =  self.Usuariodata.iniciarSesion(usuario)    
        if not result["success"]:
           return result
        if not "passwordbcryt" in result:
            return result
        else:
            contrasena = str(usuario.contrasena).encode("utf-8")
            contrasena_hash = result["passwordbcryt"]
            if bcrypt.checkpw(contrasena, contrasena_hash):
                return {"success":True,"login":True,"message":"Se inicio sesion correctamente"}
            else:
                return {"success":True,"login":True,"message":"Usuario o contraseña incorrectos"}
            
            
            
    def insertarUsuario(self,usuario: Usuario):
        exito, resultado = self._contrasenaHash(usuario.contrasena) #recupera las dos variables
        if not exito:
            return exito,resultado
        else:
            usuario.contrasena = resultado.decode("utf-8")
            return exito, f"¡Usuario [{usuario.usuario}], Contraseña [{usuario.contrasena}]!"
        
    def inicioSesion(self, usuario:Usuario):
        result = self._verificarUsuarioYContrasena(usuario)
        return result