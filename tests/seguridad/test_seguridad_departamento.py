import pytest
from models.departamento import Departamento
from services.departamentoService import DepartamentoServices
from data.departamentoData import DepartamentoData


@pytest.fixture
def departamento_service():
    return DepartamentoServices()

def setup_method(self):
        servicio = DepartamentoServices()

        return servicio
    
# Prueba de inyección SQL en el campo "nombre"
def test_sql_injection_nombre(departamento_service):
    # Entrada maliciosa intentando DROP TABLE
    malicious_name = "DeptValido; DROP TABLE departamento; --"
    # Creamos una instancia de Departamento con nombre malicioso y descripción válida
    dept = Departamento(
        nombre=malicious_name,
        descripcion="Descripción válida",
        id=0
    )

    # Ejecutamos el método de inserción
    result = departamento_service.insertarDepartamento(dept)

    # Debe rechazarse la inserción y devolver un mensaje de validación
    assert not result.get("success", False), "El servicio debería rechazar el nombre malicioso"
    assert "no es válido" in result.get("message", ""), \
        f"Mensaje inesperado: {result.get('message')}"




