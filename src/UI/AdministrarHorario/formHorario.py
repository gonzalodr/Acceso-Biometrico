from PySide6.QtWidgets import *
from PySide6.QtCore import *
from Utils.Utils import *
from UI.DialogoEmergente import *
from services.horarioService import *
from datetime import datetime
from datetime import timedelta


class formHorario(QDialog):
\
    Hservices = HorarioService()  # Instancia del servicio de horarios
    idH = 0  # ID del registro para diferenciar entre creación y actualización

    def __init__(self, parent=None, titulo="Registrar Horario", id=None):
        super().__init__(parent)
        self.setObjectName("form")
        self.setMinimumSize(QSize(700, 500))
        self.setWindowFlags(Qt.FramelessWindowHint)
        # add_Style(carpeta="css", archivoQSS="formHorario.css", QObjeto=self)
        cargar_estilos('claro','form.css',self)

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
            self._contenedor(lblDias, self.inputDias, self.errorDias), 0, 0
        )
        layoutForm.addLayout(
            self._contenedor(
                lblTipoJornada, self.inputTipoJornada, self.errorTipoJornada
            ),
            1,
            0,
        )
        layoutForm.addLayout(
            self._contenedor(lblHoraInicio, self.inputHoraInicio, self.errorHoraInicio),
            2,
            0,
        )
        layoutForm.addLayout(
            self._contenedor(lblHoraFin, self.inputHoraFin, self.errorHoraFin), 3, 0
        )
        layoutForm.addLayout(
            self._contenedor(
                lblDescripcion, self.inputDescripcion, self.errorDescripcion
            ),
            4,
            0,
        )

        # Botones de acción
        boton_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        boton_box.button(QDialogButtonBox.Cancel).setText("Cancelar")
        boton_box.button(QDialogButtonBox.Cancel).setObjectName("btncancelar")
        boton_box.button(QDialogButtonBox.Cancel).setMinimumSize(QSize(100,30))
        
        boton_box.button(QDialogButtonBox.Ok).setText("Registrar" if id == None else "Actualizar")
        boton_box.button(QDialogButtonBox.Ok).setObjectName("btnregistrar")
        boton_box.button(QDialogButtonBox.Ok).setMinimumSize(QSize(100,30))

        boton_box.accepted.connect(self._accion_horario)
        boton_box.rejected.connect(self.reject)
       
        # Centrar los botones
        boton_layout = QHBoxLayout()
        boton_layout.addStretch()
        boton_layout.addWidget(boton_box)
        boton_layout.addStretch()
        layoutFrame.addLayout(layoutForm)
        layoutFrame.addLayout(boton_layout)

        frame.setLayout(layoutFrame)
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
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

        horario = Horario(
            dias_semanales=self.inputDias.text(),
            tipo_jornada=self.inputTipoJornada.text(),
            hora_inicio=self.inputHoraInicio.time().toString("HH:mm"),
            hora_fin=self.inputHoraFin.time().toString("HH:mm"),
            descripcion=self.inputDescripcion.text(),
            id=self.idH,
        )

        if self.idH > 0:  # Si el ID es mayor a 0, se está actualizando
            result = self.Hservices.modificarHorario(horario)
            if result["success"]:
                dial = DialogoEmergente("Actualización", result["message"], "Check")
                dial.exec()
                self.accept()  # Cierra el formulario
            else:
                dial = DialogoEmergente("Error", result["message"], "Error")
                dial.exec()
        else:  # De lo contrario, es un nuevo registro
            result = self.Hservices.insertarHorario(horario)
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
        """
        result = self.Hservices.obtenerHorarioPorId(id)
        if result["success"] and result["data"]:
            horario = result["data"]
            self.idH = horario.id
            self.inputDias.setText(horario.dias_semanales)
            self.inputTipoJornada.setText(horario.tipo_jornada)

            # Convertimos `horario.hora_inicio` y `horario.hora_fin` a `str` en formato "HH:mm"
            hora_inicio_str = (datetime.min + horario.hora_inicio).strftime("%H:%M")
            hora_fin_str = (datetime.min + horario.hora_fin).strftime("%H:%M")

            # Ahora usamos `QTime.fromString` con los valores de cadena
            self.inputHoraInicio.setTime(QTime.fromString(hora_inicio_str, "HH:mm"))
            self.inputHoraFin.setTime(QTime.fromString(hora_fin_str, "HH:mm"))

            self.inputDescripcion.setText(horario.descripcion)
        else:
            dial = DialogoEmergente(
                "Error", "Hubo un error al cargar los datos.", "Error"
            )
            dial.exec()
            QTimer.singleShot(0, self.reject)  # Cierra el formulario si hay un error

    def _validar_campos(self):
        """
        Verifica que todos los campos requeridos estén llenos y en formato adecuado.
        """
        vacios = False

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
            self.inputDias.text().strip()
            or self.inputTipoJornada.text().strip()
            or self.inputHoraInicio.time().isValid()
            or self.inputHoraFin.time().isValid()
            or self.inputDescripcion.toPlainText().strip()
        ):
            return True
        else:
            return False

    def _cancelar_registro(self):
        """Si se encuentra inputs con datos entonces pregunta si esta seguro retirarse"""
        if self._validar_inputs_sin_con_datos():
            dialEmergente = DialogoEmergente(
                "¿?", "¿Estas seguro que que quieres cancelar?", "Question", True, True
            )
            opcion = dialEmergente.exec()
            if opcion == QDialog.Accepted:
                self.reject()
            elif opcion == QDialog.Rejected:
                pass 
        else:  ##si los inputs estan sin datos entonces se cierra el formulario de manera normal
            self.reject()  ##cerrar la ventana
