import pytest
from models.rol import Rol
from services.rolService import RolServices

@pytest.fixture
def rol_service():
    return RolServices()

def test_sql_injection_nombre(rol_service):
    malicious_name = "Admin'; DROP TABLE rol; --"
    rol = Rol(nombre=malicious_name, descripcion="Descripción valida", id=0)
    result = rol_service.insertarRol(rol)
    assert not result.get("success", False)
    assert "no es válido" in result.get("message", "").lower()

def test_nombre_vacio_rechazado(rol_service):
    rol = Rol(nombre="", descripcion="Descripción valida", id=0)
    result = rol_service.insertarRol(rol)
    assert not result.get("success", True)
    assert "no es válido" in result.get("message", "").lower()

def test_descripcion_vacia_aceptada(rol_service):
    
    rol = Rol(nombre="Rol descripcion vacia", descripcion="", id=0)
    result = rol_service.insertarRol(rol)
    assert result.get("success", True)

def test_nombre_con_caracteres_invalidos(rol_service):
    rol = Rol(nombre="Admin123!", descripcion="Descripción valida", id=0)
    result = rol_service.insertarRol(rol)
    assert not result.get("success", True)
    assert "no es válido" in result.get("message", "").lower()
