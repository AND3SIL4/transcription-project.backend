import os
from dotenv import load_dotenv
from io import BytesIO
from elevenlabs.client import ElevenLabs
from moviepy import VideoFileClip
import logging

# Configurar logging
logging.basicConfig(
    filename="script.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Cargar variables de entorno
load_dotenv()

# Inicializar cliente de ElevenLabs
elevenlabs = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY"),
)

# Ruta al archivo de video local
video_path = "./video.mkv"

# Extraer audio del video
video = VideoFileClip(video_path)
audio_path = "temp_audio.mp3"  # Archivo temporal para almacenar el audio extraído
if video.audio is not None:
    logging.info(f"Audio duration: {video.audio.duration}")
    video.audio.write_audiofile(audio_path)
    video.audio.close()
else:
    raise ValueError("No se encontró flujo de audio en el video.")
video.close()

# Leer el audio extraído en un objeto BytesIO
with open(audio_path, "rb") as audio_file:
    audio_data = BytesIO(audio_file.read())

# Realizar conversión de voz a texto
transcription = elevenlabs.speech_to_text.convert(
    file=audio_data,
    model_id="scribe_v1",  # Modelo a usar, por ahora solo "scribe_v1" está soportado
    tag_audio_events=True,  # Etiquetar eventos de audio como risa, aplausos, etc.
    language_code="es",  # Idioma del archivo de audio. Si se establece en None, el modelo detectará el idioma automáticamente.
    diarize=True,  # Si se debe anotar quién está hablando
)

# Guardar transcripción en un archivo
with open("transcription.txt", "w", encoding="utf-8") as f:
    f.write(transcription.text)

# Registrar la transcripción
logging.info(transcription.text)

# Limpiar el archivo de audio temporal
os.remove(audio_path)
