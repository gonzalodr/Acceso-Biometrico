import sys
import os

# Calculamos la ruta absoluta de la carpeta raíz del proyecto (dos niveles arriba de este archivo)
proyecto_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Construimos la ruta completa a la carpeta src dentro de la raíz
ruta_src = os.path.join(proyecto_root, 'src')

# Insertamos src/ al comienzo de sys.path para poder hacer import src.<algo>
if ruta_src not in sys.path:
    sys.path.insert(0,ruta_src)

import pytest
from services.perfilService import PerfilServices # Importa la clase de servicio
from models.perfil import Perfil
from models.permiso_perfil import Permiso_Perfil
from settings.config import TBPERFIL_ID, TBPERFIL_NOMBRE, TBPERFIL_DESCRIPCION # Importa constantes necesarias
import random
import string

# --- Fixture para la instancia del servicio ---
@pytest.fixture
def perfil_service_instance():
    #se crea una instancia de perfilservices
    service = PerfilServices()
    return service

# Función de ayuda para generar nombres y descripciones únicas para evitar conflictos
def generate_unique_name(prefix="Test_Perfil_"):
    suffix = ''.join(random.choices(string.ascii_uppercase, k=6))
    return f"{prefix}{suffix}"

# --- Tests para _validarNombre (Método Privado) ---
def test_validar_nombre_valido(perfil_service_instance):
    service = perfil_service_instance
    result = service._validarNombre("Administrador Valido")
    assert result["success"] is True
    assert result["message"] == "Nombre válido."

def test_validar_nombre_vacio(perfil_service_instance):
    service = perfil_service_instance
    result = service._validarNombre("")
    assert result["success"] is False
    assert result["message"] == "El nombre del perfil no es válido."

def test_validar_nombre_con_numeros(perfil_service_instance):
    service = perfil_service_instance
    result = service._validarNombre("Admin123")
    assert result["success"] is False
    assert result["message"] == "El nombre del perfil no es válido."

def test_validar_nombre_largo(perfil_service_instance):
    service = perfil_service_instance
    long_name = "a" * 101
    result = service._validarNombre(long_name)
    assert result["success"] is False
    assert result["message"] == "El nombre del perfil no es válido."

# --- Tests para _validarDescripcion (Método Privado) ---
def test_validar_descripcion_valida(perfil_service_instance):
    service = perfil_service_instance
    result = service._validarDescripcion("Descripción de prueba válida.")
    assert result["success"] is True
    assert result["message"] == "Descripción válida."

def test_validar_descripcion_larga(perfil_service_instance):
    service = perfil_service_instance
    long_description = "b" * 101
    result = service._validarDescripcion(long_description)
    assert result["success"] is False
    assert result["message"] == "La descripción del perfil no es válida."

# --- Tests para existeNombreRegistrado ---
def test_existe_nombre_registrado_true(perfil_service_instance):
    service = perfil_service_instance
    unique_name = generate_unique_name("nombre")
    # Insertar un perfil para que exista
    perfil = Perfil(nombre=unique_name, descripcion="Desc para verificar existencia")
    insetReq =service.insertarPerfil(perfil, []) # Insertar sin permisos inicialmente
    result = service.existeNombreRegistrado(unique_name)
    assert result["success"] is True
    assert result["exists"] is True

def test_existe_nombre_registrado_false(perfil_service_instance):
    service = perfil_service_instance
    unique_name = generate_unique_name("NoExisteNombre_") # Nombre que no debería existir
    result = service.existeNombreRegistrado(unique_name)
    assert result["success"] is True
    assert result["exists"] is False

def test_existe_nombre_registrado_con_id_excluido(perfil_service_instance):
    service = perfil_service_instance
    unique_name = generate_unique_name("nombreperfil")
    
    # Insertar el perfil que luego excluiremos
    perfil_existente = Perfil(nombre=unique_name, descripcion="Desc para exclusión")
    insert_result = service.insertarPerfil(perfil_existente, [])
    assert insert_result["success"] is True
    
    # Verificar que el nombre NO exista cuando se excluye su propio ID
    result = service.existeNombreRegistrado(unique_name, idPerfil=insert_result["id_perfil"])
    assert result["success"] is True
    assert result["exists"] is False 

# --- Tests para insertarPerfil (CRUD) ---
def test_insertar_perfil_success(perfil_service_instance):
    service = perfil_service_instance
    unique_name = generate_unique_name("perfil")
    perfil = Perfil(nombre=unique_name, descripcion="Descripción de un nuevo perfil")
    lista_permisos = [
        Permiso_Perfil(perfil_id=None, tabla="empleado", ver=True, crear=True, editar=False, eliminar=False),
        Permiso_Perfil(perfil_id=None, tabla="perfil", ver=True, crear=False, editar=True, eliminar=False)
    ]
    
    result = service.insertarPerfil(perfil, lista_permisos)
    
    assert result["success"] is True

    # Opcional: Verificar si el perfil y sus permisos fueron realmente insertados
    retrieved_data = service.obtenerPerfilPorId(result["id_perfil"])
    assert retrieved_data["success"] is True
    assert retrieved_data["data"]["perfil"].nombre == unique_name
    assert len(retrieved_data["data"]["listaPermisos"]) == 2

def test_insertar_perfil_invalid_name(perfil_service_instance):
    service = perfil_service_instance
    perfil = Perfil(nombre="Nombre Inv@lido", descripcion="Descripción de prueba")
    lista_permisos = []
    
    result = service.insertarPerfil(perfil, lista_permisos)
    
    assert result["success"] is False
    assert result["message"] == "El nombre del perfil no es válido."

