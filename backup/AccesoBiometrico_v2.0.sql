CREATE TABLE `Asistencia`
(
 `Id`                int NOT NULL ,
 `Id_Empleado`       int NOT NULL ,
 `Fecha`             date NOT NULL ,
 `Estado_Asistencia` varchar(45) NOT NULL ,

PRIMARY KEY (`Id`),
KEY `Id_Empleado` (`Id_Empleado`),
CONSTRAINT `Id_Empleado` FOREIGN KEY `Id_Empleado` (`Id_Empleado`) REFERENCES `Empleado` (`Id`)
);

CREATE TABLE `Departamento`
(
 `Id`          int NOT NULL ,
 `Nombre`      varchar(50) NOT NULL ,
 `Descripcion` varchar(100) NULL ,

PRIMARY KEY (`Id`)
);


CREATE TABLE `Detalle_Asistencia`
(
 `Id`               int NOT NULL ,
 `Id_Asistencia`    int NOT NULL ,
 `Hora_Entrada`     time NOT NULL ,
 `Hora_Salida`      time NOT NULL ,
 `Horas_Trabajadas` decimal(5,2) NOT NULL ,

PRIMARY KEY (`Id`),
KEY `Id_Asistencia` (`Id_Asistencia`),
CONSTRAINT `Id_Asistencia` FOREIGN KEY `Id_Asistencia` (`Id_Asistencia`) REFERENCES `Asistencia` (`Id`)
);


CREATE TABLE `Empleado`
(
 `Id`              int NOT NULL ,
 `Id_Persona`      int NOT NULL ,
 `Id_Departamento` int NULL ,
 `Id_Horario`      int NULL ,

PRIMARY KEY (`Id`),
KEY `Id_Departamento` (`Id_Departamento`),
CONSTRAINT `Id_Departamento` FOREIGN KEY `Id_Departamento` (`Id_Departamento`) REFERENCES `Departamento` (`Id`),
KEY `Id_Horario` (`Id_Horario`),
CONSTRAINT `Id_Horario` FOREIGN KEY `Id_Horario` (`Id_Horario`) REFERENCES `Horario` (`Id`),
KEY `Id_Persona` (`Id_Persona`),
CONSTRAINT `Id_Persona` FOREIGN KEY `Id_Persona` (`Id_Persona`) REFERENCES `Persona` (`Id`)
);



CREATE TABLE `Empleado_Rol`
(
 `Id`          int NOT NULL ,
 `Id_Empleado` int NOT NULL ,
 `Id_Rol`      int NOT NULL ,

PRIMARY KEY (`Id`),
KEY `Id_Empleado` (`Id_Empleado`),
CONSTRAINT `Id_Empleado` FOREIGN KEY `Id_Empleado` (`Id_Empleado`) REFERENCES `Empleado` (`Id`),
KEY `Id_Rol` (`Id_Rol`),
CONSTRAINT `Id_Rol` FOREIGN KEY `Id_Rol` (`Id_Rol`) REFERENCES `Rol` (`Id`)
);


CREATE TABLE `Horario`
(
 `Id`           int NOT NULL ,
 `Dia_Semanal`  varchar(20) NOT NULL ,
 `Tipo_Jornada` varchar(30) NOT NULL ,
 `Hora_Inicio`  time NOT NULL ,
 `Hora_Fin`     time NOT NULL ,
 `Descripcion`  varchar(100) NULL ,

PRIMARY KEY (`Id`)
);



CREATE TABLE `Huella`
(
 `Id`          int NOT NULL ,
 `Id_Empleado` int NOT NULL ,
 `Huella`      varbinary(255) NOT NULL ,

PRIMARY KEY (`Id`),
KEY `Id_Empleado` (`Id_Empleado`),
CONSTRAINT `Id_Empleado` FOREIGN KEY `Id_Empleado` (`Id_Empleado`) REFERENCES `Empleado` (`Id`)
);

CREATE TABLE `Justificacion`
(
 `Id`            int NOT NULL ,
 `Id_Empleado`   int NOT NULL ,
 `Id_Asistencia` int NOT NULL ,
 `Fecha`         date NOT NULL ,
 `Motivo`        varchar(100) NOT NULL ,
 `Descripcion`   text NULL ,

PRIMARY KEY (`Id`),
KEY `FK_2` (`Id_Asistencia`),
CONSTRAINT `FK_18` FOREIGN KEY `FK_2` (`Id_Asistencia`) REFERENCES `Asistencia` (`Id`),
KEY `Id_Empleado` (`Id_Empleado`),
CONSTRAINT `Id_Empleado` FOREIGN KEY `Id_Empleado` (`Id_Empleado`) REFERENCES `Empleado` (`Id`)
);


