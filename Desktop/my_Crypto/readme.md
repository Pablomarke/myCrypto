# Aplicación Web para calcular tradeo de cryptomonedas

Programa hecho en python con el framework flask y JS App Web

# Instalación
- crear un entorno en python y ejecutar el comando
```
pip install -r requirements.txt
```
la libreria utilizada en flask https://flask.palletsprojects.com/en/2.2.x/

# Ejecucion del programa
- inicializar el servidor de flask
- en mac: ```export FLASK_APP=main.py```
- en windows: ```set FLASK_APP=main.py```

# Otra opción de ejecucion
- instalar
  ```pip install python-dotenv```
- crear un archivo .env y dentro agregar lo siguiente:
``` FLASK_APP=main.py```
``` FLASK_DEBUG=True ```
- y luego para lanzar seria en la terminal el comando:
``` flask run ```
# Comando para ejecutar el servidor:
```flask --app main run```
# Comando para ejecutar el servidor en otro puerto diferente por default es el 5000
```flask --app main run -p 5002```
# Comando para ejecutar el servidor en modo debug, para realizar cambios en tiempo real
```flask --app main --debug run```