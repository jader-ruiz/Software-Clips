# Importamos las clases que construimos en los otros archivos
from descargador import DescargadorVideo
from transcriptor import TranscriptorVideo
from analizador import AnalizadorClips
from editor import EditorVideo
import os

def ejecutar_pipeline(url_video, api_key):
    print("=== INICIANDO PIPELINE DE CREACIÓN DE CLIPS CON IA ===")
    
    descargador = DescargadorVideo()
    descargador.descargar(url_video)
    
    # Extraemos el ID para nombrar todo de forma única
    video_id = url_video.split("v=")[1].split("&")[0]
    ruta_video = f"videos_completos/{video_id}.mp4"
    
    # Nombres de archivo dinámicos basados en el ID del video
    ruta_transcripcion = f"transcripcion_{video_id}.json"
    ruta_cortes = f"cortes_{video_id}.json"
    
    if not os.path.exists(ruta_video):
        print("Fallo crítico: No se encontró el video descargado.")
        return

    transcriptor = TranscriptorVideo()
    transcriptor.transcribir(ruta_video, ruta_transcripcion)
    
    analizador = AnalizadorClips(api_key)
    # Guardamos los cortes con el nombre dinámico
    clips = analizador.analizar_transcripcion(ruta_transcripcion)
    if clips:
        with open(ruta_cortes, 'w', encoding='utf-8') as f:
            import json
            json.dump(clips, f, indent=4, ensure_ascii=False)
            
        editor = EditorVideo()
        editor.recortar_clips(ruta_video, ruta_cortes, ruta_transcripcion, video_id)
    else:
        # Si la IA falla, detenemos el proceso con un mensaje claro
        print("\n[!] Proceso detenido: La IA no pudo generar los cortes sugeridos.")
    
    print("\n=== ¡PROCESO COMPLETADO! Revisa la carpeta 'clips_finales' ===")

if __name__ == "__main__":
    url = input("Ingresa la URL del video de YouTube: ")
    # Pedimos la llave secreta
    llave = input("Ingresa tu API Key de Google Gemini: ")
    
    # IMPORTANTE: Asegúrate de actualizar la definición de la función arriba a:
    # def ejecutar_pipeline(url_video, api_key):
    ejecutar_pipeline(url, llave)
