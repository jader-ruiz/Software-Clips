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

    def _segundos_a_srt(self, segundos):
        tiempo = timedelta(seconds=float(segundos))
        horas, resto = divmod(tiempo.seconds, 3600)
        minutos, segundos = divmod(resto, 60)
        milisegundos = int(tiempo.microseconds / 1000)
        return f"{horas:02d}:{minutos:02d}:{segundos:02d},{milisegundos:03d}"

    def generar_archivo_srt(self, ruta_json_transcripcion, ruta_salida_srt="subtitulos.srt"):
        with open(ruta_json_transcripcion, 'r', encoding='utf-8') as f:
            segmentos = json.load(f)

        with open(ruta_salida_srt, 'w', encoding='utf-8') as f:
            contador = 1
            for seg in segmentos:
                palabras = seg['texto'].split()
                inicio_seg = float(seg['inicio'])
                fin_seg = float(seg['fin'])
                duracion_total = fin_seg - inicio_seg
                
                # INGENIERÍA DE SUBTÍTULOS: Dividimos en grupos de máximo 4 palabras
                tamano_grupo = 4
                for j in range(0, len(palabras), tamano_grupo):
                    grupo = palabras[j:j+tamano_grupo]
                    
                    # Interpolación de tiempo para los fragmentos cortos
                    fraccion_inicio = j / max(len(palabras), 1)
                    fraccion_fin = min(j + tamano_grupo, len(palabras)) / max(len(palabras), 1)
                    
                    tiempo_inicio = inicio_seg + (duracion_total * fraccion_inicio)
                    tiempo_fin = inicio_seg + (duracion_total * fraccion_fin)
                    
                    f.write(f"{contador}\n")
                    f.write(f"{self._segundos_a_srt(tiempo_inicio)} --> {self._segundos_a_srt(tiempo_fin)}\n")
                    f.write(f"{' '.join(grupo)}\n\n")
                    contador += 1
        
        return ruta_salida_srt.replace('\\', '/')

    def recortar_clips(self, ruta_video_original, ruta_json_cortes, ruta_json_transcripcion, video_id="default"):
        # CREACIÓN DINÁMICA DE CARPETAS
        carpeta_video = os.path.join(self.carpeta_salida, video_id)
        if not os.path.exists(carpeta_video):
            os.makedirs(carpeta_video)

        ruta_srt = self.generar_archivo_srt(ruta_json_transcripcion)

        with open(ruta_json_cortes, 'r', encoding='utf-8') as archivo:
            clips = json.load(archivo)

        print(f"Renderizando {len(clips)} clips en la carpeta: {carpeta_video}")

        for i, clip in enumerate(clips):
            inicio = clip.get('inicio', 0)
            fin = clip.get('fin', 0)
            titulo = clip.get('titulo', f'clip_{i+1}').replace(" ", "_")
            archivo_salida = os.path.join(carpeta_video, f"{titulo}.mp4")
            
            # ESTILO PREMIUM: Texto blanco pequeño, caja de fondo semitransparente (BorderStyle=3)
            estilo = "FontName=Arial,FontSize=14,PrimaryColour=&H00FFFFFF,BorderStyle=3,Outline=1,Shadow=0,BackColor=&H80000000,Alignment=2,MarginV=40"
            filtro = f"crop=ih*(9/16):ih, eq=saturation=1.1, subtitles={ruta_srt}:force_style='{estilo}'"

            comando = [
                self.ruta_ffmpeg, 
                "-y", 
                "-i", ruta_video_original,
                "-ss", str(inicio),
                "-to", str(fin),
                "-map", "0:v:0",  # Fuerza la extracción de video
                "-map", "0:a:0?", # Fuerza la extracción de audio
                "-vf", filtro,
                "-c:v", "libx264",
                "-preset", "ultrafast", # MODO TURBO para tu procesador
                "-c:a", "aac",
                "-b:a", "192k",
                archivo_salida
            ]
            
            try:
                # Ocultamos el exceso de texto de FFmpeg para limpiar la consola
                subprocess.run(comando, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f" Clip {i+1} guardado: {titulo}.mp4")
            except subprocess.CalledProcessError:
                print(f" Error al procesar el clip '{titulo}'.")