import pytest
import sys, os

# ————————————————————————————————————————————————————————————————————————————
# Asegura que Python encuentre tu paquete src/ para importar servicios y modelos
proyecto_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
ruta_src = os.path.join(proyecto_root, 'src')
if ruta_src not in sys.path:
    sys.path.insert(0, ruta_src)
# ————————————————————————————————————————————————————————————————————————————

from src.services.departamentoService import DepartamentoServices
from src.models.departamento          import Departamento

class DummyDataLayer:
    """
    Simula la capa de datos para Departamento.
    """
    def __init__(self):
        self.insert_count = 0
        self.update_count = 0
        self.delete_count = 0

    def create_departamento(self, departamento):
        if departamento.nombre.upper() == "DUPLICADO":
            return {"success": False, "message": "El departamento ya existe y no puede ser creado nuevamente."}
        self.insert_count += 1
        return {"success": True, "message": "Departamento creado con éxito."}

    def update_departamento(self, departamento):
        if departamento.id <= 0:
            return {"success": False, "message": "ID inválido para actualizar."}
        if departamento.nombre.upper() == "DUPLICADO":
            return {"success": False, "message": "El departamento ya existe, intente actualizar con un nombre distinto."}
        self.update_count += 1
        return {"success": True, "message": "Departamento actualizado con éxito."}

    def delete_departamento(self, departamento_id):
        if departamento_id <= 0:
            return {"success": False, "message": "ID inválido para eliminar."}
        self.delete_count += 1
        return {"success": True, "message": "Departamento eliminado con éxito."}


@pytest.fixture
def servicio_con_dummy():
    """
    Crea DepartamentoServices con DummyDataLayer para poder contar operaciones.
    """
    servicio = DepartamentoServices()
    dummy = DummyDataLayer()
    servicio.departamentoData = dummy
    return servicio, dummy


# ——————————————————————————————————————————————————————————————————————————————————————
# Tests de validación interna (_validarNombre, _validarDescripcion)
# ——————————————————————————————————————————————————————————————————————————————————————

def test_validar_nombre_valido(servicio_con_dummy):
    servicio, _ = servicio_con_dummy
    resultado = servicio._validarNombre("Departamento Valido")
    assert resultado["success"] is True
    assert resultado["message"] == "Nombre válido."

def test_validar_nombre_invalido_caracteres_y_longitud(servicio_con_dummy):
    servicio, _ = servicio_con_dummy
    invalido1 = servicio._validarNombre("Dept123")
    assert invalido1["success"] is False
    assert "no es válido" in invalido1["message"].lower()

    largo = "A" * 101
    invalido2 = servicio._validarNombre(largo)
    assert invalido2["success"] is False
    assert "no es válido" in invalido2["message"].lower()

def test_validar_descripcion_valida(servicio_con_dummy):
    servicio, _ = servicio_con_dummy
    resultado = servicio._validarDescripcion("Descripcion corta")
    assert resultado["success"] is True
    assert resultado["message"] == "Descripción válida."

def test_validar_descripcion_invalida_muy_larga(servicio_con_dummy):
    servicio, _ = servicio_con_dummy
    larga = "X" * 101
    resultado = servicio._validarDescripcion(larga)
    assert resultado["success"] is False
    assert "no es válida" in resultado["message"].lower()


# ——————————————————————————————————————————————————————————————————————————————————————
# Tests de insertarDepartamento (contar cuántos se insertan)
# ——————————————————————————————————————————————————————————————————————————————————————

def test_insertar_varias_veces(servicio_con_dummy):
    servicio, dummy = servicio_con_dummy
    depto1 = Departamento(nombre="NuevoDeptUno", descripcion="Prueba Uno", id=0)
    servicio.insertarDepartamento(depto1)
    depto2 = Departamento(nombre="NuevoDeptDos", descripcion="Prueba Dos", id=0)
    servicio.insertarDepartamento(depto2)

    # Imprime el contador final de insert
    print(f"Total insertados final: {dummy.insert_count}")
    assert dummy.insert_count == 2

