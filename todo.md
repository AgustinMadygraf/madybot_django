# Listado de Tareas To Do

A continuación, se indican los pasos prioritarios para migrar la lógica desde Flask a Django, manteniendo ambos servicios funcionales de forma provisional.  
**Nota**: No se incluyen tareas relacionadas con MySQL ni autenticación en Firebase, ya que no son prioritarias en este momento.

## 1. Migración de Lógica de Flask a Django

### 1.1 Centralizar la lógica de vistas y respuestas

#### 1.1.1 Crear un helper de respuesta unificado en Django
- **Archivo a crear:** `core/utils/response.py`
  - **Objetivo:** Unificar la función `render_json_response` que actualmente reside en `componente_flask/view.py`.
  - **Tareas detalladas:**
    1. [x] Crear la función `render_json_response(status_code: int, message: str, stream: bool = False)` en `core/utils/response.py`.
    2. [x] Adaptar la lógica para que retorne un `JsonResponse` propio de Django, pero conservando la estructura `{"response_MadyBot": "...", "response_MadyBot_stream": "..."}`.
    3. [x] Asegurarse de incluir logs similares a los de Flask (usando el `app_logger` o logger configurado).

#### 1.1.2 Eliminar duplicaciones en `componente_flask/view.py`
- **Archivo a modificar/eliminar:** `componente_flask/view.py`
  - **Objetivo:** Migrar toda la lógica de `render_json_response` y dejar el archivo obsoleto.
  - **Tareas detalladas:**
    1. [ ] Copiar el contenido de `render_json_response` a `core/utils/response.py`.
    2. [ ] Reemplazar el contenido de `view.py` por un comentario de advertencia: “Migrado a Django, archivo obsoleto”.
    3. [ ] No borrar todavía el archivo si hay referencias en producción que lo llamen directamente (para evitar romper Flask). Planificar su eliminación definitiva en la fase 3 de este documento.

### 1.2 Migrar rutas y controladores de Flask hacia Django

#### 1.2.1 Ajustar las vistas en `core/views.py`
- **Archivo a modificar:** `core/views.py`
  - **Objetivo:** Incorporar la lógica de `data_controller.py` (Flask) de forma análoga en Django.
  - **Tareas detalladas:**
    1. [ ] Crear una vista `receive_data(request)` que replique el comportamiento de `@data_controller.route(root_API + 'receive-data')`.
        - Incluye la llamada a `data_service.process_incoming_data(...)`.
        - Utiliza el helper `render_json_response` importado desde `core/utils/response.py`.
    2. [ ] Crear la vista `health_check(request)` que devuelva un estado operativo, replicando `@data_controller.route(root_API + 'health-check')`.
    3. [ ] En la vista `home(request)`, opcionalmente redirigir al frontend si `URL_FRONTEND` está configurado o devolver un mensaje de bienvenida (similar a `redirect_to_frontend` en Flask, si se requiere).

#### 1.2.2 Configurar rutas en `core/urls.py`
- **Archivo a modificar:** `core/urls.py`
  - **Objetivo:** Añadir rutas equivalentes a las que existen en Flask (`receive-data`, `health-check`, etc.).
  - **Tareas detalladas:**
    1. [ ] Agregar `path('receive-data/', views.receive_data, name='receive_data')`.
    2. [ ] Agregar `path('health-check/', views.health_check, name='health_check')`.
    3. [ ] Validar que exista `path('', views.home, name='home')` o la ruta que haga la lógica de redirección o bienvenida.

#### 1.2.3 Ajustar el controlador Flask `data_controller.py` para usar la nueva vista Django (provisional)
- **Archivo a modificar:** `componente_flask/controllers/data_controller.py`
  - **Objetivo:** Mantener Flask vivo, pero evitar la duplicación de lógica en `render_json_response` o `DataService`.
  - **Tareas detalladas:**
    1. [ ] Reemplazar la importación de `render_json_response` desde `componente_flask.view` por la función homóloga desde `core/utils/response` (si se decide compartir la misma función).
    2. [ ] Si no se desea compartir la función (para no romper Flask), simplemente marcar con comentarios que la lógica pasará a Django y se mantendrá aquí temporalmente.
    3. [ ] Confirmar que `DataService`, `DataSchemaValidator`, etc. sigan apuntando a la misma ubicación (`core/services/...`) y no dupliquen definiciones.

