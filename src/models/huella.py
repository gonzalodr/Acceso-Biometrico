class Huella:
    def __init__(
        self,
        fid: int,  # ID de la huella (en el dispositivo)
        user_id: int,  # ID del usuario en el dispositivo
        uid: int,  # UID interno del dispositivo
        id_empleado: int = 0,  # ID de tu sistema local
        valida: bool = True,  # Si la huella es válida
    ):
        self.fid = fid
        self.user_id = user_id
        self.uid = uid
        self.id_empleado = id_empleado
        self.valida = valida
