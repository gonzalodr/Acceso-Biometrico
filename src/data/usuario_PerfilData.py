from data.data import conection     #obtener la conexion
from settings.tablas import (TBUSUARIOPERFIL,TBUSUARIOPERFIL_ID,
                             TBUSUARIOPERFIL_ID_USER,TBUSUARIOPERFIL_ID_PERF)      #obtener los nombres de tablas
from settings.logger import logger  #recolectar los errores 
from mysql.connector import Error   #controlador de errores
'''
    Conexion a la tabla de la relacion 
    de usuario y perfil.

    CONSTANTES DE NOMBRE DE LA COLUMNA DE LA TABLA:

    TBUSUARIOPERFIL         = 'usuario_perfil'
    TBUSUARIOPERFIL_ID      = 'Id'
    TBUSUARIOPERFIL_ID_USER = 'Id_Usuario'
    TBUSUARIOPERFIL_ID_PERF = 'Id_Perfil'
'''
class UsuarioPerfilData:
    def create_usuario_perfil(self, id_usuario:int, id_perfil:int, conexionEx = None):
        if conexionEx is None:
            conexion, resultado = conection()
            if not resultado["success"]:
                return resultado
        else:
            conexion = conexionEx
        
        try:
            with conexion.cursor() as cursor:
                query = f''' INSERT INTO {TBUSUARIOPERFIL} (
                            {TBUSUARIOPERFIL_ID_PERF}
                            {TBUSUARIOPERFIL_ID_USER}
                            ) VALUES ( %s , %s )
                        '''
                cursor.execute(query,(id_perfil,id_usuario))
                id_userPerfil = cursor.lastrowid
                if conexionEx is None:
                    conexion.commit()
                
                return {'success':True, 'message':'Se asigno el perfil al usuario correctamente.','id_usuarioPerfil':id_userPerfil}
        except Error as e:
            logger.error(f'{e}')
            return {'success':False, 'message':'Ocurrio un error al asignar el perfil al usuario.'}
        finally:
            if conexion and conexionEx is None:
                conexion.close()
  
    def update_usuario_perfil(self, id_usuarioPerfil:int, id_usuario:int, id_perfil:int,  conexionEx = None):
        if conexionEx is None:
            conexion, resultado = conection()
            if not resultado["success"]:
                return resultado
        else:
            conexion = conexionEx
        try:
            with conexion.cursor() as cursor:
                query = f''' UPDATE {TBUSUARIOPERFIL} SET
                        {TBUSUARIOPERFIL_ID_PERF} = %s,
                        {TBUSUARIOPERFIL_ID_USER} = %s
                        WHERE {TBUSUARIOPERFIL_ID} = %s '''
                cursor.execute(query,(id_perfil,id_usuario,id_usuarioPerfil))
                if conexionEx is None:
                    conexion.commit()
                return {'success':True, 'message':'Se actualizo el perfil asignado correctamente.'}
        except Error as e:
            logger.error(f'{e}')
            return {'success':False, 'message':'Ocurrio un error al actualizar el perfil del usuario.'}
        finally:
            if conexion and conexionEx is None:
                conexion.close()
    
    def delete_usuario_perfil(self,id_usuarioPerfil:int, conexionEx = None):
        if conexionEx is None:
            conexion, resultado = conection()
            if not resultado["success"]:
                return resultado
        else:
            conexion = conexionEx
        try:
            with conexion.cursor() as cursor:
                query = f'''DELETE FROM {TBUSUARIOPERFIL} WHERE {TBUSUARIOPERFIL_ID} = %s'''
                cursor.execute(query,(id_usuarioPerfil,))
                if conexionEx is None:
                    conexion.commit()
                return {'success':True, 'message':'Se elimino correctamente el perfil asignado al usuario.'}
        except Error as e:
            logger.error(f'{e}')
            return{'success':False, 'message':'Ocurrio un error al eliminar el perfil asignado al usuario.'}
        finally:
            if conexion and conexionEx is None:
                conexion.close()
        
    def get_usuario_perfil_by_id(self, id_usuarioPerfil:int):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        try:
            with conexion.cursor() as cursor:
                query=f'''SELECT 
                        {TBUSUARIOPERFIL_ID},
                        {TBUSUARIOPERFIL_ID_PERF},
                        {TBUSUARIOPERFIL_ID_USER}
                        FROM {TBUSUARIOPERFIL}
                        WHERE {TBUSUARIOPERFIL_ID} = %s'''
                
                cursor.execute(query,(id_usuarioPerfil,))
                data = cursor.fetchone()

                if data:
                    return {
                        'success':True,
                        'message':'Se obtuvo los datos del perfil usuario.',
                        'data':{
                            'id':data[0],
                            'id_perfil':data[1],
                            'id_usuario':data[2]
                        }
                    }
                else:
                    raise
        except Error as e:
            logger.error(f'{e}')
            return {'success':False,'message':'Ocurrio un error al obtener el perfil asignado al usuario'}
        finally:
            if conexion:
                conexion.close()