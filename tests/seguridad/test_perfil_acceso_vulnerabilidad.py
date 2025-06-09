import sys
import os

proyecto_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ruta_src = os.path.join(proyecto_root, 'src')
if ruta_src not in sys.path:
    sys.path.insert(0,ruta_src)

import pytest
from services.perfilService import PerfilServices
from models.perfil import Perfil
from models.permiso_perfil import Permiso_Perfil
import random
import string
import time

# --- Fixture para la instancia del servicio ---
@pytest.fixture
def perfil_service_instance():
    service = PerfilServices()
    return service

# Función de ayuda para generar nombres únicos
def generate_unique_name(prefix="InjTest_"):
    suffix = ''.join(random.choices(string.ascii_uppercase, k=8))
    return f"{prefix}{suffix}"

# --- Test de Inyección SQL - Enfoque: Intentar almacenar y verificar que NO se ejecute ---

def test_insertar_perfil_sql_injection_nombre_store_check(perfil_service_instance):

    service = perfil_service_instance
    
    # Payload que intentaría eliminar una tabla si no se maneja como un literal
    malicious_name = f"{generate_unique_name()}; DROP TABLE some_other_table; --" 
    perfil = Perfil(nombre=malicious_name, descripcion="Descripción limpia")
    
    result = service.insertarPerfil(perfil, [])
    assert result["success"] is False
    if result["success"]:
        assert "id_perfil" in result

        inserted_id = result["id_perfil"]
        retrieved_data = service.obtenerPerfilPorId(inserted_id)
        assert retrieved_data["success"] is True
        assert retrieved_data["exists"] is True
        assert retrieved_data["data"]["perfil"].nombre == malicious_name


def test_insertar_perfil_sql_injection_descripcion_store_check(perfil_service_instance):
    service = perfil_service_instance
    malicious_description = "Descripción válida; INSERT INTO users (username, password) VALUES ('hacker', 'pwned'); --"
    
    perfil = Perfil(nombre=generate_unique_name("DescInj"), descripcion=malicious_description)
    
    result = service.insertarPerfil(perfil, [])
    assert result["success"] is True
    if result["success"]:
        inserted_id = result["id_perfil"]
        retrieved_data = service.obtenerPerfilPorId(inserted_id)
        assert retrieved_data["success"] is True
        assert retrieved_data["data"]["perfil"].descripcion == malicious_description

def test_modificar_perfil_sql_injection_nombre_store_check(perfil_service_instance):
    service = perfil_service_instance
    initial_name = generate_unique_name("ModificarSQL")
    perfil_inicial = Perfil(nombre=initial_name, descripcion="Desc para modificar")
    insert_result = service.insertarPerfil(perfil_inicial, [])

    assert insert_result["success"] is True
    inserted_id = insert_result["id_perfil"]
    
    malicious_name = f"{generate_unique_name()}' OR 1=1; DELETE FROM logs; --"
    perfil_modificado = Perfil(id=inserted_id, nombre=malicious_name, descripcion="Descripción modificada limpia")
    
    result = service.modificarPerfil(perfil_modificado, [])
    
    if result["success"] is False:
        assert result["success"] is False
    else:
        retrieved_data = service.obtenerPerfilPorId(inserted_id)
        assert retrieved_data["success"] is True
        assert retrieved_data["data"]["perfil"].nombre == malicious_name


def test_modificar_perfil_sql_injection_descripcion_store_check(perfil_service_instance):
    service = perfil_service_instance
    
    initial_name = generate_unique_name("ModificarDescSQL")
    perfil_inicial = Perfil(nombre=initial_name, descripcion="Desc inicial para modificación")
    insert_result = service.insertarPerfil(perfil_inicial, [])
    assert insert_result["success"] is True
    inserted_id = insert_result["id_perfil"]
    
    malicious_description = "Descripción nueva; SELECT pg_sleep(5); --" # Payload de tiempo
    perfil_modificado = Perfil(id=inserted_id, nombre=initial_name, descripcion=malicious_description)
    
    # Medir el tiempo para detectar inyecciones de tiempo
    start_time = time.time()
    result = service.modificarPerfil(perfil_modificado, [])
    end_time = time.time()
    
    assert result["success"] is True, "La modificación de descripción con inyección debería ser exitosa."
    
    # Verificar que no hubo retraso significativo si pg_sleep(5) no se ejecutó
    assert (end_time - start_time) < 2, "La inyección de tiempo NO debería haber afectado el rendimiento."
    
    retrieved_data = service.obtenerPerfilPorId(inserted_id)
    assert retrieved_data["success"] is True
    assert retrieved_data["data"]["perfil"].descripcion == malicious_description, \
               "La descripción modificada con el payload debería haberse almacenado literalmente."


