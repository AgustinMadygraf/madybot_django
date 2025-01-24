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

2. Crea un entorno virtual:
    ```bash
    virtualenv -p python3 env
    ```

3. Activa el entorno virtual:
    ```bash
    # En Windows
    .\env\Scripts\Activate
    ```

4. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

## Ejecución

1. Ejecuta la aplicación:
    ```bash
    python app_flask.py
    ```

## Estructura del Proyecto

```
madybot_flask/
├── core/
│   ├── logs/
│   ├── services/
│   └── utils/
├── env/
├── .env
├── .gitignore
├── app_flask.py
├── readme.md
└── requirements.txt
```

## Tecnologías Utilizadas

- Python 3.x
- Flask
- Flask-CORS
- Python-dotenv
- Google Generative AI
- Marshmallow
- Virtualenv

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para cualquier mejora o corrección.

## Autor

[AgustinMadygraf](https://github.com/AgustinMadygraf)
