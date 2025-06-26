# Sistema de Logging - Módulo Reutilizable

Este módulo proporciona un sistema de logging centralizado y reutilizable para todo el proyecto de transcripción.

## Características

- ✅ **Logs organizados por fecha** en la carpeta `logs/`
- ✅ **Múltiples loggers** para diferentes módulos
- ✅ **Métodos especializados** para transcripciones, operaciones de archivos y API
- ✅ **Configuración automática** de handlers y formatters
- ✅ **Supresión de logs de framework** (FastAPI/Uvicorn)
- ✅ **Fácil de usar** en cualquier parte del proyecto

## Uso Básico

### Importar el módulo

```python
from logger_config import get_logger, default_logger
```

### Usar el logger por defecto

```python
# Usar el logger por defecto
default_logger.info("Mensaje de información")
default_logger.error("Mensaje de error")
```

### Crear un logger personalizado

```python
# Crear un logger con nombre personalizado
logger = get_logger("mi_modulo")
logger.info("Mensaje desde mi módulo")
```

## Métodos Disponibles

### Métodos Básicos

```python
logger.info("Mensaje de información")
logger.error("Mensaje de error")
logger.warning("Mensaje de advertencia")
logger.debug("Mensaje de debug")
logger.critical("Mensaje crítico")
```

### Métodos Especializados

#### Para Transcripciones

```python
logger.log_transcription_start("video.mp4")
logger.log_transcription_success("video.mp4", 1500)  # 1500 caracteres
logger.log_transcription_error("video.mp4", "Error específico")
```

#### Para Operaciones de Archivos

```python
logger.log_file_operation("read", "/path/to/file.txt", "Leyendo configuración")
logger.log_file_operation("write", "/path/to/output.txt", "Guardando datos")
logger.log_file_operation("delete", "/path/to/temp.txt", "Limpiando archivo temporal")
```

#### Para Requests de API

```python
logger.log_api_request("/transcribe", "POST", "Archivo: video.mp4")
logger.log_api_request("/download/123", "GET", "Descargando transcripción")
```

## Ejemplos de Uso

### En un módulo de procesamiento

```python
from logger_config import get_logger

logger = get_logger("processor")

def process_video(filename):
    logger.log_transcription_start(filename)

    try:
        logger.log_file_operation("read", filename, "Leyendo video")
        # ... procesamiento ...
        logger.log_transcription_success(filename, 2000)
    except Exception as e:
        logger.log_transcription_error(filename, str(e))
```

### En un cliente de API

```python
from logger_config import get_logger

logger = get_logger("api_client")

def make_request(endpoint, method, data=None):
    logger.log_api_request(endpoint, method, f"Datos: {data}")
    # ... hacer request ...
    logger.info("Request completado exitosamente")
```

## Configuración

### Estructura de Archivos

```
logs/
├── transcription_api_20250626.log
├── custom_module_20250626.log
├── file_processor_20250626.log
└── ...
```

### Formato de Logs

```
2025-06-26 17:55:34,597 - transcription_api - INFO - Starting transcription process for file: video.mp4
2025-06-26 17:55:35,123 - transcription_api - INFO - File operation 'save': /tmp/video.mkv - Size: 1024000 bytes
```

## Personalización

### Cambiar el directorio de logs

```python
logger = get_logger("mi_modulo", log_dir="custom_logs")
```

### Cambiar el nivel de logging

```python
# En logger_config.py, cambiar:
self.logger.setLevel(logging.DEBUG)  # Para ver todos los logs
self.logger.setLevel(logging.ERROR)  # Solo errores
```

## Ventajas del Sistema

1. **Consistencia**: Todos los logs siguen el mismo formato
2. **Organización**: Logs separados por módulo y fecha
3. **Reutilización**: Fácil de usar en cualquier parte del proyecto
4. **Mantenibilidad**: Configuración centralizada
5. **Escalabilidad**: Fácil de extender con nuevos métodos

## Archivos del Sistema

- `logger_config.py` - Módulo principal de logging
- `example_usage.py` - Ejemplos de uso
- `LOGGING_README.md` - Esta documentación
- `main.py` - Ejemplo de uso en la API principal
