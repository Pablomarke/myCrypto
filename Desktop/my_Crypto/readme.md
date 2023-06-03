# Aplicación Web para calcular tradeo e inversión de cryptomonedas

Programa creado en python con el framework flask. Desarrollado por Pablo Márquez para el bootcamp de keepCoding.

# Aviso importante !!

Esta app es solo para visualizar datos y jugar con supuestas inversiones. En ningún caso se realizan compras, inversiones o tradeo real. Desaconsejamos invertir en cualquier tipo de cryptomoneda.

# Necesidades previas 
- Necesitas una clave gratuita previa para sustituir en el archivo "key.py"  
```
APIKEY = "Aquí introduce su apikey"
```
- Obtenla aquí: https://www.coinapi.io/

# Instalación
- crear un entorno en python y ejecutar el comando
```
pip install -r requirements.txt
```
la libreria utilizada en flask https://flask.palletsprojects.com/en/2.2.x/

# Opción de ejecucion RECOMENDADA
- instalar
  ```pip install python-dotenv```
- crear un archivo .env y dentro agregar lo siguiente:
``` FLASK_APP=main.py```
``` FLASK_DEBUG=True ```
- y luego para lanzar seria en la terminal el comando:
``` flask run ```

# Ejecucion del programa
- inicializar el servidor de flask
- en mac: ```export FLASK_APP=main.py```
- en windows: ```set FLASK_APP=main.py```

# Comando para ejecutar el servidor:
```flask --app main run```
# Comando para ejecutar el servidor en otro puerto diferente por default es el 5000
```flask --app main run -p 5002```
# Comando para ejecutar el servidor en modo debug, para realizar cambios en tiempo real
```flask --app main --debug run```