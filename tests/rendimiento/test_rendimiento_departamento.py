import os
import sys

# --- Ajuste de ruta para localizar el paquete 'src' ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, os.pardir, os.pardir))
src_path = os.path.join(project_root, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

import random
import string
import time
import uuid
from locust import User, task, between, SequentialTaskSet, events

# Importa tus clases reales de Departamento
from services.departamentoService import DepartamentoServices
from models.departamento import Departamento

# --- Función auxiliar para nombres únicos ---
def generate_unique_name():
    """
    Genera un nombre único de departamento alfabético.
    """
    length = 12
    return ''.join(random.choices(string.ascii_letters, k=length))

class UserBehavior(SequentialTaskSet):
    """
    Comportamiento secuencial de un usuario para departamentos:
      1. Insertar
      2. Subir documento
      3. Consultar lista
    """
    def on_start(self):
        self.service = DepartamentoServices()
        self.last_inserted_dept_id = None
        self.user_session_id = str(uuid.uuid4())

    @task(1)
    def insert_departamento(self):
        operation_name = "Insertar Departamento (DB)"
        dept_name = generate_unique_name()
        dept = Departamento(nombre=dept_name, descripcion=f"Descripción de {dept_name}")

        start = time.perf_counter()
        exception = None
        try:
            resp = self.service.insertarDepartamento(dept)
            if resp.get("success", False):
                self.last_inserted_dept_id = resp.get("id_departamento")
            else:
                exception = Exception(resp.get("message", "Error insertando departamento"))
        except Exception as e:
            exception = e
        dt = (time.perf_counter() - start) * 1000

        events.request.fire(
            request_type="DB",
            name=operation_name,
            response_time=dt,
            response_length=len(str(resp)) if 'resp' in locals() else 0,
            exception=exception,
            context={"user_id": self.user_session_id}
        )

    @task(1)
    def upload_documento(self):
        operation_name = "Upload Documento (IO)"
        start = time.perf_counter()
        size_kb = random.choice([100, 500, 1024, 2048])
        time.sleep(size_kb / 1024)
        dt = (time.perf_counter() - start) * 1000

        events.request.fire(
            request_type="IO",
            name=operation_name,
            response_time=dt,
            response_length=0,
            exception=None,
            context={"user_id": self.user_session_id}
        )

    @task(1)
    def query_departamentos(self):
        operation_name = "Consultar Lista Departamentos (DB)"
        term = self.last_inserted_dept_id or ""

        start = time.perf_counter()
        exception = None
        try:
            resp = self.service.obtenerListaDepartamento(pagina=1, tam_pagina=10, busqueda=term)
            if not resp.get("success", False):
                exception = Exception(resp.get("message", "Error consultando departamentos"))
        except Exception as e:
            exception = e
        dt = (time.perf_counter() - start) * 1000

        events.request.fire(
            request_type="DB",
            name=operation_name,
            response_time=dt,
            response_length=len(str(resp)) if 'resp' in locals() else 0,
            exception=exception,
            context={"user_id": self.user_session_id}
        )

class MyDbUser(User):
    """
    Usuario simulado que ejecuta:
      - insertar_departamento
      - upload_documento
      - query_departamentos
    """
    host = "local_db_connection"
    wait_time = between(1, 2)
    tasks = [UserBehavior]