### 1.3 Convivencia y Desactivación Gradual de Flask

#### 1.3.1 Mantener ambos servidores en paralelo
- **Objetivo:** Permitir que los endpoints de Flask sigan funcionando mientras se prueba la aplicación en Django.
- **Tareas detalladas:**
  1. [ ] Ejecutar `app_flask.py` y `app_django.py` en puertos distintos (por ejemplo, Flask en 5000 y Django en 8000).
  2. [ ] Verificar que las nuevas rutas de Django respondan de forma idéntica a las peticiones.

#### 1.3.2 Redirigir tráfico gradualmente hacia Django
- **Objetivo:** Comenzar a usar Django como principal gestor de peticiones.
- **Tareas detalladas:**
  1. [ ] Configurar en el load balancer o proxy inverso (si existe) una ruta canaria para `/receive-data` que apunte a Django, monitorizar la respuesta.
  2. [ ] Una vez confirmadas las pruebas, apuntar la totalidad de `/receive-data` y `/health-check` hacia la instancia Django.

#### 1.3.3 Eliminar definitivamente la aplicación Flask
- **Objetivo:** Quitar Flask cuando la migración esté comprobada.
- **Tareas detalladas:**
  1. [ ] **Eliminar archivo:** `componente_flask/view.py` (ya obsoleto).
  2. [ ] **Eliminar carpeta:** `componente_flask/controllers/`.
  3. [ ] **Eliminar archivo:** `app_flask.py`.
  4. [ ] Limpiar referencias en `readme.md` u otros lugares donde se mencione la ejecución de Flask.

---

## 2. Ajustes Complementarios (No Prioritarios, Pero Recomendados)

### 2.1 Configuración de Variables de Entorno en Django
- **Archivo a modificar:** `madybot_django/settings.py` o un archivo de arranque tipo `wsgi.py`.
  - **Tareas detalladas:**
    1. [ ] Asegurarse de que `python-dotenv` o similar cargue las mismas variables que utiliza Flask (por ejemplo, `ROOT_API`, `URL_FRONTEND`, etc.).
    2. [ ] Validar que la API Key de Gemini (`GEMINI_API_KEY`) y otras variables se lean correctamente en Django.

### 2.2 Logger Singleton Compartido
- **Objetivo:** Evitar conflictos de configuración entre Flask y Django.
  - **Tareas detalladas:**
    1. [ ] Verificar que `LoggerConfigurator` sea singleton y que no reconfigure el logger innecesariamente en Django.
    2. [ ] Ajustar los filtros si fuera preciso (los definimos en `core/logs/config_logger.py`).

### 2.3 Documentar la Convivencia de Entornos
- **Archivo a modificar:** `readme.md` o `docs/*`
  - **Tareas detalladas:**
    1. [ ] Añadir instrucciones para levantar simultáneamente Flask y Django.
    2. [ ] Incluir notas de uso (ej. “Use `python app_flask.py` en caso de emergencias mientras se migra.”).

---

## 3. Futuras Extensiones (No Inmediatas)

Estas tareas se listan como recordatorio, pero **no se deben ejecutar aún**:

1. **Migración a MySQL**  
   - Configurar `DATABASES` en `settings.py` para MySQL.  
   - Ejecutar migraciones e integrar el ORM de Django cuando haya modelos.  

2. **Integración de Firebase para Autenticación**  
   - Añadir lógica de verificación de tokens JWT en `views.py` o mediante un middleware.  

3. **Pruebas Unitarias y de Integración**  
   - Agregar `pytest` o pruebas nativas de Django en `core/tests.py`.

---

## 4. Verificación de Incongruencias y Riesgos

1. **Riesgo de Desincronización de Variables de Entorno:**  
   - Asegurarse de que tanto Flask como Django carguen las mismas variables para no romper la lógica.  
2. **Riesgo de Duplicación de Paquetes:**  
   - Confirmar que las dependencias (Flask, Django, Marshmallow, etc.) convivan o que no exista un conflicto de versiones en un mismo entorno virtual.  
3. **Riesgo de Llamadas Directas a `componente_flask.view` o `data_controller.py`:**  
   - Hasta que se remueva Flask, revisar que no quede código “huérfano” que lo invoque, lo cual podría romper el flujo si no se ajustan las imports.  
