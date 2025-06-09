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
import random
import string
from PySide6.QtWidgets import QComboBox, QPushButton, QApplication, QLabel
from PySide6.QtCore import Qt, QTimer
from UI.AdministrarPermisosPerfil.formPerfil import FormularioPerfilAccesos

def generate_unique_name(prefix="Test_Perfil_"):
    """Genera un nombre único con un sufijo aleatorio."""
    suffix = ''.join(random.choices(string.ascii_uppercase, k=6))
    return f"{prefix}{suffix}"

@pytest.mark.qtbot
def test_registrar_perfil_sin_dialogo(qtbot):

    form = FormularioPerfilAccesos()
    qtbot.addWidget(form)
    form.show()

    # --- 1. Preparación de datos y llenado del formulario ---
    nombre_test = generate_unique_name("testUiPerfil")
    descripcion_test = generate_unique_name("descUiPerfil")
    
    form.inNombrePerfil.setText(nombre_test)
    form.inDescripcion.setText(descripcion_test)

    # --- 2. Simulación de adición de accesos y selección de permisos ---
    form.btnAddAccesos.click()
    qtbot.wait(100) 

    index = form.model.index(0, 0)
    widget = form.ArbolAccesos.indexWidget(index)
    
    assert widget is not None, "El widget del índice 0,0 (primer acceso) no fue encontrado."
    
    combo = widget.findChild(QComboBox)
    assert combo is not None, "QComboBox no encontrado dentro del widget del acceso."

    combo.setCurrentIndex(0)
    # Selecciona permisos específicos en el árbol de accesos
    itemRaiz = form.model.item(0)
    assert itemRaiz is not None, "El item raíz del modelo de accesos no fue encontrado."
    for i in range(itemRaiz.rowCount()):
        permiso = itemRaiz.child(i)
        # Selecciona "Ver" y "Crear" si existen
        if permiso.text() in ["Ver", "Crear"]:
            permiso.setCheckState(Qt.Checked)
            print(f"DEBUG: Marcado permiso: {permiso.text()}")

    # --- 3. Localizar el botón de registro y simular clic ---
    btnRegistrar = form.findChild(QPushButton, "btnregistrar")
    assert btnRegistrar is not None, "Botón 'btnregistrar' no encontrado en el formulario."

    print("DEBUG: Simulando clic en el botón 'Registrar'.")
    qtbot.mouseClick(btnRegistrar, Qt.LeftButton)

    # --- 4. Validación de la respuesta del servicio (después de la llamada) ---
    print(f"DEBUG: Verificando respuesta del servicio. form.response: {form.response}")
    resultado = form.response
    assert resultado is not None, "No se obtuvo resultado desde el servicio de creación (form.response es None)."
    assert resultado.get("success") is True, f"Fallo en el servicio de creación: {resultado.get('message', 'Sin mensaje de error')}"
    assert "id_perfil" in resultado, "No se retornó el ID del perfil en la respuesta del servicio."

    # --- 5. Validación final contra la base de datos (si aplica) ---
    id_perfil = resultado["id_perfil"]
    print(f"DEBUG: Perfil creado con ID: {id_perfil}")

    perfil_response = form.perfilServices.obtenerPerfilPorId(id_perfil)
    assert perfil_response.get("success") is True, f"Error al obtener perfil de DB: {perfil_response.get('message')}"
    assert perfil_response.get("exists") is True, "El perfil no existe en la base de datos después de la creación."
    assert perfil_response["data"]["perfil"].nombre == nombre_test, "El nombre del perfil recuperado no coincide con el enviado."
    assert perfil_response["data"]["perfil"].descripcion == descripcion_test, "La descripción del perfil recuperado no coincide con la enviada."

    print("DEBUG: Test de registro de perfil completado exitosamente (sin interacción con diálogo emergente).")