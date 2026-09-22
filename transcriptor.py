import whisper
import json
import os

class TranscriptorVideo:
    def __init__(self, modelo_tamano="base"):
        """
        Inicializa el modelo de IA. 
        'base' es rápido y ligero. Si tienes buena PC, luego puedes probar 'small' o 'medium'.
        """
        print(f"Cargando modelo de Whisper '{modelo_tamano}'... (La primera vez descargará el modelo, ten paciencia)")
        self.modelo = whisper.load_model(modelo_tamano)
        print("¡Modelo de IA cargado en memoria!")

    def transcribir(self, ruta_video, ruta_salida_json="transcripcion.json"):
        """
        Analiza el audio del video y extrae el texto junto con los tiempos exactos.
        """
        print(f"Empezando a escuchar y transcribir: {ruta_video}")
        
        # Whisper hace la magia aquí. Extrae el audio del video automáticamente y lo transcribe.
        resultado = self.modelo.transcribe(ruta_video)
        
        segmentos = []
        # resultado['segments'] contiene la lista de frases con su segundo de inicio y fin
        for segmento in resultado['segments']:
            segmentos.append({
                "inicio": segmento['start'],
                "fin": segmento['end'],
                "texto": segmento['text'].strip()
            })
        
        # Guardamos todo en un archivo JSON. Esto será la "comida" para el LLM (Ollama) en el paso 3.
        with open(ruta_salida_json, 'w', encoding='utf-8') as archivo_json:
            json.dump(segmentos, archivo_json, indent=4, ensure_ascii=False)
            
        print(f"Transcripción completada con éxito. Datos guardados en {ruta_salida_json}")
        return segmentos

# Bloque de ejecución principal
if __name__ == "__main__":
    # La ruta del video que descargaste en el paso anterior (Me at the zoo)
    # Verifica que el archivo termine en .mp4. Si terminó en .webm u otro, cámbialo aquí.
    ruta_archivo = "videos_completos/jNQXAC9IVRw.mp4" 
    
    if os.path.exists(ruta_archivo):
        mi_transcriptor = TranscriptorVideo(modelo_tamano="base")
        mi_transcriptor.transcribir(ruta_archivo)
    else:
        print(f"Error: No se encontró el archivo en {ruta_archivo}. Revisa el nombre o la extensión.")