def test_insertar_departamento_duplicado(servicio_con_dummy):
    servicio, dummy = servicio_con_dummy
    depto_duplicado = Departamento(nombre="DUPLICADO", descripcion="Cualquier cosa", id=0)
    respuesta = servicio.insertarDepartamento(depto_duplicado)

    # Imprime el contador final (debería seguir en 0)
    print(f"Total insertados final (duplicado): {dummy.insert_count}")
    assert dummy.insert_count == 0
    assert respuesta["success"] is False
    assert "ya existe" in respuesta["message"].lower()


# ——————————————————————————————————————————————————————————————————————————————————————
# Tests de modificarDepartamento (contar cuántos se actualizan)
# ——————————————————————————————————————————————————————————————————————————————————————

def test_modificar_varias_veces(servicio_con_dummy):
    servicio, dummy = servicio_con_dummy
    depto1 = Departamento(nombre="ActualizadoUno", descripcion="Desc Uno", id=5)
    servicio.modificarDepartamento(depto1)
    depto2 = Departamento(nombre="ActualizadoDos", descripcion="Desc Dos", id=6)
    servicio.modificarDepartamento(depto2)

    # Imprime contador final de update
    print(f"Total actualizados final: {dummy.update_count}")
    assert dummy.update_count == 2

def test_modificar_departamento_duplicado(servicio_con_dummy):
    servicio, dummy = servicio_con_dummy
    depto = Departamento(nombre="DUPLICADO", descripcion="Desc", id=7)
    respuesta = servicio.modificarDepartamento(depto)

    # Contador no debe incrementarse
    print(f"Total actualizados final (duplicado): {dummy.update_count}")
    assert dummy.update_count == 0
    assert respuesta["success"] is False
    assert "ya existe" in respuesta["message"].lower()


# ——————————————————————————————————————————————————————————————————————————————————————
# Tests de eliminarDepartamento (contar cuántos se eliminan)
# ——————————————————————————————————————————————————————————————————————————————————————

def test_eliminar_varias_veces(servicio_con_dummy):
    servicio, dummy = servicio_con_dummy
    servicio.eliminarDepartamento(3)
    servicio.eliminarDepartamento(4)

    # Imprime contador final de delete
    print(f"Total eliminados final: {dummy.delete_count}")
    assert dummy.delete_count == 2

def test_eliminar_departamento_id_invalido(servicio_con_dummy):
    servicio, dummy = servicio_con_dummy
    respuesta = servicio.eliminarDepartamento(0)

    # Contador no debe incrementarse
    print(f"Total eliminados final (invalid): {dummy.delete_count}")
    assert dummy.delete_count == 0
    assert respuesta["success"] is False
    assert "id inválido" in respuesta["message"].lower()


# ——————————————————————————————————————————————————————————————————————————————————————
# Tests “forward” para las consultas
# ——————————————————————————————————————————————————————————————————————————————————————

def test_obtener_lista_departamento_forward(servicio_con_dummy):
    servicio, dummy = servicio_con_dummy
    dummy_return = {
        "success": True,
        "data": {"listaDepartamentos": ["A", "B"], "pagina_actual": 1, "tam_pagina": 10, "total_paginas": 1, "total_registros": 2}
    }
    servicio.departamentoData.list_departamentos = lambda pagina, tam, col, tipo, busq: dummy_return

    resp = servicio.obtenerListaDepartamento(pagina=1, tam_pagina=10, ordenar_por="Nombre", tipo_orden="ASC", busqueda=None)
    assert resp == dummy_return

def test_obtener_departamento_por_id_forward(servicio_con_dummy):
    servicio, dummy = servicio_con_dummy
    dummy_return = {"success": True, "exists": True, "departamento": Departamento(nombre="X", descripcion="Y", id=2)}
    servicio.departamentoData.get_departamento_by_id = lambda x: dummy_return

    resp = servicio.obtenerDepartamentoPorId(2)
    assert resp == dummy_return