def test_insertar_perfil_invalid_description(perfil_service_instance):
    service = perfil_service_instance
    unique_name = generate_unique_name("PerfilInvDesc")
    perfil = Perfil(nombre=unique_name, descripcion="a" * 101)
    lista_permisos = []
    
    result = service.insertarPerfil(perfil, lista_permisos)
    
    assert result["success"] is False

# --- Tests para modificarPerfil (CRUD) ---
def test_modificar_perfil_success(perfil_service_instance):
    service = perfil_service_instance
    
    # Primero insertamos un perfil para modificarlo
    initial_name = generate_unique_name("ModificarInicio")
    perfil_inicial = Perfil(nombre=initial_name, descripcion="Descripción inicial")
    insert_result = service.insertarPerfil(perfil_inicial, [])
    assert insert_result["success"] is True
    inserted_id = insert_result["id_perfil"]


    # Creamos el perfil con los datos a actualizar
    updated_name = generate_unique_name("ModificadoExito")
    perfil_modificado = Perfil(id=inserted_id, nombre=updated_name, descripcion="Descripción actualizada")
    # Lista de permisos: se asume que los IDs de permiso existen si no se crean nuevos
    lista_permisos = [
        Permiso_Perfil(id=None, perfil_id=inserted_id, tabla="empleado", ver=True, crear=True, editar=True, eliminar=True) # Se crearía si no existe ID de permiso
    ]
    
    result = service.modificarPerfil(perfil_modificado, lista_permisos)
    
    assert result["success"] is True

    # Opcional: Verificar que los cambios se reflejan en la BD
    retrieved_data = service.obtenerPerfilPorId(inserted_id)
    assert retrieved_data["success"] is True


def test_modificar_perfil_invalid_name(perfil_service_instance):
    service = perfil_service_instance
    # No necesitamos insertar porque la validación ocurre antes de la interacción con la BD
    perfil = Perfil(id=1, nombre="Inv@lid", descripcion="Desc válida")
    result = service.modificarPerfil(perfil, [])
    assert result["success"] is False

# --- Tests para eliminarPerfil (CRUD) ---
def test_eliminar_perfil_success(perfil_service_instance):
    service = perfil_service_instance
    
    # Insertar un perfil para eliminarlo
    perfil_a_eliminar = Perfil(nombre=generate_unique_name("EliminarPerfil"), descripcion="Perfil a borrar")
    insert_result = service.insertarPerfil(perfil_a_eliminar, [])
    assert insert_result["success"] is True
    inserted_id = insert_result["id_perfil"]
    result = service.eliminarPerfil(inserted_id)
    assert result["success"] is True
    check_result = service.obtenerPerfilPorId(inserted_id)
    assert check_result["success"] is True # La capa de datos retorna success=True y exists=False
    assert check_result["exists"] is False


# --- Tests para obtenerListaPerfil (CRUD - Listar con paginación) ---
def test_obtener_lista_perfil_success(perfil_service_instance):
    service = perfil_service_instance
    service.insertarPerfil(Perfil(nombre=generate_unique_name("L1"), descripcion="Desc L1"), [])
    service.insertarPerfil(Perfil(nombre=generate_unique_name("L2"), descripcion="Desc L2"), [])
    result = service.obtenerListaPerfil(pagina=1, tam_pagina=5, ordenar_por="nombre", tipo_orden="ASC", busqueda="Test_Perfil_L")
    assert result["success"] is True
    assert "listaPerfiles" in result["data"]

def test_obtener_lista_perfil_empty(perfil_service_instance):
    service = perfil_service_instance
    result = service.obtenerListaPerfil(busqueda="UNLIKELY_NON_EXISTENT_SEARCH_STRING_12345")
    assert result["success"] is True
    assert len(result["data"]["listaPerfiles"]) == 0

# --- Tests para obtenerListaPerfilCB (CRUD - Listar para ComboBox) ---
def test_obtener_lista_perfil_cb_success(perfil_service_instance):
    service = perfil_service_instance
    service.insertarPerfil(Perfil(nombre=generate_unique_name("CB_"), descripcion="Desc CB"), [])
    result = service.obtenerListaPerfilCB(pagina=1, tam_pagina=10, ordenar_por="nombre", tipo_orden="ASC")
    assert result["success"] is True
    assert "listaPerfiles" in result["data"]
    assert len(result["data"]["listaPerfiles"]) >= 1 

# --- Tests para obtenerPerfilPorId (CRUD - Obtener por ID) ---
def test_obtener_perfil_por_id_found(perfil_service_instance):
    service = perfil_service_instance
    
    # Insertar un perfil para buscarlo por ID
    unique_name = generate_unique_name("BuscarID")
    perfil_a_buscar = Perfil(nombre=unique_name, descripcion="Perfil para buscar por ID")
    insert_result = service.insertarPerfil(perfil_a_buscar, [])
    assert insert_result["success"] is True
    inserted_id = insert_result["id_perfil"]
    result = service.obtenerPerfilPorId(inserted_id)
    assert result["success"] is True
    assert result["exists"] is True

def test_obtener_perfil_por_id_not_found(perfil_service_instance):
    service = perfil_service_instance
    result = service.obtenerPerfilPorId(9999999999999) 
    assert result["success"] is True
    assert result["exists"] is False

# --- Tests para obtener_todo_perfiles (CRUD - Obtener todos) ---
def test_obtener_todo_perfiles_success(perfil_service_instance):
    service = perfil_service_instance
    service.insertarPerfil(Perfil(nombre=generate_unique_name("Todo_"), descripcion="Desc Todo"), [])
    result = service.obtener_todo_perfiles()     
    assert result["success"] is True
    assert "listaPerfiles" in result["data"]
    assert len(result["data"]["listaPerfiles"]) >= 1