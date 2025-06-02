import time
from settings.config import ZKTECA_CONFIG
from settings.logger import logger
from zk import ZK
from datetime import date
from datetime import time as dt_time

from services.huellaService import HuellaService

from typing import Optional, List, Union, Tuple
from Utils.Utils import parse_date, parse_time
from models.huella import Huella
import re
import traceback


class ZKServices:

    huellaService = HuellaService()

    def __init__(self):

        self.zk = ZK(ZKTECA_CONFIG["host"], ZKTECA_CONFIG["port"])

    # obteniendo huella
    def obtener_huella(self, id_empleado):
        try:
            conexion = self.zk.connect()
            listHuella = conexion.get_templates()
            huella = list(filter(lambda f: f.uid == id_empleado, listHuella)) or None
            conexion.disconnect()
            return {"success": True, "huella": huella[0] if huella else huella}
        except Exception as e:
            return {
                "success": False,
                "message": "Ocurrio un error al obtener la huella",
            }

    # registrar empleado con huella
    def registrar_empleado_con_huella(self, id_empleado: int, nombre: str, cedula: str):
        try:
            conn = self.zk.connect()
            conn.enable_device()

            conn.set_user(uid=id_empleado, name=f"{nombre}-{cedula}")
            time.sleep(1)

            conn.enroll_user(uid=id_empleado, temp_id=9)

            start_time = time.time()
            while (time.time() - start_time) < 30:
                templates = conn.get_templates()
                huella = list(filter(lambda t: t.uid == id_empleado, templates)) or None
                if huella:
                    conn.test_voice(0)
                    return {
                        "success": True,
                        "message": "Se registro con exito el empleado.",
                        "huella_id_ZK": huella[0].uid,
                    }
                time.sleep(0.5)

            return {
                "success": True,
                "message": "Se registro el empleado pero sin huella.",
                "huella_id_ZK": None,
            }
        except Exception as e:
            logger.error(f"{e}")
            return {
                "success": False,
                "message": f"Ocurrio un error al registrar el empleado.",
            }

    def obtener_asistencias(
        self,
        id_empleado: Optional[int] = None,
        fecha: Optional[Union[date, str]] = None,
        rango_fechas: Optional[Union[Tuple[date, date], List[str]]] = None,
    ):
        try:
            if fecha:
                if isinstance(fecha, str):
                    fecha = parse_date(fecha)
            if rango_fechas:
                if isinstance(rango_fechas, list):
                    if len(rango_fechas) != 2:
                        return {
                            "success": False,
                            "message": "El rango de fechas debe contener exactamente 2 elementos",
                        }
                    rango_fechas = (
                        parse_date(rango_fechas[0]),
                        parse_date(rango_fechas[1]),
                    )

                if rango_fechas[0] > rango_fechas[1]:
                    return {
                        "success": False,
                        "message": "La primera fecha del filtro debe ser menor o igual a la ultima fecha.",
                    }

            conn = self.zk.connect()

            conn.disable_device()

            asistencias = conn.get_attendance()
            users = conn.get_users()

            filtered = []
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
                empleado = (
                    list(filter(lambda e: str(e.user_id) == str(asist.user_id), users))
                    or None
                )
                if empleado:
                    filtered.append((empleado[0], asist))

            conn.enable_device()
            conn.disconnect()
            return {
                "success": True,
                "message": "Se obtuvieron las asistencias.",
                "asistencias": filtered,
            }
        except Exception as e:
            logger.error(f"{e}")
            return {
                "success": False,
                "message": "Ocurrio un erro al obtener la asistencias",
            }

    def actualizar_empleado(self, id_em: int, nombre: str, cedula: str):
        try:
            conn = self.zk.connect()
            conn.enable_device()

            # Actualizar los datos del empleado
            conn.set_user(uid=id_em, name=f"{nombre}-{cedula}")
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
                    return {
                        "success": True,
                        "message": "Empleado actualizado con éxito.",
                        "huella_id_ZK": huella[0].uid,
                    }
                time.sleep(0.5)

            conn.disconnect()
            return {
                "success": True,
                "message": "Empleado actualizado pero sin huella.",
                "huella_id_ZK": None,
            }
        except Exception as e:
            logger.error(f"{e}")
            return {
                "success": False,
                "message": "Ocurrió un error al actualizar el empleado.",
            }

    def obtener_usuarios(self, id_empleado=None):
        try:
            conn = self.zk.connect()  # Conectar al dispositivo
            # Obtener todos los usuarios
            usuarios = conn.get_users()
            if id_empleado:
                usuarios = (
                    list(filter(lambda u: u.uid == id_empleado, usuarios)) or None
                )
            return {
                "success": True,
                "message": "Se obtuvieron los usuarios.",
                "usuarios": usuarios,
            }
        except Exception as e:
            logger.error(e)
            return {
                "success": False,
                "message": "Ocurrio un error al obtener usuarios.",
            }
        finally:
            if conn:
                conn.disconnect()

    def obtener_usuarios_y_huellas(self):
        # Dirección IP y puerto del dispositivo ZKTeco K20
        ip = "192.168.1.201"  # Dirección IP del dispositivo de huella
        puerto = 4370  # Puerto del dispositivo

        # Crear una instancia de ZK
        zk = ZK(ip, puerto, timeout=5, force_udp=False)

        try:
            zk.connect()  # Conectar al dispositivo
            print("Conectado al dispositivo de huella.")

            # Obtener todos los usuarios
            usuarios = zk.get_users()
            for usuario in usuarios:
                print(
                    f"ID: {usuario.uid}, Nombre: {usuario.name}, Privilegio: {usuario.privilege}, User ID: {usuario.user_id}"
                )

                # Obtener las huellas del usuario
                huellas = zk.get_templates()
                huellas_usuario = list(filter(lambda f: f.uid == usuario.uid, huellas))
                if huellas_usuario:
                    print(f"  Huellas para el usuario {usuario.name}:")
                    for huella in huellas_usuario:
                        print(f"    Huella ID: {huella.fid}, Valida: {huella.valid}")
                else:
                    print(
                        f"  No se encontraron  huellas para el usuario {usuario.name}."
                    )

        except Exception as e:
            print(f"Error al conectar al dispositivo: {e}")
        finally:
            zk.disconnect()  # Desconectar cuando termine
            print("Desconectado del dispositivo.")

    # En la clase ZKServices, modificar el método registrar_empleado_con_huella
    def registrar_empleado_con_huella(self, id_empleado: int, nombre: str, cedula: str):
        try:
            conn = self.zk.connect()
            conn.enable_device()

            # Primero registrar el usuario con nombre y cédula
            conn.set_user(uid=id_empleado, name=f"{nombre}-{cedula}")
            time.sleep(1)

            # Luego registrar la huella
            conn.enroll_user(
                uid=id_empleado, temp_id=9
            )  # temp_id=9 para registro de huella

            start_time = time.time()
            while (time.time() - start_time) < 30:
                templates = conn.get_templates()
                huella = list(filter(lambda t: t.uid == id_empleado, templates)) or None
                if huella:
                    # Guardar información adicional en el dispositivo
                    try:
                        # Almacenar datos adicionales en el dispositivo (si soporta esta característica)
                        user = conn.get_user(uid=id_empleado)
                        if user:
                            # Algunos dispositivos permiten almacenar datos adicionales en el campo 'name'
                            conn.set_user(uid=id_empleado, name=f"{nombre}-{cedula}")
                    except Exception as e:
                        logger.error(f"Error al guardar datos adicionales: {e}")

                    conn.test_voice(0)  # Sonido de confirmación
                    return {
                        "success": True,
                        "message": "Empleado registrado con huella exitosamente.",
                        "huella_id_ZK": huella[0].uid,
                        "nombre": nombre,
                        "cedula": cedula,
                    }
                time.sleep(0.5)

            return {
                "success": True,
                "message": "Empleado registrado pero sin huella.",
                "huella_id_ZK": None,
                "nombre": nombre,
                "cedula": cedula,
            }
        except Exception as e:
            logger.error(f"{e}")
            return {
                "success": False,
                "message": f"Error al registrar empleado: {str(e)}",
            }

    def obtener_info_empleado(self, id_empleado: int):
        try:
            conn = self.zk.connect()
            user = conn.get_user(uid=id_empleado)
            conn.disconnect()

            if user:
                # Extraer nombre y cédula del campo 'name' (formato: "nombre-cedula")
                nombre_cedula = user.name.split("-")
                if len(nombre_cedula) == 2:
                    nombre = nombre_cedula[0]
                    cedula = nombre_cedula[1]
                else:
                    nombre = user.name
                    cedula = "No registrada"

                return {
                    "success": True,
                    "nombre": nombre,
                    "cedula": cedula,
                    "user_id": user.user_id,
                    "privilege": user.privilege,
                }
            return {"success": False, "message": "Empleado no encontrado"}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def registrar_empleado_completo(self, nombre: str, cedula: str):
        """Registra un empleado con nombre, cédula y huella en el dispositivo"""
        try:
            # Generar ID válido (1-65535)
            id_empleado = self._generar_id_valido(cedula)

            conn = self.zk.connect()
            conn.enable_device()

            # 1. Registrar usuario básico
            conn.set_user(
                uid=id_empleado,
                name=f"{nombre} ({cedula})",  # Nombre y cédula
                privilege=0,  # Usuario normal
                password="",
                group_id=0,
                user_id=id_empleado,
            )
            time.sleep(1)  # Pausa para asegurar registro

            # 2. Capturar huella digital
            conn.enroll_user(uid=id_empleado, temp_id=0)  # temp_id 0 para primer dedo

            # 3. Esperar y verificar huella
            start_time = time.time()
            while (time.time() - start_time) < 30:  # 30 segundos de espera
                templates = conn.get_templates()
                if any(t.uid == id_empleado for t in templates):
                    conn.test_voice(0)  # Sonido de confirmación
                    return {
                        "success": True,
                        "message": "Registro completo exitoso",
                        "user_id": id_empleado,
                        "huella_registrada": True,
                    }
                time.sleep(0.5)

            return {
                "success": True,
                "message": "Usuario registrado sin huella",
                "user_id": id_empleado,
                "huella_registrada": False,
            }

        except Exception as e:
            logger.error(f"Error en registro: {str(e)}")
            return {"success": False, "message": f"Error en dispositivo: {str(e)}"}
        finally:
            if "conn" in locals():
                conn.disconnect()

    def _generar_id_valido(self, cedula: str) -> int:
        """Genera un ID de usuario válido para dispositivos ZKTeco"""
        try:
            # Intentar usar la cédula como base
            if cedula.isdigit():
                id_usuario = int(cedula) % 65535  # Asegurar rango
                return max(1, id_usuario)  # Nunca cero
            # Si la cédula no es numérica, usar timestamp
            return int(time.time()) % 65535 or 1
        except:
            return 1  # Valor por defecto seguro

    def registrar_empleado_simple(self, nombre: str, id_empleado: int, bandera: bool):
        if bandera: 
                self.eliminar_huella_por_nombre(nombre)
        conn = None
        try:
            logger.info("Intentando conectar y habilitar el dispositivo.")
            conn = self.zk.connect()
            conn.enable_device()
            logger.info("Dispositivo habilitado.")

            

            # Registrar al usuario
            conn.set_user(uid=id_empleado, name=nombre)
            time.sleep(1)  # Esperar para asegurar el registro

            # Intentar registrar huella
            conn.enroll_user(uid=id_empleado)

            # Esperar hasta 30 segundos por la huella
            start_time = time.time()
            while time.time() - start_time < 30:
                templates = conn.get_templates()
                huella = next((t for t in templates if t.uid == id_empleado), None)
                if huella:
                    conn.test_voice(0)
                    nueva_huella = Huella(id_empleado, id_empleado=id_empleado)
                    self.huellaService.insertarHuella(nueva_huella)
                    return {
                        "success": True,
                        "huella_registrada": True,
                        "message": "Huella registrada con éxito.",
                    }
                time.sleep(0.5)

            # Si llegamos aquí es que no se registró la huella
            return {
                "success": True,
                "huella_registrada": False,
                "message": "Empleado registrado pero no se capturó huella digital",
            }

        except Exception as e:
            logger.error(f"Error en registrar_empleado_simple: {e}")
            return {
                "success": False,
                "message": str(e),
            }
        finally:
            if conn:
                try:
                    conn.disconnect()
                except:
                    pass
        
    def verificar_conexion(self) -> bool:
        try:
            # Intenta conectar al dispositivo
            conexion = self.zk.connect(timeout=5)
            # Si la conexión es exitosa, desconectar y retornar True
            conexion.disconnect()
            return True
        except Exception as e:
            # Si ocurre un error, registrar el error y retornar False
            logger.error(f"Error al verificar conexión: {e}")
            return False
        
    def verificar_huella_por_nombre(self, nombre: str) -> bool:
        try:
            conn = self.zk.connect(timeout=5)
            
            # Obtener todos los usuarios
            usuarios = conn.get_users()
            
            # Buscar usuario por nombre (el nombre en ZKTeco suele estar en formato "nombre-cedula")
            usuario = next((u for u in usuarios if nombre.lower() in u.name.lower()), None)
            
            if not usuario:
                return False
                
            # Obtener todas las huellas
            huellas = conn.get_templates()
            
            # Verificar si hay huellas para este usuario
            tiene_huella = any(h.uid == usuario.uid for h in huellas)
            
            return tiene_huella
            
        except Exception as e:
            logger.error(f"Error al verificar huella por nombre: {str(e)}")
            return False
        finally:
            if 'conn' in locals():
                conn.disconnect()

    def eliminar_huella_por_nombre(self, nombre: str) -> bool:
        try:
            conn = self.zk.connect(timeout=5)
            conn.enable_device()
            
            # Buscar usuario
            usuario = next((u for u in conn.get_users() if nombre.lower() in u.name.lower()), None)
            if not usuario:
                return False
            
            # Eliminar huellas solo si existen
            huellas_usuario = [h for h in conn.get_templates() if h.uid == usuario.uid]
            if huellas_usuario:
                for huella in huellas_usuario:
                    conn.delete_user_template(uid=usuario.uid, temp_id=huella.fid)
            
            # Eliminar usuario (esto funciona aunque no tenga huellas)
            conn.delete_user(uid=usuario.uid)
            conn.refresh_data()
            
            return True
            
        except Exception as e:
            logger.error(f"Error eliminando usuario {nombre}: {str(e)}")
            return False
        finally:
            if 'conn' in locals():
                conn.disconnect()
                
            
