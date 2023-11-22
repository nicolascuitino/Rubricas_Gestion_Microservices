FROM python:3.11.5

#Establece el directorio de trabajo en /app
WORKDIR /app

#Copia el archivo requirements.txt al contenedor en /app/
COPY requirements.txt /app/

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

#Copia el contenido del directorio actual al contenedor en /app/
COPY . /app/

#Expone el puerto 8000
EXPOSE 8001

#Comando para ejecutar la aplicación cuando el contenedor se inicia
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]

#comandos:
#imagen django:
#docker build -t coordinadores_microservice .
#docker run -it -p 8001:8001 coordinadores_microservice
#docker-compose:
#docker-compose build
#docker-compose up
#docker-compose down