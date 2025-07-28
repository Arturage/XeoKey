# Servicios

Esta es una aplicación sencilla de gestión de servicios construida con Flask.

## Requisitos

Instala las dependencias con:

```bash
pip install -r requirements.txt
```

## Ejecución

Inicia la aplicación ejecutando:

```bash
python app.py
```

La aplicación se ejecutará en `http://localhost:5000/`.

## Endpoints

- `GET /services` lista todos los servicios.
- `POST /services` crea un nuevo servicio. Requiere JSON con el campo `name`.
- `GET /services/<id>` obtiene un servicio específico.
- `PUT /services/<id>` actualiza un servicio.
- `DELETE /services/<id>` elimina un servicio.

## Pruebas

Ejecuta las pruebas con:

```bash
pytest
```
