import os
import sys
from datetime import date
import random
import string
import time
import uuid
from locust import User, task, between, SequentialTaskSet, events

# --- Ajuste de ruta para localizar el paquete 'src' ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, os.pardir, os.pardir))
src_path = os.path.join(project_root, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Asegúrate de que las siguientes importaciones apunten a tus clases reales
from src.services.justificacionService import JustificacionServices
from src.models.justificacion import Justificacion

# --- Funciones de Ayuda ---
def generate_random_string(length, pattern=r"^[A-Za-z\s]+$"):
    """
    Genera un string aleatorio que cumple con el patrón especificado.
    """
    return ''.join(random.choices(string.ascii_letters + ' ', k=length))

class UserBehavior(SequentialTaskSet):
    """
    Define el comportamiento secuencial de un usuario.
    SequentialTaskSet asegura que las tareas se ejecuten en el orden definido.
    """
    def on_start(self):
        """ Se ejecuta al inicio de cada usuario virtual. """
        self.service = JustificacionServices()
        self.last_inserted_justificacion_id = None
        self.user_session_id = str(uuid.uuid4())

    @task(1)
    def insert_justificacion(self):
        """ Simula la inserción de una justificación directamente a través del servicio. """
        operation_name = "Insertar Justificación (DB)"
        motivo = generate_random_string(50)
        descripcion = generate_random_string(100)
        tipo = random.choice(["Permiso", "Falta justificada", "Vacaciones"])
        
        justificacion_data = Justificacion(
            id_empleado=1,  # ID de empleado fijo para pruebas (ajustar según tu caso)
            id_asistencia=1,  # ID de asistencia fijo para pruebas (ajustar según tu caso)
            fecha=date.today(),
            motivo=motivo,
            descripcion=descripcion,
            tipo=tipo,
            id_justificacion=None  # ID será generado por la base de datos
        )

        start_time = time.perf_counter()
        exception = None
        try:
            response = self.service.insertarJustificacion(justificacion_data)
            success = response.get("success", False)
            if success:
                self.last_inserted_justificacion_id = justificacion_data.id_justificacion
            else:
                exception = Exception(response.get("message", "Error desconocido en inserción"))
        except Exception as e:
            exception = e

        end_time = time.perf_counter()
        response_time_ms = (end_time - start_time) * 1000

        events.request.fire(
            request_type="CUSTOM",
            name=operation_name,
            response_time=response_time_ms,
            response_length=len(str(response)) if 'response' in locals() else 0,
            exception=exception,
            context={"user_id": self.user_session_id}
        )

    @task(1)
    def query_justificaciones(self):
        """ Simula la consulta de justificaciones directamente a través del servicio. """
        operation_name = "Consultar Lista Justificaciones (DB)"
        search_term = generate_random_string(10) if not self.last_inserted_justificacion_id else None

        start_time = time.perf_counter()
        exception = None
        try:
            response = self.service.obtenerListaJustificacion(
                pagina=1,
                tam_pagina=10,
                ordenar_por="fecha",
                tipo_orden="DESC",
                busqueda=search_term
            )
            success = response.get("success", False)
            if not success:
                exception = Exception(response.get("message", "Error desconocido en consulta"))
        except Exception as e:
            exception = e

        end_time = time.perf_counter()
        response_time_ms = (end_time - start_time) * 1000

        events.request.fire(
            request_type="CUSTOM",
            name=operation_name,
            response_time=response_time_ms,
            response_length=len(str(response)) if 'response' in locals() else 0,
            exception=exception,
            context={"user_id": self.user_session_id}
        )

class MyDbUser(User):
    """
    Representa un usuario simulado que interactúa directamente con la DB a través de servicios.
    """
    host = "local_db_connection"
    wait_time = between(1, 2)
    tasks = [UserBehavior]