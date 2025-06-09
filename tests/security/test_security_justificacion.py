import pytest
from datetime import date
from models.justificacion import Justificacion
from data.justificacionData import JustificacionData
from src.services.justificacionService import JustificacionServices

@pytest.fixture
def justificacion_service():
    return JustificacionServices()

def setup_method(self):
        servicio = JustificacionServices()

        return servicio

def test_sql_injection_motivo(justificacion_service):
    # Crear una justificación con un intento de inyección SQL en el motivo
    servicio = JustificacionServices()
    malicious_input = "Motivo válido; DROP TABLE justificacion; --"
    justificacion = Justificacion(
        id_empleado=1,
        id_asistencia=1,
        fecha=date.today(),
        motivo=malicious_input,
        descripcion="Descripción válida",
        tipo="Permiso"
    )
    
    # Ejecutar el método de inserción
    result = servicio.insertarJustificacion(justificacion)
    
    # Verificar que la validación rechace el input malicioso
    assert not result["success"]
    assert "El motivo contiene caracteres inválidos." in result["message"]