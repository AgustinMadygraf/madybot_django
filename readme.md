# MadyBot Flask

## Descripción

Chatbot conversacional que aspira a tener múltiples agentes. En principio, tiene un agente que brinda asistencia técnica y capacitaciones en ingeniería financiera. Aspiramos a que además proporcione asistencia técnica en el uso del ERP Xubio mediante RAG (MySQL) y, mediante la API de Xubio, poder conocer variables como el stock de inventarios de materia prima, producto final y productos intermedios.

## Funcionalidades Clave

- Asistencia técnica en ingeniería financiera.
- Capacitación en herramientas financieras.
- Integración con el ERP Xubio para gestionar y monitorear inventarios mediante RAG y MySQL.
- Consulta de variables de inventario como stock de materia prima, producto final y productos intermedios a través de la API de Xubio.

## Instalación

1. Clona el repositorio:
    ```bash
    git clone https://github.com/AgustinMadygraf/madybot_flask.git
    cd madybot_flask
    ```

2. Configura el entorno virtual usando Pipenv:
    ```bash
    pipenv shell
    ```

3. Instala las dependencias:
    ```bash
    pipenv install
    ```

## Ejecución

1. Ejecuta la aplicación:
    ```bash
    python app_flask.py
    ```

## Estructura del Proyecto

```
madybot_flask/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   └── ...
├── tests/
│   └── test_app.py
├── Pipfile
├── Pipfile.lock
├── readme.md
└── ...
```

## Tecnologías Utilizadas

- Python 3.x
- Flask
- MySQL
- Pipenv

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para cualquier mejora o corrección.

## Autor

[Tu Nombre](https://github.com/tu_usuario)

## Licencia

Este proyecto está licenciado bajo la Licencia MIT.
