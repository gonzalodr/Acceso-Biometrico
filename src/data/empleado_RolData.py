from data.data import conection     #obtener la conexión
from settings.tablas import (TBROLEMPLEADO,TBROLEMPLEADO_ID,
                            TBROLEMPLEADO_ID_EMPLEADO,TBROLEMPLEADO_ID_ROL)     #obtener los nombres de tablas
from settings.logger import logger  #recolectar los errores 
from mysql.connector import Error   #controlador de errores

from data.rolData import RolData

from models.rol import Rol
'''
    Conexión a la tabla de la relación 
    de empleado y rol.

    CONSTANTES DE NOMBRE DE LA COLUMNA DE LA TABLA:

    TBROLEMPLEADO               = 'empleado_rol'
    TBROLEMPLEADO_ID            = 'Id'
    TBROLEMPLEADO_ID_EMPLEADO   = 'Id_Empleado'
    TBROLEMPLEADO_ID_ROL        = 'Id_Rol'
'''
class EmpleadoRolData:
    def __init__(self):
        self.roldata = RolData()

    def create_rol_empleado(self, id_empleado:int, id_rol:int, conexionEx = None):
        conexion, resultado = conection() if conexionEx is None else (conexionEx, {"success": True})
        if not resultado["success"]:
            return resultado
        
        try:
            with conexion.cursor() as cursor:
                query=f''' INSERT INTO {TBROLEMPLEADO} (
                        {TBROLEMPLEADO_ID_ROL},
                        {TBROLEMPLEADO_ID_EMPLEADO}                        
                        ) VALUES(%s,%s)
                    '''
                cursor.execute(query,(id_rol,id_empleado))
                id_rolempleado = cursor.lastrowid

                if conexionEx is None:
                    conexion.commit()
                return {'success':True, 'message':'Se asigno el rol al empleado correctamente','id_rolempleado':id_rolempleado}
        except Error as e:
            logger.error(f'{e}')
            return {'success':False, 'message':'Ocurrió un error al asignar el rol al empleado'}
        finally:
            if conexion and conexionEx is None:
                conexion.close()

    def update_rol_empleado(self, id_rolEmpleado:int, id_empleado:int, id_rol:int, conexionEx = None):
        conexion, resultado = conection() if conexionEx is None else (conexionEx, {"success": True})
        if not resultado["success"]:
            return resultado

        try:
            with conexion.cursor() as cursor:
                query = f'''UPDATE {TBROLEMPLEADO} SET
                        {TBROLEMPLEADO_ID_ROL} =%s,
                        {TBROLEMPLEADO_ID_EMPLEADO} = %s
                        WHERE {TBROLEMPLEADO_ID} = %s
                        '''
                cursor.execute(query,(id_rol, id_empleado, id_rolEmpleado))

                if conexionEx is None:
                    conexion.commit()

                return {'success':True, 'message':'Se actualizo el rol del empleado.'}

        except Error as e:
            logger.error(f'{e}')
            return {'success':False,'message':'Ocurrió un error al actualizar el rol del empleado.'}
        finally:
            if conexion and conexionEx is None:
                conexion.close()

    def delete_rol_empleado(self, id_rolempleado:int, conexionEx = None):
        conexion, resultado = conection() if conexionEx is None else (conexionEx, {"success": True})
        if not resultado["success"]:
            return resultado
        
        try:
            with conexion.cursor() as cursor:
                query = f'''DELETE FROM {TBROLEMPLEADO} WHERE {TBROLEMPLEADO_ID} = %s'''
                cursor.execute(query,(id_rolempleado,))

                if conexionEx is None:
                    conexion.commit()
                return {'success':True, 'message':'Se elimino el rol asignado al empleado correctamente.'}                
        except Error as e:
            logger.error(f'{e}')
            return {'success':False, 'message':'Ocurrió un error al eliminar el rol asignado al empleado.'}
        finally:
            if conexion and conexionEx is None:
                conexion.close()

    def get_rol_empleado_by_id(self,id_rolempleado:int, conexionEx = None):
        conexion, resultado = conection() if conexionEx is None else (conexionEx, {"success": True})
        if not resultado["success"]:
            return resultado

        try:
            with conexion.cursor(dictionary = True) as cursor:
                query = f'''SELECT 
                        {TBROLEMPLEADO_ID},
                        {TBROLEMPLEADO_ID_ROL},
                        {TBROLEMPLEADO_ID_EMPLEADO}
                        FROM {TBROLEMPLEADO}
                        WHERE {TBROLEMPLEADO_ID} = %s'''
                cursor.execute(query,(id_rolempleado,))
                data = cursor.fetchone()
                if data:
                    return {
                        'success':True,
                        'exists':True,
                        'message':'Se obtuvo los datos del rol empleado.',
                        'rolEmpleado':{
                            'id': data[0],
                            'id_rol':data[1],
                            'id_empleado':data[2]
                        }
                    }
                else:
                    return {'success':True,'exists':False,'message':'No se obtuvo los datos del rol empleado.'}
        except Error as e:
            logger.error(f'{e}')
            return {'success':False,'message':'Ocurrió un error al obtener el rol asignado del empleado'}
        finally:
            if conexion and conexionEx is None:
                conexion.close()