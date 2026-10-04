import os
import subprocess

def cortar_y_subtitular(ruta_video, momentos_virales):
    # 1. Crear el ecosistema de carpetas para mantener todo limpio
    carpeta_clips = "clips_finales"
    carpeta_subs = "subtitulos"
    carpeta_temp = "temp"
    
    for carpeta in [carpeta_clips, carpeta_subs, carpeta_temp]:
        os.makedirs(carpeta, exist_ok=True)
        
    nombre_base = os.path.splitext(os.path.basename(ruta_video))[0]
    
    for i, clip in enumerate(momentos_virales):
        titulo = clip.get('titulo', f'Clip_{i}')
        # Limpiar el título para evitar errores de guardado en Windows
        titulo_limpio = "".join(x for x in titulo if x.isalnum() or x == "_")
        
        inicio = clip.get('inicio', 0)
        fin = clip.get('fin', 0)
        
        # 2. Rutas organizadas hacia sus respectivas carpetas
        ruta_srt = os.path.join(carpeta_subs, f"{nombre_base}_{titulo_limpio}.srt")
        ruta_salida = os.path.join(carpeta_clips, f"{nombre_base}_{titulo_limpio}.mp4")
        
        print(f"\n✂️ Procesando clip: {titulo}")
        
        # -------------------------------------------------------------
        # AQUÍ VA LA LÓGICA DE FFMPEG.
        # Ejemplo del corte base adaptado a formato vertical 9:16
        # -------------------------------------------------------------
        comando_ffmpeg = [
            "ffmpeg", "-y",
            "-ss", str(inicio),
            "-to", str(fin),
            "-i", ruta_video,
            "-vf", "crop=ih*9/16:ih", # Convierte el stream horizontal a vertical TikTok
            "-c:a", "copy",
            ruta_salida
        ]
        
        subprocess.run(comando_ffmpeg, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        print(f"✅ Clip finalizado en: {ruta_salida}")