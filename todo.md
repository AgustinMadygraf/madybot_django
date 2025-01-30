### Nueva Estructura de Carpetas y Ubicación de Archivos

#### 4. **Servicios**
- `app/services/`
  - `__init__.py`
  - `business_rules_engine.py` (mover desde `core_services/business_rules_engine.py`)
  - `data_service.py` (mover desde `core_services/data_service.py`)
  - `data_validator.py` (mover desde `core_services/data_validator.py`)
  - `llm_client.py` (mover desde `core_services/llm_client.py`)
  - `model_config.py` (mover desde `core_services/model_config.py`)
  - `ngrok_api.py` (mover desde `core_services/ngrok_api.py`)
  - `ngrok_error_handler.py` (mover desde `core_services/ngrok_error_handler.py`)
  - `ngrok_manager.py` (mover desde `core_services/ngrok_manager.py`)
  - `ngrok_session.py` (mover desde `core_services/ngrok_session.py`)
  - `response_generator.py` (mover desde `core_services/response_generator.py`)
  - `url_service.py` (mover desde `core_services/url_service.py`)
  - `llm_impl/`
    - `deep_seek_llm.py` (mover desde `core_services/llm_impl/deep_seek_llm.py`)
    - `gemini_llm.py` (mover desde `core_services/llm_impl/gemini_llm.py`)


#### 9. **Estáticos y Plantillas**
- `static/`
- `templates/`