CREATE TABLE `Mantenimiento`
(
 `Id`               int NOT NULL ,
 `Id_usuario`       int NOT NULL ,
 `Fecha`            date NOT NULL ,
 `Accion_Realizada` varchar(50) NOT NULL ,
 `Descripcion`      text NULL ,

PRIMARY KEY (`Id`),
KEY `FK_1` (`Id_usuario`),
CONSTRAINT `FK_17_1` FOREIGN KEY `FK_1` (`Id_usuario`) REFERENCES `Usuario` (`Id`)
);





CREATE TABLE `Permiso_usuario`
(
 `Id`           int NOT NULL ,
 `Id_usuario`   int NOT NULL ,
 `nombre_tabla` varchar(45) NOT NULL ,
 `Ver`          boolean NOT NULL ,
 `Insertar`     boolean NOT NULL ,
 `Editar`       boolean NOT NULL ,
 `Eliminar`     boolean NOT NULL ,

KEY `Id_usuario` (`Id_usuario`),
CONSTRAINT `FK_17` FOREIGN KEY `Id_usuario` (`Id_usuario`) REFERENCES `Usuario` (`Id`)
);





CREATE TABLE `Persona`
(
 `Id`               int NOT NULL ,
 `Foto`             mediumblob NOT NULL ,
 `Nombre`           varchar(50) NOT NULL ,
 `Apellido1`        varchar(50) NOT NULL ,
 `Apellido2`        varchar(50) NOT NULL ,
 `Fecha_Nacimiento` date NOT NULL ,
 `Cedula`           varchar(20) NOT NULL ,
 `Estado_Civil`     varchar(20) NOT NULL ,
 `Correo`           varchar(max) NOT NULL ,
 `Direccion`        varchar(50) NOT NULL ,

PRIMARY KEY (`Id`),
UNIQUE KEY `AK1_Persona` (`Cedula`),
UNIQUE KEY `Correo` (`Correo`)
);







CREATE TABLE `Reporte`
(
 `Id`               int NOT NULL ,
 `Id_Empleado`      int NULL ,
 `Fecha_Generacion` date NULL ,
 `Tipo_Reporte`     varchar(50) NULL ,
 `Contenido`        text NULL ,

PRIMARY KEY (`Id`),
KEY `Id_Empleado` (`Id_Empleado`),
CONSTRAINT `Id_Empleado` FOREIGN KEY `Id_Empleado` (`Id_Empleado`) REFERENCES `Empleado` (`Id`)
);


CREATE TABLE `Rol`
(
 `Id`          int NOT NULL ,
 `Nombre`      varchar(50) NOT NULL ,
 `Descripcion` varchar(100) NULL ,

PRIMARY KEY (`Id`)
);




CREATE TABLE `Solicitud_Permiso`
(
 `Id`           int NOT NULL ,
 `Id_Empleado`  int NOT NULL ,
 `Tipo`         varchar(50) NOT NULL ,
 `Fecha_Inicio` date NOT NULL ,
 `Fecha_Fin`    date NOT NULL ,
 `Descripcion`  text NOT NULL ,
 `Estado`       varchar(20) NOT NULL ,

PRIMARY KEY (`Id`),
KEY `Id_Empleado` (`Id_Empleado`),
CONSTRAINT `Id_Empleado` FOREIGN KEY `Id_Empleado` (`Id_Empleado`) REFERENCES `Empleado` (`Id`)
);


CREATE TABLE `Telefono`
(
 `Id`            int NOT NULL ,
 `Id_Persona`    int NOT NULL ,
 `Numero`        varchar(15) NOT NULL ,
 `Tipo_Contacto` varchar(45) NOT NULL ,

PRIMARY KEY (`Id`),
KEY `Id_Persona` (`Id_Persona`),
CONSTRAINT `Id_Persona` FOREIGN KEY `Id_Persona` (`Id_Persona`) REFERENCES `Persona` (`Id`)
);



CREATE TABLE `Usuario`
(
 `Id`         int NOT NULL ,
 `Id_Persona` int NOT NULL ,
 `Usuario`    varchar(50) NOT NULL ,
 `Contrasena` varchar(100) NOT NULL ,

PRIMARY KEY (`Id`),
UNIQUE KEY `AK1_Usuario` (`Usuario`),
KEY `Id_Persona` (`Id_Persona`),
CONSTRAINT `Id_Persona` FOREIGN KEY `Id_Persona` (`Id_Persona`) REFERENCES `Persona` (`Id`)
);



CREATE TABLE `Usuario_Rol`
(
 `Id`         int NOT NULL ,
 `Id_Usuario` int NOT NULL ,
 `Id_Rol`     int NOT NULL ,

PRIMARY KEY (`Id`),
KEY `Id_Rol` (`Id_Rol`),
CONSTRAINT `Id_Rol` FOREIGN KEY `Id_Rol` (`Id_Rol`) REFERENCES `Rol` (`Id`),
KEY `Id_Usuario` (`Id_Usuario`),
CONSTRAINT `Id_Usuario` FOREIGN KEY `Id_Usuario` (`Id_Usuario`) REFERENCES `Usuario` (`Id`)
);


