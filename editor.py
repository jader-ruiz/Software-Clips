import json
import os
import subprocess
import imageio_ffmpeg
from datetime import timedelta

class EditorVideo:
    def __init__(self, carpeta_salida="clips_finales"):
        self.carpeta_salida = carpeta_salida
        if not os.path.exists(self.carpeta_salida):
            os.makedirs(self.carpeta_salida)
        
        self.ruta_ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
        print(f"Editor de video inicializado.")

    def _segundos_a_srt(self, segundos):
        """Convierte segundos (ej. 4.5) al formato SRT (00:00:04,500)"""
        tiempo = timedelta(seconds=float(segundos))
        # Formatear a HH:MM:SS,mmm
        horas, resto = divmod(tiempo.seconds, 3600)
        minutos, segundos = divmod(resto, 60)
        milisegundos = int(tiempo.microseconds / 1000)
        return f"{horas:02d}:{minutos:02d}:{segundos:02d},{milisegundos:03d}"

    def generar_archivo_srt(self, ruta_json_transcripcion, ruta_salida_srt="subtitulos.srt"):
        """Toma el JSON de Whisper y crea un archivo de subtítulos universal"""
        print("Generando archivo de subtítulos SRT...")
        with open(ruta_json_transcripcion, 'r', encoding='utf-8') as f:
            segmentos = json.load(f)

        with open(ruta_salida_srt, 'w', encoding='utf-8') as f:
            for i, seg in enumerate(segmentos, 1):
                inicio_srt = self._segundos_a_srt(seg['inicio'])
                fin_srt = self._segundos_a_srt(seg['fin'])
                texto = seg['texto'].strip()
                
                # Formato estándar de un bloque SRT
                f.write(f"{i}\n")
                f.write(f"{inicio_srt} --> {fin_srt}\n")
                f.write(f"{texto}\n\n")
        
        print(f"Archivo {ruta_salida_srt} creado.")
        # FFmpeg en Windows necesita las barras invertidas dobles o barras normales para leer rutas en los filtros
        return ruta_salida_srt.replace('\\', '/')

    def recortar_clips(self, ruta_video_original, ruta_json_cortes, ruta_json_transcripcion):
        if not os.path.exists(ruta_json_cortes):
            print(f"Error: No se encontró {ruta_json_cortes}")
            return

        # 1. Crear el archivo de subtítulos para todo el video primero
        ruta_srt = self.generar_archivo_srt(ruta_json_transcripcion)

        with open(ruta_json_cortes, 'r', encoding='utf-8') as archivo:
            clips = json.load(archivo)

        print(f"Se encontraron {len(clips)} clip(s) para procesar.")

        for i, clip in enumerate(clips):
            inicio = clip.get('inicio', 0)
            fin = clip.get('fin', 0)
            titulo = clip.get('titulo', f'clip_{i+1}').replace(" ", "_")
            archivo_salida = os.path.join(self.carpeta_salida, f"{titulo}.mp4")
            
            print(f"\nProcesando Clip {i+1}: '{titulo}' (De {inicio}s a {fin}s)")
            
            # EL FILTRO MAESTRO:
            # 1. crop=ih*(9/16):ih -> Recorta a vertical (9:16)
            # 2. eq=saturation=1.1 -> Anti-spam (color)
            # 3. subtitles=... -> Quema los subtítulos usando un estilo amarillo con borde negro
            estilo_subs = "FontName=Arial,FontSize=18,PrimaryColour=&H0000FFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2,Alignment=2,MarginV=50"
            filtro = f"crop=ih*(9/16):ih, eq=saturation=1.1, subtitles={ruta_srt}:force_style='{estilo_subs}'"

            comando = [
                self.ruta_ffmpeg, 
                "-y", 
                "-i", ruta_video_original,
                "-ss", str(inicio),
                "-to", str(fin),
                "-vf", filtro,
                archivo_salida
            ]
            
            try:
                subprocess.run(comando, check=True)
                print(f"¡Clip guardado exitosamente en: {archivo_salida}!")
            except subprocess.CalledProcessError as e:
                print(f"\n--- ERROR AL RECORTAR ---")
                print(f"Falló al procesar el clip '{titulo}'.")

# Bloque de ejecución principal
if __name__ == "__main__":
    mi_editor = EditorVideo()
    # Ahora le pasamos también la transcripción para que pueda hacer los subtítulos
    mi_editor.recortar_clips("videos_completos/jNQXAC9IVRw.mp4", "cortes_sugeridos.json", "transcripcion_actual.json")