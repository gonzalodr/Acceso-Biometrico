
from PySide6.QtWidgets      import *
from PySide6.QtCore         import *
from PySide6.QtGui          import *
from Utils.Utils            import *
from UI.DialogoEmergente    import DialogoEmergente
from services.permisosPerfilServices import PermisosPerfilServices
from services.perfilService import PerfilServices
from settings.config        import MODULOS_ACCESO
from models.permiso_perfil  import Permiso_Perfil
from models.perfil          import Perfil


class FormularioPerfilAccesos(QDialog): 
    idPerfil = None
    perfilServices  = PerfilServices()
    permisoServices = PermisosPerfilServices()
    
    def __init__(self, parent=None, id_perfil:int=None):
        super().__init__(parent)
        
        self.setWindowTitle("Perfil de Accesos")
        self.setFixedSize(600, 650)
        self.setObjectName("form")
        
        cargar_estilos('claro','form.css',self)
        # Layout principal
        layout = QVBoxLayout()
        frame = QFrame()
        layout.addWidget(frame)

        # Layout para los inputs
        layoutInputs = QVBoxLayout()

        ## Agregando títulos e inputs
        lblTitulo = QLabel("Crear Perfil" if id_perfil is None else "Editar perfil")
        lblTitulo.setAlignment(Qt.AlignCenter)
        lblTitulo.setObjectName('titulo')

        ##aqui se agregan los inputs para nombre, descripcion y accesos
        layoutInputs.addWidget(lblTitulo)

        ##label e input para el nombre del perfil
        self.lblNombrePerfil = QLabel("Nombre del perfil")
        self.inNombrePerfil = QLineEdit()
        self.inErrorNombrePerfil = QLabel()
        
        ##label e input para la descripcion del perfil
        self.lblDescripcion = QLabel("Descripcion del perfil")
        self.inDescripcion = QLineEdit()
        self.inErrorDescripcion = QLabel()

        # Árbol de accesos y tipoPermisos
        self.ArbolAccesos = QTreeView()
        self.model = QStandardItemModel() ##modelo para el arbol
        self.model.setHorizontalHeaderLabels(["Accesos y tipo de permisos"])
        # Asignar el modelo al árbol
        self.ArbolAccesos.setModel(self.model)

        #lblError de acceso
        self.errAcceso = QLabel("Error al agregar acceso")
        self.errAcceso.setObjectName("lblerror")
        self.errAcceso.setMaximumHeight(25)
        self.errAcceso.setWordWrap(True)
        
        # Botón para agregar accesos
        self.btnAddAccesos = QPushButton("Agregar Acceso")
        self.btnAddAccesos.setObjectName('btnAgregar')
        self.btnAddAccesos.clicked.connect(self.agregarAcceso)
        self.btnAddAccesos.setMaximumSize(100,30)

        # Agregar los widgets al layout de inputs
        layoutInputs.addLayout(self.contenedor(self.lblNombrePerfil,self.inNombrePerfil,self.inErrorNombrePerfil))
        layoutInputs.addLayout(self.contenedor(self.lblDescripcion,self.inDescripcion,self.inErrorDescripcion))
        layoutInputs.addWidget(self.ArbolAccesos)
        layoutInputs.addWidget(self.errAcceso)
        layoutInputs.addWidget(self.btnAddAccesos)

        # Botones de aceptar y cancelar
        boton_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        boton_box.button(QDialogButtonBox.Cancel).setText("Cancelar")
        boton_box.button(QDialogButtonBox.Cancel).setObjectName("btncancelar")
        boton_box.button(QDialogButtonBox.Cancel).setMinimumSize(QSize(100,30))
        boton_box.button(QDialogButtonBox.Cancel).clicked.connect(self.cancelarRegistro)
        
        boton_box.button(QDialogButtonBox.Ok).setText("Registrar")
        boton_box.button(QDialogButtonBox.Ok).setObjectName("btnregistrar")
        boton_box.button(QDialogButtonBox.Ok).setMinimumSize(QSize(100,30))
        boton_box.button(QDialogButtonBox.Ok).clicked.connect(self.registrar)


        if id_perfil:
            self.idPerfil = id_perfil
            self.precargar_datos()

        layoutInputs.addWidget(boton_box)
        # Asignar el layout de inputs al frame
        frame.setLayout(layoutInputs)
        # Asignar el layout principal al QDialog
        self.setLayout(layout)

    def contenedor(self,lblTelefono:QLabel,input,label_error:QLabel)->QVBoxLayout:
            layout = QVBoxLayout()
            layout.setContentsMargins(10,5,10,0)
            layout.setSpacing(0)
            
            label_error.setObjectName("lblerror")
            label_error.setMaximumHeight(25)
            label_error.setMinimumHeight(25)
            label_error.setWordWrap(True)
            
            layout.addWidget(lblTelefono)
            layout.addSpacing(5)
            layout.addLayout(input) if isinstance(input,QVBoxLayout) else layout.addWidget(input)
            layout.addWidget(label_error)
            return layout

    def agregarAcceso(self, objPermiso:Permiso_Perfil=None):
        """Agrega un nuevo acceso al árbol con un ComboBox y un botón de eliminar."""
        # Crear un ítem raíz para el acceso
        itemRaiz = QStandardItem()
        self.model.appendRow(itemRaiz)

        # Crear un widget personalizado para el ComboBox y el botón de eliminar
        widget = QWidget()
        widget.setMinimumWidth(200)
        widget.setMinimumHeight(40)
        #Layout para el widget
        layoutWidget = QHBoxLayout()
        layoutWidget.setContentsMargins(0, 0, 0, 0)

        # ComboBox para seleccionar el acceso
        comboAcceso = QComboBox()
        comboAcceso.currentIndexChanged.connect(self.validarSiRepiteAcceso)
        comboAcceso.wheelEvent = lambda event: event.ignore()

        # Botón para eliminar el acceso
        btnEliminar = QPushButton("Eliminar")
        btnEliminar.setObjectName("btneliminar")
        btnEliminar.setFixedWidth(100)
        btnEliminar.setFixedHeight(30)
        btnEliminar.clicked.connect(lambda _, item=itemRaiz: self.eliminarAcceso(item))

        layoutWidget.addWidget(comboAcceso)
        layoutWidget.addWidget(btnEliminar)
        widget.setLayout(layoutWidget)

        # Insertar el widget en la primera columna
        index = self.model.indexFromItem(itemRaiz)
        self.ArbolAccesos.setIndexWidget(index.sibling(index.row(), 0), widget)

        # cargado de accesos y tipoPermisos
        for data in MODULOS_ACCESO:
            comboAcceso.addItem(data[0], data[1])
        tipoPermisos = [("Ver",False), ("Editar",False), ("Crear",False), ("Eliminar", False)] 
        
        self.validarSiRepiteAcceso()
        #si es cargar un registro recibido desde bd
        if objPermiso: 
            itemRaiz.setData(objPermiso.id, Qt.UserRole)    #guarda id del permiso
            comboAcceso.setCurrentIndex(comboAcceso.findData(objPermiso.tabla))   #selecciona el acceso que esta registrado
            comboAcceso.setEnabled(False)
            tipoPermisos = [("Ver",objPermiso.ver), ("Editar",objPermiso.editar), ("Crear",objPermiso.crear),("Eliminar",objPermiso.eliminar)]

        self.model.dataChanged.connect(self.onDataChanged)
        for tipo in tipoPermisos:
            itemPermiso = QStandardItem(tipo[0])
            itemPermiso.setCheckable(True)
            itemPermiso.setCheckState(Qt.Checked if tipo[1] else Qt.Unchecked) 
            itemPermiso.setEditable(False)
            itemRaiz.appendRow(itemPermiso)

        self.ArbolAccesos.setExpanded(index, True)

    """ accion a manipular los checks de los accesos """
    def onDataChanged(self, topLeft, bottomRight, roles):
        """Slot que se ejecuta cuando cambia el estado de un QCheckBox."""
        if Qt.CheckStateRole in roles:
            itemCambiado = self.model.itemFromIndex(topLeft)
            if itemCambiado is not None and itemCambiado.parent() is not None:
                itemRaiz = itemCambiado.parent()        # Obtener el ítem raíz (padre del ítem cambiado)
                if itemCambiado.text() == "Ver" and itemCambiado.checkState() == Qt.Unchecked:
                    self.desactivarPermisos(itemRaiz)   # Si el ítem cambiado es "Ver" y se desactiva, desactivar los demás
                elif itemCambiado.text() != "Ver" and itemCambiado.checkState() == Qt.Checked:
                    self.activarVer(itemRaiz)           # Si el ítem cambiado no es "Ver" y se activa, activar "Ver"

    def activarVer(self, itemRaiz):
        """Activa el QCheckBox de 'Ver' si no está activado."""
        for child_row in range(itemRaiz.rowCount()):
            itemHijo = itemRaiz.child(child_row)
            if itemHijo.text() == "Ver" and itemHijo.checkState() == Qt.Unchecked:
                itemHijo.setCheckState(Qt.Checked)  #activa ver cuando otros checks(eliminar,crear,editar) se activan

    def desactivarPermisos(self, itemRaiz):
        """Desactiva los QCheckBox de 'Editar', 'Crear' y 'Eliminar'."""
        for child_row in range(itemRaiz.rowCount()):
            itemHijo = itemRaiz.child(child_row)
            if itemHijo.text() in ["Editar", "Crear", "Eliminar"] and itemHijo.checkState() == Qt.Checked:
                itemHijo.setCheckState(Qt.Unchecked)#desactiva votros checks(eliminar,crear,editar) cuando se desactiva el check ver
            
    """ valida todos los inputs """
    def validacionDeTodo(self):
        validacionAceptada = True
        self.inErrorNombrePerfil.setText("")

        print(self.inNombrePerfil.text().strip())
        if not self.inNombrePerfil.text().strip():
            self.inErrorNombrePerfil.setText("Debes ingresar algun nombre al perfil.")
            validacionAceptada = False

        if not self.validarSiRepiteAcceso():
            validacionAceptada = False
        
        return validacionAceptada
    
    """ Validad si se repiten accesos """
    def validarSiRepiteAcceso(self):
        validacionAceptada = True
        error = ""
        listaRevisados = [] #guarda el valor del combobox dupicado
        ##reviso si los accesos estan repetidos.
        for row in range(self.model.rowCount()):
            itemRaiz = self.model.item(row)
            index    = self.model.index(row, 0) 
            widget   = self.ArbolAccesos.indexWidget(index)
            comboAcceso = widget.findChild(QComboBox)
            tabla    = comboAcceso.currentData()
        
            for rowAux in range(self.model.rowCount()):
                itemRaizAux = self.model.item(rowAux)
                indexAux    = self.model.index(rowAux, 0) 
                widgetAux   = self.ArbolAccesos.indexWidget(indexAux)
                comboAccesoAux = widgetAux.findChild(QComboBox)
                tablaAux    = comboAccesoAux.currentData()
                if tablaAux == tabla and itemRaiz != itemRaizAux and not comboAccesoAux.currentText() in listaRevisados:
                    error += f"Hay mas de un acceso \'{comboAccesoAux.currentText()}\'. "
                    listaRevisados.append(comboAccesoAux.currentText())
                    validacionAceptada = False
                    
        ##mostrando mensaje de error
        self.errAcceso.setText(error)
        return validacionAceptada
   
    """Elimina un acceso del árbol, manda a eliminar en bd si el acceso ya esta registrado(solo se ve al editar)"""
    def eliminarAcceso(self, item):
        id_permiso = item.data(Qt.UserRole)

        if id_permiso:
            ##eliminar el permiso en la base de datos
            ## recuerde mostrar una ventana emergente para que el usuario
            ## confirme si desea eliminar el permiso
            ## si el usuario confirma, entonces se elimina el permiso
            ## si el usuario cancela, entonces no se elimina el permiso
            
            dial = DialogoEmergente("","Este acceso ya esta registrado\n¿Estas seguro que quieres eliminar este acceso?","Question",True, True)
            if dial.exec() == QDialog.Accepted:
                print(f"Eliminado {id_permiso}")
                result = self.permisoServices.eliminar_permiso_perfil(id_permiso)

                if not result['success']:
                    dial = DialogoEmergente('','Ocurrio un error al eliminar el perfil.','Error')
                    dial.exec()
                    return

                dial = DialogoEmergente('','Se elimino el acceso correctamente','Check')
                dial.exec()
                self.model.removeRow(item.row())
        else:
            self.model.removeRow(item.row())    ##eliminar el acceso esto cuando es un acceso no registrado en bd
        self.validarSiRepiteAcceso()            ##realiza validacion, congruencia del errAcceso
    
    """Obtiene los permisos del árbol(QTreeWidget) y los devuelve en una lista de objetos Permiso."""
    def obtener_permisos_del_arbol(self):
        """Recorre el árbol y devuelve una lista de objetos Permiso."""
        listaPermisos = []  # lista de permisos
        # Recorrer todas las filas del modelo
        for row in range(self.model.rowCount()):
            itemRaiz    = self.model.item(row)          # Obtener el ítem raíz (permiso)
            id_permiso  = itemRaiz.data(Qt.UserRole)    # Obtener el id del permiso (almacenado en Qt.UserRole)
            # Obtener el widget de la primera columna (que contiene el QComboBox y el botón Eliminar)
            index   = self.model.index(row, 0)          # Obtener el índice del acceso
            widget  = self.ArbolAccesos.indexWidget(index)
            comboAcceso = widget.findChild(QComboBox)   # Obtener el QComboBox del widge
            tabla   = comboAcceso.currentData()         # Obtener el valor seleccionado en el QComboBox (tabla)

            # Obtener los ítems hijos (tipos de permisos: Ver, Editar, Crear, Eliminar)
            ver         = False
            editar      = False
            crear       = False
            eliminar    = False

            for child_row in range(itemRaiz.rowCount()):
                itemHijo = itemRaiz.child(child_row)
                tipo_permiso = itemHijo.text()
                estado = itemHijo.checkState() == Qt.Checked
                if tipo_permiso == "Ver":
                    ver = estado
                elif tipo_permiso == "Editar":
                    editar = estado
                elif tipo_permiso == "Crear":
                    crear = estado
                elif tipo_permiso == "Eliminar":
                    eliminar = estado

            # Crear un objeto Permiso con los datos obtenidos
            permiso = Permiso_Perfil(
                id          = id_permiso,
                perfil_id   = self.idPerfil,
                tabla       = tabla,
                ver         = ver,
                editar      = editar,
                crear       = crear,
                eliminar    = eliminar
            )
            # Agregar el objeto Permiso a la lista
            listaPermisos.append(permiso)

        return listaPermisos
    
    """Obtiene los datos ingresados en el formulario."""
    def obtenerTodoFormulario(self):
        """Obtiene los datos ingresados en el formulario."""
        nombrePerfil = self.inNombrePerfil.text()
        descripcion  = self.inDescripcion.text()

        perfil   = Perfil(nombrePerfil, descripcion)
        permisos = self.obtener_permisos_del_arbol()

        return {"perfil": perfil, "permisos": permisos}
    
    """ Carga el formulario con los datos de un perfil y sus permisos para el caso de editar"""
    def precargar_datos(self):
        # permiso = Permiso_Perfil(1,"empleado",True,True,True,True,1)
        # self.agregarAcceso(permiso)
        # permiso = Permiso_Perfil(1,"usuario",True,True,True,True,2)
        # self.agregarAcceso(permiso)
        """Precarga los datos del formulario para cuando esta editando"""
        
        # mandar a traer el perfil y los permisos del perfil con el id del perfil(no del acceso del perfil)
        # Desde data traer solo una vez el perfil y todos los permisos que tiene ese perfil.
        # enviarlos de desde data asi:
        # { 
        #   "success":True, 
        #   "exists":True, 
        #   "data":{
        #           "perfil":perfil,
        #           "listaPermisos":listaPermisos
        #   }, 
        #   "message":"Perfil encontrado"
        #}

        # Ejemplo
        result = self.perfilServices.obtenerPerfilPorId(self.idPerfil)
        print(self.idPerfil)
        print(result)
        if not result['success']:
            dial = DialogoEmergente("","Ocurrio un error al cargar el perfil para editar.","Error",True, False)
            dial.exec()
            self.reject()
            return 
        
        if not result["exists"]:
            dial = DialogoEmergente("","No se encontraron los datos del perfil.","Error",True, False)
            dial.exec()
            self.reject()
            return 
        
        perfil   = result["data"]["perfil"]
        permisos = result["data"]["listaPermisos"]

        ##cargar los datos del perfil
        self.inNombrePerfil.setText(perfil.nombre)
        self.inDescripcion.setText(perfil.descripcion)

        ##cargar los permisos
        for permiso in permisos:
            self.agregarAcceso(permiso)
    
    def cancelarRegistro(self):
        if self.inNombrePerfil.text().strip() or self.inDescripcion.text().strip() or len(self.obtener_permisos_del_arbol())>0:
            ##mostrar un texto de si quiere cancelar el registor si cancela realizar self.reject()
            dial = DialogoEmergente("","¿Estas seguro que que quieres cancelar?","Error",True, True)
            if dial.exec() == QDialog.Accepted:
                self.reject()
                return
        else:
            self.reject()
            return
            
    """ Envia todo a la bd para ser actualizado o registrado """
    def registrar(self):
        if not self.validacionDeTodo():
            # mostrar una ventana emergente de que tiene que llenar todos los datos.
            dial = DialogoEmergente("","Asegurese de completar los datos correctamente.","Warning",True, False)
            dial.exec()
            return #evita que se proceda a actualizar o crear perfil
        
        if self.idPerfil:   ## se procede a actualizar y mostrar mensaje de confirmacion.
            pass    
        else:               ## se procede a crear y mostrar mensaje de confirmacion.
            pass
