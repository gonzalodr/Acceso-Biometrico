##Estilos generales para la interfaz
btnStyleSheet =u"""QPushButton {      
                                background-color: rgb(99, 118, 244);
                                color: white;
                                border: none; 
                                padding: 10px;
                                border-radius: 15px;
                                font: 700 10pt \"Segoe UI\";
                        }
                        QPushButton:hover {
                                background-color: rgb(76, 64, 207);
                        }"""                
LineEditStyleSheet = u"""QLineEdit {
                                background-color: rgb(247, 248, 255);
                                color: rgb(0, 0, 0);
                                border: 2px solid rgb(60, 0, 188);
                                padding: 5px;
                                border-radius: 10px;
                        }
                        QLineEdit:focus {
                                border: 2px solid darkblue;
                        }"""
tableStyleSheet = u"""
                        QTableWidget {    
                                background-color: white;
                                border-radius: 10px;
                        }
                        QHeaderView::section {    
                                background-color:rgb(96, 53, 223);    
                                color: white;    
                                padding: 10px;	
                                font: 700 10pt \"Segoe UI\";
                        }"""

mesboxStyleSheet = u"""
            QMessageBox {
                background-color: #F0F0F0;  /* Cambia a un gris claro o cualquier color que prefieras */
                color: Black;
                font: 14px Arial;
            }
            QLabel {
                color: Black;  /* Color del texto dentro del mensaje */
            }
            QPushButton {
                color: Black;  /* Color del texto del botón */
            }
            """

btnEliminarStyleSheet = u"""QPushButton {      
                                background-color:#E02500;
                                color: white;
                                border: none; 
                                padding: 10px;
                                border-radius: 15px;
                                font: 700 10pt \"Segoe UI\";
                        }
                        QPushButton:hover {
                                background-color: #C92200;
                        }""" 
btnDisableStyleSheet=  u"""QPushButton {      
                                background-color:#EDEDED;
                                color: #C2C2C2;
                                border: none; 
                                padding: 10px;
                                border-radius: 15px;
                                font: 700 10pt \"Segoe UI\";
                        }""" 
                                # Estilo general del formulario
form_styleSheet = """
            QFrame {
                background-color: White;
            }
            QLineEdit, QDateEdit, QTextEdit, QComboBox {
                background-color: #EBF3FF; 
                border: 1px solid #C6B6FE;  
                border-radius: 5px; 
                padding: 5px;
                font-size: 12px;
            }
            QLabel{
                font: 700 10pt \"Segoe UI\";
                background-color:transparent;
                color:black;
            }
            QLineEdit:focus, QDateEdit:focus, QTextEdit:focus, QComboBox:focus {
                border: 2px solid #8a2be2;  /* Borde lila oscuro al enfocar */
            }
        """                 