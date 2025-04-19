import bcrypt 
from models.usuario import Usuario #llamando modulo `models` y a un archivo `usuario` para importar la clase `Usuario`
from data.usuarioData import UsuarioData
import re

class UsuarioServices:
    def __init__(self):
        self.UserData = UsuarioData() 

    def verificarUsuario(self,usuario:str,id_usuario:int = None):
        return self.UserData.verificar_usuario(usuario, id_usuario)
        
    def verificacionCorreo(self,correo):
        correo = str(correo)
        patron = r'^[a-z0-9_.+-]+@[a-z0-9-]+(\.[a-z0-9-]+)+$'# especifica el formato que se debe seguir
        result = re.match(patron, correo)#verifica si el correo cumple con dichas condiciones para ser correo
        if result:
            return {"success":True, "message":"¡Correo Valido!"}
        else:
            return {"success":False,"message":"Asegúrese que el correo sea válido,\nque no tenga mayúsculas y que el dominio este correcto.\nEjemplo:\n\templeado@example.com"}
    
    def verificarContraseña(self,contraseña):
        contrasena = str(contraseña)
        if len(contraseña) < 8 :
            return {"success":False,"message":f"¡La contraseña debe ser mínimo de 8 caracteres!"}
        elif not contraseña.strip() or contraseña.find(' ') != -1:
            return {"success":False,"message":"¡La contraseña no debe llevar espacios!"}
        return {"success":True,"message":"La contraseña cumple con los caracteres mínimos"}
    
    def _contrasenaHash(self,contrasena):
        contrasena = str(contrasena).encode("utf-8")
        contrasena_hash = bcrypt.hashpw(contrasena,bcrypt.gensalt())
        return contrasena_hash
        
    def insertarUsuario(self, usuario: Usuario, id_perfil: int):
        contrasena = self._contrasenaHash(usuario.contrasena)
        usuario.contrasena = contrasena
        
        # Crear el usuario
        resultado_usuario = self.UserData.create_usuario(usuario)
        
        if resultado_usuario['success']:
            id_usuario = resultado_usuario['id_usuario']  # Suponiendo que el método devuelve el id del usuario creado
            
            # Asignar el perfil al usuario
            resultado_perfil = self.UserProfileData.create_usuario_perfil(id_usuario, id_perfil)
            
            if not resultado_perfil['success']:
                # Manejo de error si no se pudo asignar el perfil
                return {'success': False, 'message': 'Usuario creado, pero no se pudo asignar el perfil.'}
            
            return {'success': True, 'message': 'Usuario creado y perfil asignado correctamente.'}
        
        return resultado_usuario  # Retornar el resultado del intento de creación del usuario

    def modificarUsuario(self, usuario: Usuario):
        return self.UserData.update_usuario(usuario)

    def eliminarUsuario(self, id_usuario, id_usuario_perfil):
        resultado_perfil = self.UserProfileData.delete_usuario_perfil(id_usuario_perfil)
        
        if not resultado_perfil['success']:
            return {'success': False, 'message': 'No se pudo eliminar el perfil del usuario antes de eliminar el usuario.'}
        
        resultado_usuario = self.UserData.delete_usuario(id_usuario)
        
        return resultado_usuario

    def obtenerListaUsuarios(self, pagina=1, tam_pagina=10, ordenar_por="Id", tipo_orden="ASC", busqueda=None):
        return self.UserData.list_usuarios(pagina, tam_pagina, ordenar_por, tipo_orden, busqueda)

    def obtenerUsuarioPorId(self, id_usuario):
        pass

    def iniciar_sesion(self, identificador, contrasena):
        resultado = self.UserData.verificar_usuario_contrasena(identificador, contrasena)
        return resultado
