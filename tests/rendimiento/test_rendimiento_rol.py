
import sys
import os

proyecto_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
ruta_src = os.path.join(proyecto_root, 'src')
if ruta_src not in sys.path:
    sys.path.insert(0, ruta_src)



# locustfile.py
import random
import string
import time
from locust import User, task, between, SequentialTaskSet, events
import uuid
from locust import HttpUser

# Asegúrate de que las siguientes importaciones apunten a tus clases reales
from services.rolService import RolServices
from models.rol import Rol

def generate_unique_name():
    return f"Rol_{uuid.uuid4().hex[:8]}"

class RolBehavior(SequentialTaskSet):
    def on_start(self):
        self.service = RolServices()
        self.last_inserted_rol_name = None
        self.user_session_id = str(uuid.uuid4())

    @task(1)
    def insert_rol(self):
        operation_name = "Insertar Rol (DB)"
        rol_name = generate_unique_name()
        rol_data = Rol(nombre=rol_name, descripcion=f"Rol generado por locust {rol_name}")

        start_time = time.perf_counter()
        exception = None
        try:
            response = self.service.insertarRol(rol_data)
            if response.get("success", False):
                self.last_inserted_rol_name = rol_name
            else:
                exception = Exception(response.get("message", "Error al insertar rol"))
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
    def query_roles(self):
        operation_name = "Consultar Lista Roles (DB)"
        search_term = self.last_inserted_rol_name or "admin"

        start_time = time.perf_counter()
        exception = None
        try:
            response = self.service.obtenerListaRol(pagina=1, tam_pagina=10, busqueda=search_term)
            if not response.get("success", False):
                exception = Exception(response.get("message", "Error al consultar roles"))
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
    host = "localhost"  # Cambia esto a tu host de base de datos si es necesario
    wait_time = between(1, 2)
    tasks = [RolBehavior]