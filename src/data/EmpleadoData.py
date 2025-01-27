from data.data import conection     #obtener la conexion
from settings.tablas import *       #obtener los nombres de tablas
from settings.logger import logger  #recolectar los errores 


#importando clases
from typing import Dict, Any        #clase diccionario
from models.persona import Persona  #clase persona
from models.usuario import Usuario  #clase usuario

#importando la clases data de usuarioData y personaData
from data.personaData import PersonaData
from data.usuarioData import UsuarioData

class EmpleadoData:
    def __init__(self):
        self.personadata = PersonaData()
        self.usuariodata = UsuarioData()

    def create_Empleado(self, datos: Dict[str, Any])->Dict[str,Any]:
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        
        try:
            persona:Persona = datos.get('persona')
            usuario:Usuario = datos.get('usuario')

            id_dep:int = datos.get('id_departamento') if datos.get('id_departamento') else None
            id_rol:int = datos.get('id_rol') if datos.get('id_rol') else None
            id_per:int = datos.get('id_perfil') if datos.get('id_perfil') else None #perfils

            #registrando la persona
            result = self.personadata.create_persona(persona,conexion)
            if not result['success']:
                conexion.rollback()
                return result
            id_persona = result['id_persona'] #optenemos el id

            #registrando empleado
            result = self.registrar_empleado(id_persona,id_dep,conexion)
            if not result['success']:
                conexion.rollback()
                return result
            id_empleado = result['id_empleado']

            #registrando rol empleado
            if id_rol:
                pass

            #ingresando el usuario
            if usuario:
                usuario.id_persona = id_persona
                result = self.usuariodata.create_usuario(usuario,conexion)
                if not result['success']:
                    conexion.rollback()
                    return result
                id_usuario = result['id_usuario']
                #registrando el perfil


            #confirmando los registros
            conexion.commit()
            
        except Exception as e:
            conexion.rollback()
            logger.error(f'{e}') 
            return {'success':False, 'message':f'Ocurrio un error al registrar el empleado'}
        finally:
            if conexion:
                conexion.close()
    '''
    Creando registro empleado
    '''
    def registrar_empleado(self, id_persona:int, id_departamento:int, conexionEx = None)->Dict[str,Any]:
        if conexionEx is None:
            conexion, resultado = conection()
            if not resultado["success"]:
                return resultado
        else:
            conexion = conexionEx
        
        try:
            with conexion.cursor() as cursor:
                queryEmpleado = f'''INSERT INTO {TBEMPLEADO} (
                    {TBEMPLEADO_PERSONA},
                    {TBEMPLEADO_DEPARTAMENTO}
                    )VALUES(%s, %s)
                '''
                cursor.execute(queryEmpleado,(id_persona, id_departamento))
                
                id_empleado = cursor.lastrowid
                if conexionEx is None:
                    conexion.commit()

                return {'success':True, 
                        'message':'Empleado registrado exitosamente',
                        'id_empleado':id_empleado 
                        }
        except Exception as e:
            logger.error(f'{e}')
            return {'success':False, 'message':'Ocurrio un error al registrar al empleado'}
        finally:
            if conexion and conexionEx is None:
                conexion.close()
    
    def registrar_rol(self, id_rol, id_empleado,conexionEx)->Dict[str,Any]:
        pass