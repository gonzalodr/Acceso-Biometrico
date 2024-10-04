import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Crear un widget central y un layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        # Crear la tabla
        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(4)  # Número de filas
        self.table_widget.setColumnCount(3)  # Número de columnas
        
        # Establecer encabezados
        self.table_widget.setHorizontalHeaderLabels(["Columna 1", "Columna 2", "Columna 3"])

        # Agregar algunos datos de ejemplo
        for i in range(4):
            for j in range(3):
                item = QTableWidgetItem(f"Fila {i+1}, Columna {j+1}")
                self.table_widget.setItem(i, j, item)

        # Aplicar estilo CSS a la tabla
        # self.table_widget.setStyleSheet("""
        #     QTableWidget {
        #         border: 1px solid #ccc;
        #         font-size: 16px;
        #     }
        #     QHeaderView::section {
        #         background-color: #f2f2f2;
        #         color: #333;
        #         font-weight: bold;
        #     }
        #     QTableWidget::item {
        #         padding: 10px;
        #     }
        #     QTableWidget::item:selected {
        #         background-color: #0078d7; /* Color al seleccionar */
        #         color: white; /* Color del texto al seleccionar */
        #     }
        # """)

        layout.addWidget(self.table_widget)
        self.setCentralWidget(central_widget)
        self.setWindowTitle("Tabla con Estilo CSS")

app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())

