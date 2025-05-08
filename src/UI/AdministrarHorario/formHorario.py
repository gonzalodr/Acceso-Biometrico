from PySide6.QtWidgets import *
from PySide6.QtCore import *
from Utils.Utils import *
from UI.DialogoEmergente import *
from services.horarioService import *
from datetime import datetime
from datetime import timedelta
from services.rolService import *


class formHorario(QDialog):

    Hservices = HorarioService()  # Instancia del servicio de horarios
    idH = 0  # ID del registro para diferenciar entre creación y actualización
    RolService = RolServices()

    def __init__(self, parent=None, titulo="Registrar Horario", id=None):
        super().__init__(parent)
        self.setObjectName("form")
        self.setMinimumSize(QSize(850, 650))
        self.setWindowFlags(Qt.FramelessWindowHint)
        # add_Style(carpeta="css", archivoQSS="formHorario.css", QObjeto=self)
        cargar_estilos("claro", "form.css", self)

        # Configuración del frame principal
        frame = QFrame()
        layoutFrame = QVBoxLayout()
        frame.setObjectName("formFrame")
        layoutFrame.setContentsMargins(10, 20, 10, 20)
        layoutFrame.setSpacing(10)

        # Título del formulario
        lblTitulo = QLabel(text=titulo)
        lblTitulo.setObjectName("titulo")
        lblTitulo.setAlignment(Qt.AlignCenter)
        layoutFrame.addWidget(lblTitulo)

        # Layout del formulario
        layoutForm = QGridLayout()
        layoutForm.setContentsMargins(20, 10, 20, 20)
        layoutForm.setHorizontalSpacing(45)
        layoutForm.setVerticalSpacing(1)

        # Elementos del formulario
        # Nombre de Horario
        lblNombreHorario = QLabel(text="Nombre de Horario")
        self.inputNombreHorario = QLineEdit()
        self.inputNombreHorario.setPlaceholderText("Ingrese el nombre del horario")
        self.inputNombreHorario.installEventFilter(self)
        self.errorNombreHorario = QLabel()
        Sombrear(self.inputNombreHorario, 20, 0, 0)

        # Rol
        lblRol = QLabel(text="Rol")
        self.inputRol = QComboBox()
        self.inputRol.setPlaceholderText("Seleccione un rol")
        self.cargar_roles()  # para cargar los roles
        self.errorRol = QLabel()
        Sombrear(self.inputRol, 20, 0, 0)

        lblDias = QLabel(text="Días Semanales")
        self.inputDias = QLineEdit()
        self.inputDias.setPlaceholderText("Ingrese los días (ej. Lunes-Viernes)")
        self.inputDias.installEventFilter(self)
        self.errorDias = QLabel()
        Sombrear(self.inputDias, 20, 0, 0)

        lblTipoJornada = QLabel(text="Tipo de Jornada")
        self.inputTipoJornada = QLineEdit()
        self.inputTipoJornada.setPlaceholderText("Ingrese el tipo de jornada")
        self.inputTipoJornada.installEventFilter(self)
        self.errorTipoJornada = QLabel()
        Sombrear(self.inputTipoJornada, 20, 0, 0)

        lblHoraInicio = QLabel(text="Hora de Inicio")
        self.inputHoraInicio = QTimeEdit()
        self.inputHoraInicio.setDisplayFormat("HH:mm")
        self.inputHoraInicio.setTime(QTime.currentTime())
        self.errorHoraInicio = QLabel()
        Sombrear(self.inputHoraInicio, 20, 0, 0)

        lblHoraFin = QLabel(text="Hora de Fin")
        self.inputHoraFin = QTimeEdit()
        self.inputHoraFin.setDisplayFormat("HH:mm")
        self.inputHoraFin.setTime(QTime.currentTime())
        self.errorHoraFin = QLabel()
        Sombrear(self.inputHoraFin, 20, 0, 0)

        lblDescripcion = QLabel(text="Descripción")
        self.inputDescripcion = QLineEdit()
        self.inputDescripcion.setPlaceholderText("Ingrese una descripción opcional")
        self.inputDescripcion.setMaximumHeight(50)
        self.errorDescripcion = QLabel()
        Sombrear(self.inputDescripcion, 20, 0, 0)

        # Añadiendo widgets al layout de formulario
        layoutForm.addLayout(
            self._contenedor(
                lblNombreHorario, self.inputNombreHorario, self.errorNombreHorario
            ),
            0,
            0,
        )
        layoutForm.addLayout(
            self._contenedor(lblRol, self.inputRol, self.errorRol), 1, 0
        )
        layoutForm.addLayout(
            self._contenedor(lblDias, self.inputDias, self.errorDias), 2, 0
        )
        layoutForm.addLayout(
            self._contenedor(
                lblTipoJornada, self.inputTipoJornada, self.errorTipoJornada
            ),
            3,
            0,
        )
        layoutForm.addLayout(
            self._contenedor(lblHoraInicio, self.inputHoraInicio, self.errorHoraInicio),
            4,
            0,
        )
        layoutForm.addLayout(
            self._contenedor(lblHoraFin, self.inputHoraFin, self.errorHoraFin), 5, 0
        )
        layoutForm.addLayout(
            self._contenedor(
                lblDescripcion, self.inputDescripcion, self.errorDescripcion
            ),
            6,
            0,
        )

        # Botones de acción
        boton_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        boton_box.button(QDialogButtonBox.Cancel).setText("Cancelar")
        boton_box.button(QDialogButtonBox.Cancel).setObjectName("btncancelar")
        boton_box.button(QDialogButtonBox.Cancel).setMinimumSize(QSize(100, 30))

        boton_box.button(QDialogButtonBox.Ok).setText(
            "Registrar" if id == None else "Actualizar"
        )
        boton_box.button(QDialogButtonBox.Ok).setObjectName("btnregistrar")
        boton_box.button(QDialogButtonBox.Ok).setMinimumSize(QSize(100, 30))

        boton_box.accepted.connect(self._accion_horario)
        boton_box.rejected.connect(self._cancelar_registro)

        # Centrar los botones
        boton_layout = QHBoxLayout()
        boton_layout.addStretch()
        boton_layout.addWidget(boton_box)
        boton_layout.addStretch()
        layoutFrame.addLayout(layoutForm)
        layoutFrame.addLayout(boton_layout)

        frame.setLayout(layoutFrame)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(frame)
        self.setLayout(layout)

        # Cargar datos si se pasa un ID
        if id:
            self._obtener_registroId(id)

    def _contenedor(self, label: QLabel, input, label_error: QLabel):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        label_error.setObjectName("lblerror")
        label_error.setMaximumHeight(25)
        label_error.setMinimumHeight(25)
        label_error.setWordWrap(True)

        layout.addWidget(label)
        layout.addWidget(input)
        layout.addWidget(label_error)
        return layout

    def _accion_horario(self):
        """
        Maneja la acción de crear o actualizar un horario.
        """
        if not self._validar_campos():
            dialEmergente = DialogoEmergente(
                "Advertencia", "Llene todos los campos requeridos.", "Warning"
            )
            dialEmergente.exec()
            return

        id_rol = self.inputRol.currentData()

        horario = Horario(
            nombre_horario=self.inputNombreHorario.text(),
            dias_semanales=self.inputDias.text(),
            tipo_jornada=self.inputTipoJornada.text(),
            hora_inicio=self.inputHoraInicio.time().toString("HH:mm"),
            hora_fin=self.inputHoraFin.time().toString("HH:mm"),
            descripcion=self.inputDescripcion.text(),
            id=self.idH,
        )

        if self.idH > 0:  # Si el ID es mayor a 0, se está actualizando
            result = self.Hservices.modificarHorario(horario, id_rol)
            if result["success"]:
                dial = DialogoEmergente("Actualización", result["message"], "Check")
                dial.exec()
                self.accept()  # Cierra el formulario
            else:
                dial = DialogoEmergente("Error", result["message"], "Error")
                dial.exec()
        else:  # De lo contrario, es un nuevo registro
            result = self.Hservices.insertarHorario(horario, id_rol)
            if result["success"]:
                dial = DialogoEmergente("Registro", result["message"], "Check")
                dial.exec()
                self.accept()  # Cierra el formulario
            else:
                dial = DialogoEmergente("Error", result["message"], "Error")
                dial.exec()

    def _obtener_registroId(self, id):
        """
        Carga los datos de un horario específico en los campos de entrada.
        (Versión actualizada para manejar nombre y rol)
        """
        result = self.Hservices.obtenerHorarioPorId(id)
        if result["success"] and result["data"]:
            horario = result["data"]
            self.idH = horario["id"]

            # Campos básicos (manteniendo tu estructura original)
            self.inputNombreHorario.setText(horario["nombre_horario"])
            self.inputDias.setText(horario["dias_semanales"])
            self.inputTipoJornada.setText(horario["tipo_jornada"])
            self.inputDescripcion.setText(horario["descripcion"])

            # Manejo de horas (versión mejorada)
            try:
                # Si las horas vienen como timedelta (formato original)
                if isinstance(horario["hora_inicio"], timedelta):
                    hora_inicio_str = (datetime.min + horario["hora_inicio"]).strftime(
                        "%H:%M"
                    )
                    hora_fin_str = (datetime.min + horario["hora_fin"]).strftime(
                        "%H:%M"
                    )
                else:  # Si ya vienen como string
                    hora_inicio_str = str(horario["hora_inicio"])
                    hora_fin_str = str(horario["hora_fin"])

                self.inputHoraInicio.setTime(QTime.fromString(hora_inicio_str, "HH:mm"))
                self.inputHoraFin.setTime(QTime.fromString(hora_fin_str, "HH:mm"))
            except Exception as e:
                print(f"Error al convertir horas: {e}")
                # Establecer horas por defecto si hay error
                self.inputHoraInicio.setTime(QTime.currentTime())
                self.inputHoraFin.setTime(QTime.currentTime().addSecs(3600))  # +1 hora

            # Manejo del rol (nuevo)
            if "rol_id" in horario and horario["rol_id"]:
                # Buscar el índice del rol actual en el combobox
                index = self.inputRol.findData(horario["rol_id"])
                if index >= 0:
                    self.inputRol.setCurrentIndex(index)
                else:
                    print(
                        f"Advertencia: Rol ID {horario['rol_id']} no encontrado en combobox"
                    )
                    self.inputRol.setCurrentIndex(-1)  # Deseleccionar cualquier rol
            else:
                print("Advertencia: No se encontró rol_id en los datos del horario")
                self.inputRol.setCurrentIndex(-1)

        else:
            error_msg = result.get("message", "Hubo un error al cargar los datos.")
            dial = DialogoEmergente("Error", error_msg, "Error")
            dial.exec()
            QTimer.singleShot(0, self.reject)

    def _validar_campos(self):
        """
        Verifica que todos los campos requeridos estén llenos y en formato adecuado.
        """
        vacios = False

        if not self.inputNombreHorario.text().strip:
            Sombrear(self.inputNombreHorario, 20, 0, 0, "red")
            vacios = True
        else:
            Sombrear(self.inputNombreHorario, 20, 0, 0)

        if not self.inputDias.text().strip():
            Sombrear(self.inputDias, 20, 0, 0, "red")
            vacios = True
        else:
            Sombrear(self.inputDias, 20, 0, 0)

        if not self.inputTipoJornada.text().strip():
            Sombrear(self.inputTipoJornada, 20, 0, 0, "red")
            vacios = True
        else:
            Sombrear(self.inputTipoJornada, 20, 0, 0)

        # Valida el campo de Rol
        if self.inputRol.currentIndex() == -1:  # Si no se ha seleccionado ningún rol
            Sombrear(self.inputRol, 20, 0, 0, "red")
            vacios = True
        else:
            Sombrear(self.inputRol, 20, 0, 0)

        if (
            not self.inputHoraInicio.time().isValid()
            or not self.inputHoraFin.time().isValid()
        ):
            Sombrear(self.inputHoraInicio, 20, 0, 0, "red")
            Sombrear(self.inputHoraFin, 20, 0, 0, "red")
            vacios = True
        else:
            Sombrear(self.inputHoraInicio, 20, 0, 0)
            Sombrear(self.inputHoraFin, 20, 0, 0)

        # Validación de que la hora de inicio sea menor que la hora de fin
        if self.inputHoraInicio.time() >= self.inputHoraFin.time():
            dialEmergente = DialogoEmergente(
                "Error", "La hora de inicio debe ser menor que la hora de fin.", "Error"
            )
            dialEmergente.exec()
            return False  # Regresa inmediatamente si las horas son incorrectas

        return not vacios  # Retorna True si todos los campos están correctos

    def _validar_inputs_sin_con_datos(self):
        """
        Verifica si algún campo del formulario tiene datos ingresados.
        Retorna True si al menos un campo tiene datos, de lo contrario, False.
        """
        if (
            self.inputNombreHorario.text().strip()
            or self.inputDias.text().strip()
            or self.inputTipoJornada.text().strip()
            or self.inputHoraInicio.time().isValid()
            or self.inputHoraFin.time().isValid()
            or self.inputDescripcion.toPlainText().strip()
            or self.inputRol.currentIndex() == -1
        ):
            return True
        else:
            return False

    def _cancelar_registro(self):
        """Muestra diálogo de confirmación al cancelar si hay datos ingresados"""
        if self._validar_inputs_sin_con_datos():
            dialEmergente = DialogoEmergente(
                "Confirmar cancelación",
                "¿Estás seguro que deseas cancelar? Se perderán los cambios no guardados.",
                "Question",
                True,  # Mostrar botones Sí/No
                True,  # Activar modo pregunta
            )
            if dialEmergente.exec() == QDialog.Accepted:
                self.reject()
        else:
            self.reject()

    def cargar_roles(self):
        """
        Método para cargar los roles en el QComboBox.
        """
        try:
            # Limpia el QComboBox antes de agregar nuevos elementos
            self.inputRol.clear()

            # Obtiene todos los roles
            resultado = self.RolService.obtener_nombre_rol()

            if resultado["success"]:
                roles = resultado["data"]
                if roles:  # Si hay roles
                    for rol in roles:
                        self.inputRol.addItem(rol["nombre"], rol["id"])
                else:  # Si no hay roles
                    dialEmergente = DialogoEmergente(
                        "Advertencia",
                        "No se encontraron roles.",
                        "Warning",
                        True,
                        False,
                    )
                    dialEmergente.exec()
            else:  # Si hubo un error
                dialEmergente = DialogoEmergente(
                    "Error",
                    resultado["message"],
                    "Error",
                    True,
                    False,
                )
                dialEmergente.exec()

        except Exception as e:
            print(f"Error al cargar los roles: {e}")
            dialEmergente = DialogoEmergente(
                "Error",
                "No se pudieron cargar los roles.",
                "Error",
                True,
                False,
            )
            dialEmergente.exec()
