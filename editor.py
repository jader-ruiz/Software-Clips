import json
import os
import subprocess
import imageio_ffmpeg

class EditorVideo:
    def __init__(self, carpeta_salida="clips_finales"):
        self.carpeta_salida = carpeta_salida
        if not os.path.exists(self.carpeta_salida):
            os.makedirs(self.carpeta_salida)
        
        # Obtenemos la ruta secreta donde Python instaló el FFmpeg portable
        self.ruta_ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
        print(f"Editor de video inicializado.")
        print(f"Usando FFmpeg desde: {self.ruta_ffmpeg}")

    def recortar_clips(self, ruta_video_original, ruta_json_cortes):
        if not os.path.exists(ruta_json_cortes):
            print(f"Error: No se encontró el archivo de cortes {ruta_json_cortes}")
            return

        with open(ruta_json_cortes, 'r', encoding='utf-8') as archivo:
            try:
                clips = json.load(archivo)
            except json.JSONDecodeError:
                print("Error: El archivo de cortes no tiene un formato JSON válido.")
                return

        print(f"Se encontraron {len(clips)} clip(s) para procesar.")

        for i, clip in enumerate(clips):
            inicio = clip.get('inicio', 0)
            fin = clip.get('fin', 0)
            titulo = clip.get('titulo', f'clip_{i+1}').replace(" ", "_")
            
            archivo_salida = os.path.join(self.carpeta_salida, f"{titulo}.mp4")
            
            print(f"\nProcesando Clip {i+1}: '{titulo}' (De {inicio}s a {fin}s)")
            
            # Construimos el comando de FFmpeg
            # Al quitar "-c:v copy", FFmpeg recodificará el video logrando un corte exacto
            comando = [
                self.ruta_ffmpeg, 
                "-y", 
                "-i", ruta_video_original,
                "-ss", str(inicio),
                "-to", str(fin),
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
    # Verifica que la ruta de tu video sea esta
    mi_editor.recortar_clips("videos_completos/jNQXAC9IVRw.mp4", "cortes_sugeridos.json")