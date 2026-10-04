import yt_dlp
import os
import uuid

def descargar_video(url):
    # Crear la carpeta 'videos_completos' si no existe en el directorio
    carpeta_salida = "videos_completos"
    os.makedirs(carpeta_salida, exist_ok=True)
    
    # Generar un código aleatorio único para el nombre del video
    id_aleatorio = uuid.uuid4().hex[:8]
    nombre_archivo = f"vod_{id_aleatorio}.mp4"
    ruta_salida = os.path.join(carpeta_salida, nombre_archivo)
    
    # Configuración inteligente: soporta m3u8 de Kick y links normales de YouTube
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': ruta_salida,
        'overwrites': True,
        'quiet': False
    }
    
    print(f"\n📥 Iniciando descarga desde: {url}")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"✅ Video descargado y guardado en: {ruta_salida}")
        return ruta_salida
    except Exception as e:
        print(f"❌ Error al descargar el video: {e}")
        return None