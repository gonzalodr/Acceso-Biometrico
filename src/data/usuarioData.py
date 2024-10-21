from models.usuario import Usuario
from data.data import conection
from settings.config import *

class UsuarioData:
    def iniciarSesion(self, usuario: Usuario):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        try:
            cursor = conexion.cursor()
            query = f"SELECT {TBUSUARIOCONTRASENA} FROM {TBUSUARIO} WHERE {TBUSUARIOUSUARIO} =%s "
            cursor.execute(query,(usuario.usuario, usuario.contrasena))
            sesion = cursor.fetchone()
            if sesion:
                resultado["success"] = True
                resultado["passwordbcryt"] = sesion[TBUSUARIOCONTRASENA]
                resultado["message"] = "Inicio de sesión correctamente."
            else:  
                resultado["success"] = True
                resultado["message"] = "Usuario o contraseña incorrectas."
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = "Error al verificar el usuario"
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()
        return resultado

    def insertarUsuario(self, usuario:Usuario):
        pass
    
    def eliminarUsuario(self, id):
        pass
    
    def modificarUsuario(self, usuario: Usuario):
        pass
    
    def listarUsuario(self):
        pass
    
    def obtenerUsuarioPorId(self,id):
        pass
    
    def verificarExistenciaUsuario(self, usuario):
        pass
    