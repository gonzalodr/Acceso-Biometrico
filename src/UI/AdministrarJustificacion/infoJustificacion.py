from PySide6.QtWidgets import *
from PySide6.QtCore import *
from Utils.Utils import *

class InfoJustificacion(QDialog):
    def __init__(self, justificacion, nombre_empleado, fecha_asistencia, parent=None):
        super().__init__(parent)
        self.justificacion = justificacion 
        self.nombre_empleado = nombre_empleado
        self.fecha_asistencia = fecha_asistencia
        self.setWindowTitle("Información de la Justificación")
        self.setObjectName("infoJustificacion")  
        


        cargar_estilos('claro', 'info.css', self)


        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Title
        titulo = QLabel("Información de la Justificación")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignCenter)  
        layout.addWidget(titulo)

        # Información
        info_text = (
            f"<b>Nombre del Empleado:</b><br> {self.nombre_empleado}<br><br>"
            f"<b>Fecha de Asistencia:</b><br> {self.fecha_asistencia}<br><br>"
            f"<b>Fecha Realizada:</b><br> {self.justificacion.fecha}<br><br>"
            f"<b>Motivo:</b><br> {self.justificacion.motivo}<br><br>"
            f"<b>Descripción:</b><br> {self.justificacion.descripcion}<br><br>"
            f"<b>Tipo:</b><br> {self.justificacion.tipo}<br><br>"
        )

        info_label = QLabel(info_text)
        info_label.setObjectName("infoLabel")
        info_label.setAlignment(Qt.AlignCenter)  
        info_label.setWordWrap(True)  
        layout.addWidget(info_label)

        # Botón Aceptar
        btn_aceptar = QPushButton("Aceptar")
        btn_aceptar.setObjectName("btnaceptar")
        btn_aceptar.clicked.connect(self.close)  # Cerrar la ventana directamente
        layout.addWidget(btn_aceptar, alignment=Qt.AlignCenter)

        self.setLayout(layout)