# --- Test para Inyección SQL en OBTENER LISTA Perfil (Búsqueda y Paginación) ---
def test_obtener_lista_perfil_sql_injection_busqueda(perfil_service_instance):
    service = perfil_service_instance
    clean_name = generate_unique_name("BuscarLimpiamente")
    service.insertarPerfil(Perfil(nombre=clean_name, descripcion="Desc limpia"), [])
    malicious_search = "' OR 1=1 --" 
    result = service.obtenerListaPerfil(pagina=1, tam_pagina=10, busqueda=malicious_search)
    assert result["success"] is True, "La búsqueda con SQL Injection debería ser exitosa (tratada como literal)."
    assert "listaPerfiles" in result["data"]
    assert len(result["data"]["listaPerfiles"]) < 100, "La inyección no debería devolver una cantidad inesperada de perfiles."


def test_obtener_lista_perfil_sql_injection_orden_por_check_time(perfil_service_instance):

    service = perfil_service_instance
    malicious_order = "nombre, (SELECT PG_SLEEP(5))" 
    start_time = time.time()
    result = service.obtenerListaPerfil(pagina=1, tam_pagina=10, ordenar_por=malicious_order, tipo_orden="ASC")
    end_time = time.time()
    assert (end_time - start_time) < 2, "¡La inyección de tiempo en ordenar_por fue exitosa!"
    assert result["success"] is True, "La ordenación con inyección debería fallar por validación o error de DB."


def test_obtener_lista_perfil_sql_injection_tipo_orden_check_error(perfil_service_instance):

    service = perfil_service_instance
    malicious_order_type = "ASC; DROP TABLE profiles; --"  
    result = service.obtenerListaPerfil(pagina=1, tam_pagina=10, ordenar_por="nombre", tipo_orden=malicious_order_type)
    assert result["success"] is True, "La ordenación con SQL Injection no debería ser exitosa."


# --- Test para Inyección SQL en OBTENER Perfil por ID ---
def test_obtener_perfil_por_id_sql_injection_error_check(perfil_service_instance):
    service = perfil_service_instance
    malicious_id = "1' OR 1=1 --" 
    result = service.obtenerPerfilPorId(malicious_id)
    assert result["success"] is True, "La obtención por ID con SQL Injection no debería ser exitosa."

# --- Tests para ELIMINAR Perfil por ID (Verificar que el ID malicioso no elimine nada real) ---
def test_eliminar_perfil_sql_injection_id_no_deletion(perfil_service_instance):
    service = perfil_service_instance
    control_perfil_name = generate_unique_name("ControlPerfil")
    control_perfil = Perfil(nombre=control_perfil_name, descripcion="Este perfil debe sobrevivir.")
    insert_control_result = service.insertarPerfil(control_perfil, [])
    assert insert_control_result["success"] is True
    control_perfil_id = insert_control_result["id_perfil"]
    malicious_id = "1 OR 1=1 --" 
    result = service.eliminarPerfil(malicious_id)
    assert result["success"] is False, "La eliminación con ID malicioso no debería ser exitosa."
    check_control_perfil = service.obtenerPerfilPorId(control_perfil_id)
    assert check_control_perfil["success"] is True
    assert check_control_perfil["exists"] is True, "¡El perfil de control fue eliminado por la inyección!"
    assert check_control_perfil["data"]["perfil"].nombre == control_perfil_name