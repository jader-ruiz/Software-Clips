# Importamos las clases que construimos en los otros archivos
from descargador import DescargadorVideo
from transcriptor import TranscriptorVideo
from analizador import AnalizadorClips
from editor import EditorVideo
import os

def ejecutar_pipeline(url_video):
    print("=== INICIANDO PIPELINE DE CREACIÓN DE CLIPS CON IA ===")
    
    # 1. Descarga
    descargador = DescargadorVideo()
    descargador.descargar(url_video)
    
    # Extraemos el ID del video de la URL para saber cómo se guardó
    # (Una forma simple de hacerlo para este ejemplo)
    video_id = url_video.split("v=")[1].split("&")[0]
    ruta_video = f"videos_completos/{video_id}.mp4"
    
    if not os.path.exists(ruta_video):
        print("Fallo crítico: No se encontró el video descargado.")
        return

    # 2. Transcripción
    transcriptor = TranscriptorVideo()
    transcriptor.transcribir(ruta_video, "transcripcion_actual.json")
    
    # 3. Análisis con IA
    analizador = AnalizadorClips()
    analizador.analizar_transcripcion("transcripcion_actual.json")
    
    # 4. Edición y Subtítulos
    editor = EditorVideo()
    # Le pasamos la ruta del video, los cortes que pensó Llama3 y la transcripción de Whisper
    editor.recortar_clips(ruta_video, "cortes_sugeridos.json", "transcripcion_actual.json")
    
    print("\n=== ¡PROCESO COMPLETADO! Revisa la carpeta 'clips_finales' ===")

if __name__ == "__main__":
    # ¡Aquí pones la URL del video que quieras procesar!
    url = input("Ingresa la URL del video de YouTube: ")
    ejecutar_pipeline(url)
