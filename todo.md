
### 2. **Revisar la estructura de las interfaces y servicios LLM**
2.1 **Dividir interfaz en métodos streaming y no-streaming (ISP)**  
   - **Objetivo**: Asegurar que cada clase LLM implemente solo los métodos que realmente necesita.  
   - **Acciones**:  
     - Crear `IBaseLLMClient` con el método esencial `send_message`.  
     - Crear `IStreamingLLMClient` que extienda de `IBaseLLMClient` e incluya `send_message_streaming`.  
   - **Archivos a modificar**:  
     - `core/services/llm_client.py` (Reemplazar o subdividir la interfaz existente en dos).  

2.2 **Actualizar implementaciones que hereden de la interfaz**  
   - **Objetivo**: Alinear cada cliente con la nueva interfaz correspondiente.  
   - **Acciones**:  
     - `GeminiLLMClient` que implemente `IStreamingLLMClient` (si soporta streaming) o solo `IBaseLLMClient` (si no lo soporta).  
     - `DeepSeek_llm.py` (si no soporta streaming, implementar la interfaz base).  
   - **Archivos a modificar**:  
     - `core/services/llm_impl/gemini_llm.py` (Implementar la interfaz correcta).  
     - `core/services/llm_impl/DeepSeek_llm.py` (Implementar la interfaz correcta).

---

### 3. **Refactorizar `ResponseGenerator` (SRP y DIP)**
3.1 **Eliminar lógica redundante de sesión en `ResponseGenerator`**  
   - **Objetivo**: Garantizar que `ResponseGenerator` sea agnóstico del tipo de LLM que se usa.  
   - **Acciones**:  
     - Retirar la lógica `_gemini_start_chat` si se considera muy específica.  
     - Invocar directamente métodos de la interfaz (por ejemplo, `send_message`) y delegar la creación de “sesiones” a cada cliente.  
   - **Archivos a modificar**:  
     - `core/services/response_generator.py`.  

3.2 **Inyectar `ILLMClient` por constructor**  
   - **Objetivo**: Cumplir con DIP (que `ResponseGenerator` no conozca concreciones).  
   - **Acciones**:  
     - Mantener el parámetro `llm_client` en el constructor.  
     - Eliminar referencias a clases concretas (`GeminiLLMClient`) dentro de `ResponseGenerator`.  
   - **Archivos a modificar**:  
     - `core/services/response_generator.py`.  

3.3 **Uso del método streaming**  
   - **Objetivo**: Separar la generación de respuesta normal de la lógica de “streaming”.  
   - **Acciones**:  
     - En `ResponseGenerator`, si el cliente inyectado implementa `IStreamingLLMClient`, se usa `send_message_streaming`; en caso contrario, se recurre a `send_message`.  
   - **Archivos a modificar**:  
     - `core/services/response_generator.py`.  

---

### 4. **Organizar el arranque del servidor (SRP y DIP)**
4.1 **Crear clase o función `ServerLauncher`**  
   - **Objetivo**: Extraer la lógica de arranque de Flask en un lugar dedicado.  
   - **Acciones**:  
     - Crear un nuevo archivo `core/launcher/server_launcher.py` para iniciar el servidor.  
     - Invocar la lectura de configuración desde `flask_config.py` y registrar el blueprint.  
   - **Archivos a crear**:  
     - `core/launcher/server_launcher.py`.  
   - **Archivos a modificar**:  
     - `app_flask.py` (Se quedará casi vacío; solo llamará a `ServerLauncher`).

4.2 **Manejar gracefully la ejecución de URL Service**  
   - **Objetivo**: Asegurar que si falla la obtención de la URL pública no caiga toda la app.  
   - **Acciones**:  
     - En `ServerLauncher`, envolver la llamada al servicio `UrlService` en un try-catch.  
     - Definir un fallback (por ejemplo, usar `localhost`) si no funciona la obtención de la URL.  
   - **Archivos a modificar**:  
     - `core/launcher/server_launcher.py`.  

---

### 5. **Crear o refinar pruebas unitarias (según se necesite)**
5.1 **Testear la nueva arquitectura de LLMClients**  
   - **Objetivo**: Verificar que cada implementación (`GeminiLLMClient`, `DeepSeek_llm`) cumpla con su interfaz y maneje errores apropiadamente.  
   - **Acciones**:  
     - Crear tests unitarios para `GeminiLLMClient`, especialmente para `send_message` y `send_message_streaming` (si aplica).  
     - Añadir mocks/fakes para simular respuestas de la API en `DeepSeek_llm`.  
   - **Archivos a crear**:  
     - `tests/test_gemini_llm.py`.  
     - `tests/test_deepseek_llm.py`.  

5.2 **Testear `ResponseGenerator`**  
   - **Objetivo**: Verificar que la clase respete DIP y se apoye en la interfaz en lugar de la implementación concreta.  
   - **Acciones**:  
     - Usar un mock de `ILLMClient` para comprobar que `ResponseGenerator` llama a los métodos correctos.  
   - **Archivos a crear**:  
     - `tests/test_response_generator.py`.  

5.3 **Testear `ServerLauncher`**  
   - **Objetivo**: Confirmar que levantar el servidor funciona sin romper la producción y manejar correctamente los errores.  
   - **Acciones**:  
     - Mock de `UrlService` para simular fallas y éxitos en la obtención de la URL.  
   - **Archivos a crear**:  
     - `tests/test_server_launcher.py`.  

---

### 6. **Depuración y eliminación de código obsoleto**
6.1 **Eliminar configuraciones duplicadas**  
   - **Objetivo**: Evitar sobrecarga de definiciones en múltiples sitios de la app.  
   - **Acciones**:  
     - Revisar si hay archivos de configuración obsoletos tras la creación de `flask_config.py`.  
     - Eliminar duplicados.  
   - **Archivos a eliminar o modificar**:  
     - Cualquier archivo .py que solía cargar config de forma duplicada.  

6.2 **Eliminar métodos no utilizados**  
   - **Objetivo**: Mantener la base de código limpia.  
   - **Acciones**:  
     - Hacer un barrido en cada clase para ver si hay métodos “dummy” sin uso o que puedan convertirse en privados.  
   - **Archivos a modificar**:  
     - Dependiendo de lo que encuentres en `core/services/`, `componente_flask/services/`, etc.  

---

### 7. **Despliegue progresivo y validación en entorno de staging**
7.1 **Actualizar la documentación**  
   - **Objetivo**: Asegurarte de que los cambios de arquitectura y nuevas clases estén documentados.  
   - **Acciones**:  
     - Actualizar el README con las instrucciones para iniciar el servidor (`ServerLauncher`) y cómo inyectar distintos LLMClients.  
     - Documentar cómo correr las pruebas unitarias.  
   - **Archivos a modificar**:  
     - `README.md`.  

7.2 **Desplegar en un entorno de staging**  
   - **Objetivo**: Validar que todo funcione antes de subir a producción.  
   - **Acciones**:  
     - Subir tus cambios a un branch de integración.  
     - Ejecutar todos los tests y validaciones.  
     - Probar manualmente la app (endpoints Flask, LLMClients, etc.).  

7.3 **Despliegue final en producción**  
   - **Objetivo**: Poner la versión estable en el entorno productivo.  
   - **Acciones**:  
     - Hacer merge a la rama principal.  
     - Generar una release tag.  
     - Confirmar logs y monitoreo estén funcionando con la nueva configuración.  
