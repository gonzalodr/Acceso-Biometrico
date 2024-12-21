# Acceso-Biometrico
 Acceso Biometrico de empleados

markdown
# Guía para Crear y Manejar un Entorno Virtual en Python para el proyecto 
# Acceso Biometrico de Empleados.

## 1. Instalar Python
Asegúrate de tener Python 3.12 instalado en tu sistema. Puedes descargarlo desde [python.org](https://www.python.org/downloads/). 
Durante la instalación, asegúrate de marcar la opción "Add Python to PATH".

## 2. Crear un Entorno Virtual
Para crear un entorno virtual llamado `venv`, sigue estos pasos:

1. **Abre la Terminal o Símbolo del Sistema**:
   - En Windows, busca "cmd" en el menú de inicio.
   - En macOS/Linux, abre la aplicación de Terminal.

2. **Navega a tu Proyecto**:
   Usa el comando `cd` para cambiar al directorio donde quieres crear el entorno virtual. Por ejemplo:
   ```bash
   cd ruta/a/tu/proyecto

   seleciona el directorio del proyecto.
   

3. **Crear el Entorno Virtual**:
   Ejecuta el siguiente comando:
   ```bash
   python -m virtualenv venv
   
   si tienes mas de una version de python indicar la version deseada, preferible la mas reciente, 
   ejecutas el comando especificando la version, ejemplo:
   ```bash
   python -3.12 -m virtualvenv venv
   
   Esto creará una carpeta llamada `venv` en tu directorio actual.

## 3. Activar el Entorno Virtual
Una vez creado, necesitas activar el entorno virtual:

- **En Windows**:
      ```bash
      .\venv\Scripts\activate
  
   si esto no funciona prueba con el siguiete comando en la terminal CMD
      ```bash 
      .\venv\Scripts\activate.bat

- **En macOS/Linux**:
   ````bash
   source venv/bin/activate
  

Cuando esté activado, verás `(venv)` al principio de la línea de comandos.
ejemplo:
   ```bash
   (venv)ruta/a/tu/proyecto>

## 4. Desactivar el Entorno Virtual
Para salir del entorno virtual, ejecuta:
   ```bash
   deactivate


## 5. Cargar Dependencias desde requirements.txt
Si tienes un archivo `requirements.txt`, sigue estos pasos:
Carga las dependecias desde el `requirements.txt`.

# Nota:
   Se deben instalar todas las dependencias mientras el entorno virtual esta encendido,
   esto para evitar conflictos con dependencias del sistema.

1. Asegúrate de que tu entorno esté activado, osea debes ver el `(venv)` al principio de la linea de comandos.

2. Usa este comando para instalar las dependencias:
      ```bash
      pip install -r requirements.txt

3. Para actualizar o instalar una nueva dependecia desde el `requirements.txt`, 
   debes ejecutar el siguiente comando:
      ```bash
      pip install --upgrade -r requirements.txt
   
## 6. ejecucion de pruebas(opcional de hacer)
   Para ejecutar pruebas para revisar el funcionamiento de los modulos puedes seguir los siguientes pasos
1. En la carpeta tests crearas un archivo .py y colocaras al inicio el prefijo (`test_`),
   Ejemplo:
      ```bash
      test_serviceUsuario.py

2. Para ejecutar tus pruebas, abre una terminal y navega hasta la carpeta principal de tu proyecto. 
   Luego escribe:
      ```bash
      python -m unittest discover -s tests

   Esto buscará automáticamente todos los archivos que comienzan con 
   test_ dentro de la carpeta tests/ y ejecutará las pruebas definidas.
## 7. Exportacion de la base de datos
   -Asegurese de que estas exportando la ultima version de la base de datos
   -Crear una base de datos en MySql con el nombre `accesobiometrico`

## Conclusión
¡Ahora sabes cómo crear, activar y desactivar un entorno virtual en Python, así como cargar dependencias desde un archivo `requirements.txt`! Tambien los pasos para importar la base de datos de manera local.
