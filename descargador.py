import yt_dlp
import os
import imageio_ffmpeg

class DescargadorVideo:
    def __init__(self, carpeta_salida="videos_completos"):
        """Inicializa el descargador y asegura que la carpeta de destino exista."""
        self.carpeta_salida = carpeta_salida
        if not os.path.exists(self.carpeta_salida):
            os.makedirs(self.carpeta_salida)

    def descargar(self, url):
        """Descarga el video en la mejor calidad disponible en formato mp4."""
        print(f"Preparando descarga de: {url}")
        
        # Le preguntamos a Python dónde escondió FFmpeg
        ruta_ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
        
        opciones = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': f'{self.carpeta_salida}/%(id)s.%(ext)s',
            'quiet': False,
            # ESTA ES LA LÍNEA MÁGICA: Le decimos a yt-dlp dónde está FFmpeg
            'ffmpeg_location': ruta_ffmpeg 
        }

        try:
            with yt_dlp.YoutubeDL(opciones) as ydl:
                ydl.download([url])
            print("¡Descarga completada con éxito!")
        except Exception as e:
            print(f"Error durante la descarga: {e}")

# Bloque de ejecución principal (solo para pruebas)
if __name__ == "__main__":
    url_prueba = "https://www.youtube.com/watch?v=jNQXAC9IVRw" 
    mi_descargador = DescargadorVideo()
    mi_descargador.descargar(url_prueba)