# tests/unitarias/test_rol_services.py

import pytest
import sys, os

proyecto_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
ruta_src = os.path.join(proyecto_root, 'src')
if ruta_src not in sys.path:
    sys.path.insert(0, ruta_src)

from src.services.rolService import RolServices
from src.models.rol import Rol


class DummyRolData:
    def __init__(self):
        self.insert_count = 0
        self.update_count = 0
        self.delete_count = 0

    def create_rol(self, rol: Rol):
        if rol.nombre.upper() == "DUPLICADO":
            return {"success": False, "message": "El rol ya existe y no puede ser creado nuevamente."}
        self.insert_count += 1
        return {"success": True, "message": "El Rol se guardó correctamente."}

    def update_rol(self, rol: Rol):
        if rol.id <= 0:
            return {"success": False, "message": "ID inválido para actualizar."}
        if rol.nombre.upper() == "DUPLICADO":
            return {"success": False, "message": "El rol ya existe, intente actualizar con un nombre distinto."}
        self.update_count += 1
        return {"success": True, "message": "Rol actualizado exitosamente."}

    def delete_rol(self, rol_id):
        if rol_id <= 0:
            return {"success": False, "message": "ID inválido para eliminar."}
        self.delete_count += 1
        return {"success": True, "message": "Rol eliminado correctamente."}
    

@pytest.fixture
def servicio_con_dummy():
    servicio = RolServices()
    dummy = DummyRolData()
    servicio.rolData = dummy
    return servicio, dummy

def test_validar_nombre_valido(servicio_con_dummy):
    servicio, _ = servicio_con_dummy
    resultado = servicio._validarNombre("Administrador Principal")
    assert resultado["success"] is True

def test_validar_nombre_invalido(servicio_con_dummy):
        servicio, _ = servicio_con_dummy
        resultado = servicio._validarNombre("Admin123!!")
        assert resultado["success"] is False

def test_validar_nombre_excesivamente_largo(servicio_con_dummy):
        servicio, _ = servicio_con_dummy
        nombre = "A" * 101
        resultado = servicio._validarNombre(nombre)
        assert resultado["success"] is False

def test_validar_descripcion_valida(servicio_con_dummy):
        servicio, _ = servicio_con_dummy
        resultado = servicio._validarDescripcion("Rol con permisos avanzados")
        assert resultado["success"] is True

def test_validar_descripcion_larga(servicio_con_dummy):
        servicio, _ = servicio_con_dummy
        descripcion = "X" * 101
        resultado = servicio._validarDescripcion(descripcion)
        assert resultado["success"] is False

def test_insertar_rol_valido(servicio_con_dummy):
        servicio, dummy = servicio_con_dummy
        rol = Rol(nombre="Supervisor", descripcion="Controla turnos", id=0)
        resultado = servicio.insertarRol(rol)
        assert resultado["success"] is True
        assert dummy.insert_count == 1

def test_insertar_rol_duplicado(servicio_con_dummy):
        servicio, dummy = servicio_con_dummy
        rol = Rol(nombre="DUPLICADO", descripcion="Copia", id=0)
        resultado = servicio.insertarRol(rol)
        assert resultado["success"] is False
        assert dummy.insert_count == 0

def test_modificar_rol_valido(servicio_con_dummy):
        servicio, dummy = servicio_con_dummy
        rol = Rol(nombre="Editor", descripcion="Edita datos", id=2)
        resultado = servicio.modificarRol(rol)
        assert resultado["success"] is True
        assert dummy.update_count == 1

def test_modificar_rol_con_nombre_duplicado(servicio_con_dummy):
        servicio, dummy = servicio_con_dummy
        rol = Rol(nombre="DUPLICADO", descripcion="Copia", id=2)
        resultado = servicio.modificarRol(rol)
        assert resultado["success"] is False
        assert dummy.update_count == 0

def test_modificar_rol_con_id_invalido(servicio_con_dummy):
        servicio, dummy = servicio_con_dummy
        rol = Rol(nombre="Editor", descripcion="Edita datos", id=0)
        resultado = servicio.modificarRol(rol)
        assert resultado["success"] is False
        assert dummy.update_count == 0

def test_eliminar_rol_valido(servicio_con_dummy):
        servicio, dummy = servicio_con_dummy
        resultado = servicio.eliminarRol(3)
        assert resultado["success"] is True
        assert dummy.delete_count == 1

def test_eliminar_rol_id_invalido(servicio_con_dummy):
        servicio, dummy = servicio_con_dummy
        resultado = servicio.eliminarRol(-1)
        assert resultado["success"] is False
        assert dummy.delete_count == 0

def test_obtener_rol_por_id_forward(servicio_con_dummy):
    servicio, _ = servicio_con_dummy
    dummy_return = {
        "success": True,
        "exists": True,
        "rol": Rol(nombre="Admin", descripcion="Gestiona", id=1)
    }
    servicio.rolData.get_rol_by_id = lambda _id: dummy_return

    resultado = servicio.obtenerRolPorId(1)
    assert resultado == dummy_return

def test_obtener_lista_roles_forward(servicio_con_dummy):
    servicio, _ = servicio_con_dummy 
    dummy_return = {"success": True, "data": ["Admin", "User"]}
    servicio.rolData.list_roles = lambda *args, **kwargs: dummy_return

    resultado = servicio.obtenerListaRol()
    assert resultado == dummy_return


