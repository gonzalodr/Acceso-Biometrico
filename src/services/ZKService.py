import time 
from settings.config import ZKTECA_CONFIG
from settings.logger import logger
from zk              import ZK
from datetime        import date
from datetime        import time as dt_time

from typing import Optional, List, Union, Tuple
from Utils.Utils     import parse_date, parse_time
import re
import traceback

class ZKServices:
    def __init__(self):
        self.zk = ZK(ZKTECA_CONFIG['host'],ZKTECA_CONFIG['port'])
    
    # obteniendo huella
    def obtener_huella(self, id_empleado):
        try:
            conexion = self.zk.connect()
            listHuella = conexion.get_templates()
            huella = list(filter(lambda f: f.uid == id_empleado, listHuella)) or None
            conexion.disconnect()
            return {'success':True, 'huella': huella[0] if huella else huella}
        except Exception as e:
            return {'success':False, 'message':'Ocurrio un error al obtener la huella'}

    #registrar empleado con huella
    def registrar_empleado_con_huella(self, id_empleado:int, nombre:str, cedula:str):
        try:
            conn = self.zk.connect()
            conn.enable_device()

            conn.set_user(uid = id_empleado, name = f'{nombre}-{cedula}')
            time.sleep(1)

            conn.enroll_user(uid = id_empleado, temp_id = 9)

            start_time = time.time()
            while (time.time() - start_time) < 30:
                templates = conn.get_templates()
                huella    = list(filter(lambda t: t.uid == id_empleado, templates)) or None
                if huella: 
                    conn.test_voice(0)
                    conn.disable_device()
                    return {'success':True,'message':'Se registro con exito el empleado.','huella_id_ZK':huella[0].uid}
                time.sleep(0.5)
                
            conn.disable_device()
            return {'success':True,'message':'Se registro el empleado pero sin huella.','huella_id_ZK':None}
        except Exception as e:
            logger.error(f'{e}')
            return {'success':False, 'message':f'Ocurrio un error al registrar el empleado.'}
    
    def obtener_asistencias(self, id_empleado: Optional[int]    = None, 
                        fecha: Optional[Union[date, str]]       = None,
                        rango_fechas: Optional[Union[Tuple[date, date], List[str]]] = None):
        try:
            if fecha:
                if isinstance(fecha, str):
                    fecha = parse_date(fecha)
            if rango_fechas:  
                if isinstance(rango_fechas, list):
                    if len(rango_fechas) != 2:
                        raise ValueError("El rango de fechas debe contener exactamente 2 elementos")
                    rango_fechas = (parse_date(rango_fechas[0]), parse_date(rango_fechas[1]))
                
                if rango_fechas[0] > rango_fechas[1]:
                    return {'success':False,'message':'La primera fecha del filtro debe ser menor o igual a la ultima fecha.'}

            conn        = self.zk.connect() 
            conn.disable_device()
            
            asistencias = conn.get_attendance()
            users       = conn.get_users()
            
            filtered    = []
            for asist in asistencias:
                asist_datetime = asist.timestamp
                
                # Filtro por ID de empleado
                if id_empleado and str(asist.user_id) != str(id_empleado):
                    continue
                # Filtro por fecha específica
                if fecha and asist_datetime.date() != fecha:
                    continue
                    
                # Filtro por rango de fechas
                if rango_fechas:
                    fecha_inicio, fecha_fin = rango_fechas
                    if not (fecha_inicio <= asist_datetime.date() <= fecha_fin):
                        continue
                # envia tanto el empleado al que le pertenece la asistencia como la misma asistencias
                empleado    = list(filter(lambda e: str(e.user_id) ==  str(asist.user_id),users)) or None
                if empleado:
                    filtered.append((empleado[0],asist))
                    
            conn.enable_device()
            conn.disconnect()
            return {'success':True, 'message':'Se obtuvieron las asistencias.','asistencias':filtered}
        except Exception as e:
            logger.error(f'{e}')
            return {'success':False, 'message':'Ocurrio un erro al obtener la asistencias'}
    
    def actualizar_empleado(self, id_em: int, nombre: str, cedula: str):
        try:
            conn = self.zk.connect()
            conn.enable_device()

            # Actualizar los datos del empleado
            conn.set_user(uid = id_em, name = f'{nombre}-{cedula}')
            time.sleep(1)

            # Aquí decidimos si también actualizamos la huella, si es necesario
            conn.enroll_user(uid=id_em, temp_id=9)

            start_time = time.time()
            while (time.time() - start_time) < 30:
                templates = conn.get_templates()
                huella = list(filter(lambda t: t.uid == id_em, templates)) or None

                if huella:
                    conn.test_voice(0)
                    conn.disconnect()
                    return {'success': True, 'message': 'Empleado actualizado con éxito.', 'huella_id_ZK': huella[0].uid}
                time.sleep(0.5)

            conn.disconnect()
            return {'success': True, 'message': 'Empleado actualizado pero sin huella.', 'huella_id_ZK': None}
        except Exception as e:
            logger.error(f'{e}')
            return {'success': False, 'message': 'Ocurrió un error al actualizar el empleado.'}
        
    def obtener_usuarios(self):
        # Dirección IP y puerto del dispositivo ZKTeco K20
        ip = '192.168.1.201'  # Dirección IP del dispositivo de huella
        puerto = 4370  # Puerto del dispositivo

        # Crear una instancia de ZK
        zk = ZK(ip, puerto, timeout=5, force_udp=False)

        try:
            zk.connect()  # Conectar al dispositivo
            print("Conectado al dispositivo de huella.")

            # Obtener todos los usuarios
            usuarios = zk.get_users()
            for usuario in usuarios:
                print(usuario)
                print(f"ID: {usuario.uid}, Nombre: {usuario.name}, Privilegio: {usuario.privilege}, User ID: {usuario.user_id}")

        except Exception as e:
            print(f"Error al conectar al dispositivo: {e}")
        finally:
            zk.disconnect()  # Desconectar cuando termine
            print("Desconectado del dispositivo.")

    def obtener_usuarios_y_huellas(self):
        # Dirección IP y puerto del dispositivo ZKTeco K20
        ip = '192.168.1.201'  # Dirección IP del dispositivo de huella
        puerto = 4370  # Puerto del dispositivo

        # Crear una instancia de ZK
        zk = ZK(ip, puerto, timeout=5, force_udp=False)

        try:
            zk.connect()  # Conectar al dispositivo
            print("Conectado al dispositivo de huella.")

            # Obtener todos los usuarios
            usuarios = zk.get_users()
            for usuario in usuarios:
                print(f"ID: {usuario.uid}, Nombre: {usuario.name}, Privilegio: {usuario.privilege}, User ID: {usuario.user_id}")

                # Obtener las huellas del usuario
                huellas = zk.get_templates()
                huellas_usuario = list(filter(lambda f: f.uid == usuario.uid, huellas))
                if huellas_usuario:
                    print(f"  Huellas para el usuario {usuario.name}:")
                    for huella in huellas_usuario:
                        print(f"    Huella ID: {huella.fid}, Valida: {huella.valid}")
                else:
                    print(f"  No se encontraron huellas para el usuario {usuario.name}.")

        except Exception as e:
            print(f"Error al conectar al dispositivo: {e}")
        finally:
            zk.disconnect()  # Desconectar cuando termine
            print("Desconectado del dispositivo.")
        
    def registrar_empleado_con_huella(self, id_empleado: int, nombre: str):
    # Dirección IP y puerto del dispositivo ZKTeco K20
        ip = '192.168.1.201'  # Dirección IP del dispositivo de huella
        puerto = 4370  # Puerto del dispositivo

        # Crear una instancia de ZK
        zk = ZK(ip, puerto, timeout=5, force_udp=False)
        try:
            conn = self.zk.connect()
            conn.enable_device()

            # Establecer el usuario en el dispositivo
            conn.set_user(uid=id_empleado, name=f'{nombre}')
            time.sleep(1)

            # Iniciar el proceso de enrolamiento de la huella
            conn.enroll_user(uid=id_empleado, temp_id=6)

            start_time = time.time()
            while (time.time() - start_time) < 30:
                templates = conn.get_templates()
                huella = list(filter(lambda t: t.uid == id_empleado, templates)) or None
                if huella:
                    conn.test_voice(0)  # Reproducir un sonido de éxito
                    # Crear una instancia de Huella
                    #nueva_huella = Huella(id_huella=str(huella[0].fid), nombre=nombre, userID=str(id_empleado))
                    return {
                        'success': True,
                                'message': 'Se registró con éxito el empleado.',
                                'huella_id_ZK': huella[0].fid,
                                #'huella_info': str(nueva_huella)  # Información de la huella
                        }
                time.sleep(0.5)

            return {
                    'success': True,
                    'message': 'Se registró el empleado pero sin huella.',
                    'huella_id_ZK': None
                }
        except Exception as e:
                logger.error(f'{e}')
                return {
                    'success': False,
                    'message': 'Ocurrió un error al registrar el empleado.'
                }