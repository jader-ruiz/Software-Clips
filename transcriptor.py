import whisper
import json
import os
import subprocess
import imageio_ffmpeg
import numpy as np
import soundfile as sf

class TranscriptorVideo:
    def __init__(self, modelo_tamano="base"):
        print(f"Cargando modelo de Whisper '{modelo_tamano}'...")
        self.modelo = whisper.load_model(modelo_tamano)
        self.ruta_ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
        print("¡Modelo de IA cargado en memoria!")

    def _extraer_audio(self, ruta_video, ruta_audio_temporal="temp_audio.wav"):
        """Usa nuestro FFmpeg interno para extraer el audio en formato WAV (16kHz)"""
        print("Extrayendo audio para Whisper...")
        comando = [
            self.ruta_ffmpeg,
            "-y", 
            "-i", ruta_video,
            "-vn", 
            "-acodec", "pcm_s16le", 
            "-ar", "16000", 
            "-ac", "1", 
            ruta_audio_temporal
        ]
        try:
            subprocess.run(comando, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return ruta_audio_temporal
        except subprocess.CalledProcessError:
            print("Error extrayendo audio con FFmpeg.")
            return None

    def transcribir(self, ruta_video, ruta_salida_json="transcripcion_actual.json"):
        print(f"Empezando proceso de transcripción de: {ruta_video}")
        
        ruta_audio = self._extraer_audio(ruta_video)
        
        if not ruta_audio:
            print("Abortando transcripción por fallo en extracción de audio.")
            return None

        print("Audio extraído. Iniciando reconocimiento de voz (esto tomará un momento)...")
        
        try:
            # EL TRUCO: Leemos el WAV directamente a la RAM
            audio_data, _ = sf.read(ruta_audio)
            
            # Whisper necesita que los datos sean de tipo float32
            audio_data = audio_data.astype(np.float32)

            # Le pasamos el audio ya procesado, así Whisper NO llama a su propio FFmpeg
            resultado = self.modelo.transcribe(audio_data)
            
            segmentos = []
            for segmento in resultado['segments']:
                segmentos.append({
                    "inicio": segmento['start'],
                    "fin": segmento['end'],
                    "texto": segmento['text'].strip()
                })
            
            with open(ruta_salida_json, 'w', encoding='utf-8') as archivo_json:
                json.dump(segmentos, archivo_json, indent=4, ensure_ascii=False)
                
            print(f"Transcripción completada con éxito. Datos guardados en {ruta_salida_json}")
            
        except Exception as e:
            print(f"Error durante la transcripción: {e}")
            
        finally:
            # Limpiamos la casa, pase lo que pase
            if os.path.exists(ruta_audio):
                os.remove(ruta_audio)
            
        return segmentos

if __name__ == "__main__":
    ruta_archivo = "videos_completos/QkFwNr0lwaQ.mp4" 
    if os.path.exists(ruta_archivo):
        mi_transcriptor = TranscriptorVideo()
        mi_transcriptor.transcribir(ruta_archivo)