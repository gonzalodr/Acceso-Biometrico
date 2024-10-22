import bcrypt 
from models.usuario import Usuario #llamando modulo `models` y a un archivo `usuario` para importar la clase `Usuario`


def _contrasenaHash(contrasena):
    contrasena = str(contrasena)
    if len(contrasena) < 8 :
        return False, f"¡La contraseña debe ser minimo de 8 caracteres!" 
    elif not contrasena.strip() or contrasena.find(' ') != -1:
        return False, "¡La contraseña no debe llevar espacios!"
    else:
        contrasena = contrasena.encode("utf-8")
        contrasena_hash = bcrypt.hashpw(contrasena,bcrypt.gensalt())
        return True, contrasena_hash 
    

def _verificarContrasenaHash(contrasena, contrasena_hash):
    contrasena = str(contrasena)
    contrasena = contrasena.encode("utf-8")
    if bcrypt.checkpw(contrasena, contrasena_hash):
        return True,"¡Inicio de sesión exitoso!"
    else:
        return False, "¡El usuario o contraseña es incorrecta!"    

def insertarUsuario(usuario: Usuario):
    exito, resultado = _contrasenaHash(usuario.contrasena) 
    if not exito:
        return exito,resultado
    else:
        usuario.contrasena = resultado.decode("utf-8")
        return exito, f"¡Usuario [{usuario.usuario}], Contraseña [{usuario.contrasena}]!"
    
    def insertarUsuario(self, usuario: Usuario):
        result = self._contrasenaHash(usuario.contrasena)
        if not result["success"]:
            return result
        
        usuario.contrasena = result["contrasena_hash"].decode("utf-8") 


        result = self._validarCorreo(usuario.correo)
        if not result["success"]:
            return result

        return self.usuarioData.create_usuario(usuario)
    
    def modificarUsuario(self, usuario: Usuario):

        result = self._validarCorreo(usuario.correo)
        if not result["success"]:
            return result
        
        # Modificar usuario
        return self.usuarioData.update_usuario(usuario)
    
    def eliminarUsuario(self, id_usuario):
        return self.usuarioData.delete_usuario(id_usuario)

    def obtenerListaUsuarios(self, pagina=1, tam_pagina=10, ordenar_por="Id", tipo_orden="ASC", busqueda=None):
        return self.usuarioData.list_usuarios(pagina, tam_pagina, ordenar_por, tipo_orden, busqueda)

    def obtenerUsuarioPorId(self, id_usuario):
        return self.usuarioData.get_usuario_by_id(id_usuario)



        def iniciar_sesion(self, identificador, contrasena):
        resultado = self.usuarioData.verificar_usuario_contrasena(identificador, contrasena)
        return resultado