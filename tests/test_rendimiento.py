
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, os.pardir)
sys.path.insert(0, os.path.abspath(os.path.join(parent_dir, 'src')))

# locustfile.py
import random
import string
import time
from locust import User, task, between, SequentialTaskSet, events
import uuid

# Asegúrate de que las siguientes importaciones apunten a tus clases reales
from services.perfilService import PerfilServices
from models.perfil import Perfil
from models.permiso_perfil import Permiso_Perfil

# --- Funciones de Ayuda ---
def generate_unique_name():
    """
    Genera un nombre único de perfil alfabético.
    """
    length = 12
    return ''.join(random.choices(string.ascii_letters, k=length))

class UserBehavior(SequentialTaskSet):
    """
    Define el comportamiento secuencial de un usuario.
    SequentialTaskSet asegura que las tareas se ejecuten en el orden definido.
    """
    def on_start(self):
        """ Se ejecuta al inicio de cada usuario virtual. """
        self.service = PerfilServices()
        self.last_inserted_perfil_name = None
        self.user_session_id = str(uuid.uuid4()) 

    @task(1)
    def insert_perfil(self):
        """ Simula la inserción de un perfil directamente a través del servicio. """
        operation_name = "Insertar Perfil (DB)"
        perfil_name = generate_unique_name()
        perfil_data = Perfil(nombre=perfil_name, descripcion=f"Descripción de {perfil_name}")
        
        lista_permisos_mock = [
            Permiso_Perfil(perfil_id=None, tabla="usuarios", ver=True, crear=True, editar=False, eliminar=False),
            Permiso_Perfil(perfil_id=None, tabla="rol", ver=True, crear=True, editar=False, eliminar=False),
            Permiso_Perfil(perfil_id=None, tabla="permiso", ver=True, crear=True, editar=False, eliminar=False),
            Permiso_Perfil(perfil_id=None, tabla="perfil", ver=True, crear=True, editar=False, eliminar=False),
            Permiso_Perfil(perfil_id=None, tabla="justificacion", ver=True, crear=True, editar=False, eliminar=False),
            Permiso_Perfil(perfil_id=None, tabla="empleado", ver=True, crear=True, editar=False, eliminar=False)
        ]

        start_time = time.perf_counter()
        exception = None
        try:
            response = self.service.insertarPerfil(perfil_data, lista_permisos_mock)
            success = response.get("success", False)
            if success:
                self.last_inserted_perfil_name = perfil_name
            else:
                exception = Exception(response.get("message", "Error desconocido en inserción"))
        except Exception as e:
            exception = e

        end_time = time.perf_counter()
        response_time_ms = (end_time - start_time) * 1000

        # Corregida la línea de contexto aquí:
        events.request.fire(
            request_type="CUSTOM",
            name=operation_name,
            response_time=response_time_ms,
            response_length=len(str(response)) if 'response' in locals() else 0,
            exception=exception,
            context={"user_id": self.user_session_id} # ¡CORREGIDO!
        )

    @task(1)
    def query_perfiles(self):
        """ Simula la consulta de perfiles directamente a través del servicio. """
        operation_name = "Consultar Lista Perfiles (DB)"
        search_term = self.last_inserted_perfil_name if self.last_inserted_perfil_name else "example"

        start_time = time.perf_counter()
        exception = None
        try:
            response = self.service.obtenerListaPerfil(pagina=1, tam_pagina=10, busqueda=search_term)
            success = response.get("success", False)
            if not success:
                exception = Exception(response.get("message", "Error desconocido en consulta"))
        except Exception as e:
            exception = e
        
        end_time = time.perf_counter()
        response_time_ms = (end_time - start_time) * 1000

        # Corregida la línea de contexto aquí también:
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