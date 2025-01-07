from data.data import conection
from settings.tablas import *
from settings.logger import logger

from typing import Dict, Any
from models.persona import Persona
from models.usuario import Usuario




class EmpleadoData:
    
    def create_Empleado(datos: Dict[str, Any])->Dict[str,Any]:
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado

        try:
            persona:Persona = datos.get('persona')
            usuario:Usuario = datos.get('usuario')

            id_dep:int = datos.get('id_departamento') if datos.get('id_departamento') else None
            id_rol:int = datos.get('id_rol') if datos.get('id_rol') else None
            id_per:int = datos.get('id_perfil') if datos.get('id_perfil') else None

            with conexion.cursor() as cursor:
                #Primero insertamos la persona para crear el empleado
                queryPersona = f''' INSERT INTO {TBPERSONA}(
                                {TBPERSONA_FOTO} , 
                                {TBPERSONA_NOMBRE} ,  
                                {TBPERSONA_APELLIDOS} ,
                                {TBPERSONA_NACIMIENTO} ,
                                {TBPERSONA_CEDULA} ,
                                {TBPERSONA_ESTADO_CIVIL} ,
                                {TBPERSONA_CORREO} , 
                                {TBPERSONA_DIRECCION}) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
                cursor.execute(queryPersona,(
                    persona.foto,
                    persona.nombre,
                    persona.apellidos,
                    persona.fecha_nacimiento,
                    persona.cedula,
                    persona.estado_civil,
                    persona.correo,
                    persona.direccion
                ))

                id_persona = cursor.lastrowid   ##obtiene el id generado para dicho insert

                queryEmpleado = f''' INSERT INTO {TBEMPLEADO} (
                                {TBEMPLEADO_PERSONA},
                                {TBEMPLEADO_DEPARTAMENTO}
                            )
                            VALUES (%s,%s)
                '''
                cursor.execute(queryEmpleado,(id_persona,id_dep))

                id_empleado = cursor.lastrowid ## obtenemos el id generado para el empleado

                if id_rol:
                    queryRolEmpleado= f'''INSERT INTO {TBROLEMPLEADO} (
                                        {TBROLEMPLEADO_ID_EMPLEADO},
                                        {TBROLEMPLEADO_ID_ROL}
                                        )
                                        VALUES(%s,%s)
                                        '''
                    cursor.execute(queryRolEmpleado,(id_empleado,id_rol))

                if usuario:
                    queryUsuario=''''''
                    pass





        except Exception as e:
            conexion.rollback()
            logger.error(f'{e}') 
            return {'success':False, 'message':f'Ocurrio un error al registrar el empleado'}
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()