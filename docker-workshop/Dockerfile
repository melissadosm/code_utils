#From image tag (search in dockerfile for image tag)
# From program: tag
FROM python:3.7-alpine

# you might need these envs
ENV APP=/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# WORKDIR Change the default directory
# Variable de entorno. Cambiar de carpeta (WORKDIR) Directorio ($APP) ver la carpeta
WORKDIR $APP

# Copy move files od folders from the host to the container
# Mover files que necesitamos a nuestro contenedor
# COPY . $APP se mueve todo de la carpeta APP
# Copiar al host los archivos que necesitamos solo requirements and main
COPY requirements.txt $APP/
COPY app/main.py $APP

# If using alpine the package manager is called pip, you might need this
RUN apk update && apk upgrade && pip install -U pip
RUN apk add build-base linux-headers

#Definir puerto
ENV PORT 5001

# Gunicorn will be the http server running the app
CMD gunicorn -b :$PORT main:app --timeout 600
