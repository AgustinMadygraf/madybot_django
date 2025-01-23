
# MadyBot Backend

Este proyecto implementa el backend para un chatbot interactivo llamado MadyBot. El backend está desarrollado en Python y utiliza Flask y Django para manejar las solicitudes HTTP. La interfaz de usuario está desarrollada en Vue.js y se sirve como una página web.

## Tecnologías Utilizadas

- Python
- Flask
- Django
- Vue.js

## Estructura del Proyecto

```bash
madybot_django/
    app_django.py
    app_flask.py
    manage.py
    todo.md
    componente_flask/
        controllers/
            data_controller.py
        services/
            data_service.py
            response_generator.py
        views/
            data_view.py
    config/
        system_instruction.txt
    core/
        admin.py
        apps.py
        models.py
        tests.py
        urls.py
        views.py
        channels/
            imessaging_channel.py
        logs/
            base_filter.py
            config_logger.py
            dependency_injection.py
            exclude_http_logs_filter.py
            info_error_filter.py
            logging.json
        migrations/
        services/
            data_service.py
            data_validator.py
            llm_client.py
            model_config.py
            response_generator.py
            llm_impl/
                gemini_llm.py
    madybot_django/
        asgi.py
        settings.py
        urls.py
        wsgi.py
```

## Configuración y Ejecución

### Requisitos Previos

- [Pipenv](https://pipenv.pypa.io/en/latest/)
- Clave API de Gemini

### Instalación

1. Clona el repositorio:
    ```sh
    git clone https://github.com/AgustinMadygraf/madybot_django.git
    cd madybot_django
    ```

2. Crea y activa el entorno virtual con Pipenv:
    ```sh
    pipenv install
    pipenv shell
    ```

3. Configura las variables de entorno:
    - Crea un archivo 

.env

 en la raíz del proyecto con el siguiente contenido:
        ```env
        GEMINI_API_KEY="tu_clave_api_aquí"
        IS_DEVELOPMENT=true
        ```

### Ejecución

#### Flask (en funcionamiento)

Para ejecutar el servidor Flask:
```sh
python app_flask.py
```

#### Django (en desarrollo)

Para ejecutar el servidor Django:
```sh
python app_django.py
```

## Funcionalidades Clave

- Integración con la API de Gemini para generación de respuestas.
- Validación de datos entrantes.
- Generación de respuestas en modo normal y streaming.

## Autores

- [AgustinMadygraf](https://github.com/AgustinMadygraf)
```
