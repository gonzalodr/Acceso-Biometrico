import pytest
from datetime import date
from src.services.justificacionService import JustificacionServices
from src.models.justificacion import Justificacion

class TestJustificacionServices:
    def setup_method(self):
        self.service = JustificacionServices()

    ## Pruebas funcionales para la validación de campos individuales ##

    def test_validar_motivo_exitoso(self):
        motivo = "Asunto personal"
        result = self.service._validarMotivo(motivo)
        assert result["success"] is True
        assert result["message"] == "Motivo válido."

    def test_validar_motivo_vacio(self):
        motivo = ""
        result = self.service._validarMotivo(motivo)
        assert result["success"] is False
        assert result["message"] == "El motivo no puede estar vacío."

    def test_validar_motivo_caracteres_invalidos(self):
        motivo = "1234@@@"
        result = self.service._validarMotivo(motivo)
        assert result["success"] is False
        assert result["message"] == "El motivo contiene caracteres inválidos."

    def test_validar_motivo_largo(self):
        motivo = "a" * 101  # Motivo de más de 100 caracteres
        result = self.service._validarMotivo(motivo)
        assert result["success"] is False
        assert result["message"] == "El motivo no puede exceder los 100 caracteres."

    def test_validar_descripcion_exitoso(self):
        descripcion = "Reunión programada con cliente"
        result = self.service._validarDescripcion(descripcion)
        assert result["success"] is True
        assert result["message"] == "Descripción válida."

    def test_validar_descripcion_vacia(self):
        descripcion = ""
        result = self.service._validarDescripcion(descripcion)
        assert result["success"] is False
        assert result["message"] == "La descripción no puede estar vacía."

    def test_validar_descripcion_larga(self):
        descripcion = "a" * 256  # Descripción de más de 255 caracteres
        result = self.service._validarDescripcion(descripcion)
        assert result["success"] is False
        assert result["message"] == "La descripción no puede exceder los 255 caracteres."

    def test_validar_fecha_exitoso(self):
        fecha = date(2025, 6, 1)
        result = self.service._validarFecha(fecha)
        assert result["success"] is True
        assert result["message"] == "Fecha válida."

    def test_validar_fecha_formato_invalido(self):
        fecha = "2025-06-01"  # Formato inválido
        result = self.service._validarFecha(fecha)
        assert result["success"] is False
        assert result["message"] == "La fecha debe ser un valor válido de tipo 'date'."


    def test_validar_fecha_nula(self):
        fecha = None
        result = self.service._validarFecha(fecha)
        assert result["success"] is False
        assert result["message"] == "La fecha debe ser un valor válido de tipo 'date'."

    ## Pruebas no funcionales ##

    

    def test_compatibilidad_con_entradas_varias(self):
        # Verificar que el sistema maneje correctamente diferentes tipos de entrada
        entradas_motivo = ["Asunto personal", "", "1234@@@", "a" * 101]
        for motivo in entradas_motivo:
            result = self.service._validarMotivo(motivo)
            if motivo == "":
                assert result["success"] is False
            elif motivo == "1234@@@" or len(motivo) > 100:
                assert result["success"] is False
            else:
                assert result["success"] is True

        entradas_descripcion = ["Reunión programada con cliente", "", "a" * 256]
        for descripcion in entradas_descripcion:
            result = self.service._validarDescripcion(descripcion)
            if descripcion == "":
                assert result["success"] is False
            elif len(descripcion) > 255:
                assert result["success"] is False
            else:
                assert result["success"] is True

    def test_tolerancia_espacios_extremos(self):
        justificacion = Justificacion(
            id_empleado=1,
            id_asistencia=1,
            fecha=date.today(),
            motivo="   ",  # Solo espacios
            descripcion="   Reunión   ",  # Espacios al inicio y final
            tipo="Permiso"
        )
        result = self.service.insertarJustificacion(justificacion)
        assert result["success"] is False
        assert "El motivo no puede estar vacío." in result["message"], f"Mensaje esperado no encontrado: {result['message']}"

    def test_tolerancia_entradas_nulas(self):
        # Verificar que el servicio maneja correctamente entradas nulas o vacías en múltiples campos
        justificacion = Justificacion(
            id_empleado=None,
            id_asistencia=None,
            fecha=None,
            motivo="",
            descripcion="",
            tipo=""
        )
        result = self.service.insertarJustificacion(justificacion)
        assert result["success"] is False
        assert "El motivo no puede estar vacío." in result["message"], f"Mensaje esperado no encontrado: {result['message']}"
