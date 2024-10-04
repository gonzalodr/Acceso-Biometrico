import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtCore import Qt

class LogginWindow (QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LOGGIN")
        self.setGeometry(0,0,700,700)
        #style 
        self.setStyleSheet ("""
                            QWidget{
                                background-color:white;
                            }
                            QLabel{
                                font-size:16px;
                                color:#003366;
                            }
                            QLineEdit{
                                padding:10px;
                                font-size:14px;
                                border:2px solid #003366;
                                border-radius:5px;
                            }
                            QPushButton{
                                background-color:#003366;
                                color:white;
                                padding:10px;
                                font-size:16px;
                            }
                            QPushButton:hover{
                                background-color:#005599;
                            }
                            """)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        self.user_label = QLabel("Usuario")
        self.username_input = QLineEdit()
        self.pass_label = QLabel("Contraseña")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        
        self.login_button = QPushButton("Iniciar Sesión")
        self.login_button.clicked.connect(self.handle_login)
        
        layout.addWidget(self.user_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.pass_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        self.setLayout(layout)
    
    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        print(f"User: {username}\nPass: {password}")
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LogginWindow()
    window.show()
    sys.exit(app.exec())