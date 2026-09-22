import yt_dlp
import os

class DescargadorVideo:
    def __init__(self, carpeta_salida="videos_completos"):
        """Inicializa el descargador y asegura que la carpeta de destino exista."""
        self.carpeta_salida = carpeta_salida
        if not os.path.exists(self.carpeta_salida):
            os.makedirs(self.carpeta_salida)

    def descargar(self, url):
        """Descarga el video en la mejor calidad disponible en formato mp4."""
        print(f"Preparando descarga de: {url}")
        
        opciones = {
            # Busca video y audio en mp4, o el mejor formato unificado
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            # Guarda el archivo con el ID del video para evitar nombres con caracteres raros
            'outtmpl': f'{self.carpeta_salida}/%(id)s.%(ext)s',
            # Evita que yt-dlp llene la consola con demasiada información
            'quiet': False 
        }

        try:
            with yt_dlp.YoutubeDL(opciones) as ydl:
                ydl.download([url])
            print("¡Descarga completada con éxito!")
        except Exception as e:
            print(f"Error durante la descarga: {e}")

# Bloque de ejecución principal
if __name__ == "__main__":
    # URL de prueba: "Me at the zoo" (el primer video de YouTube, dura 18 segundos)
    url_prueba = "https://www.youtube.com/watch?v=jNQXAC9IVRw" 
    
    mi_descargador = DescargadorVideo()
    mi_descargador.descargar(url_prueba)