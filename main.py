import os
import getpass
from descargador import descargar_video
from transcriptor import transcribir_video
from analizador import analizar_con_gemini
from editor import cortar_y_subtitular

def procesar_stream():
    print("="*50)
    print("🤖 INICIANDO GANCHO AI 🤖")
    print("="*50)
    
    # 1. Pedir el link al usuario
    url_video = input("\n🔗 Pega el link del video (YouTube o el .m3u8 de Kick) y presiona Enter:\n> ").strip()
    if not url_video:
        print("❌ No ingresaste ningún enlace. Cancelando ejecución.")
        return

    # 2. Pedir la API Key de forma segura (los caracteres no se verán en pantalla)
    api_key = getpass.getpass("🔑 Pega tu API Key de Gemini y presiona Enter (el texto será invisible por seguridad):\n> ").strip()
    if not api_key:
        print("❌ Necesitas proporcionar una API Key para analizar el texto. Cancelando.")
        return

    # 3. Descargar el video
    ruta_video = descargar_video(url_video)
    if not ruta_video:
        print("🛑 Deteniendo ejecución: No se pudo descargar el archivo.")
        return

    # 4. Transcribir el audio a texto
    print("\n🎙️ Paso 1: Extrayendo y transcribiendo audio con Whisper...")
    datos_transcripcion = transcribir_video(ruta_video)

    # 5. Detectar ganchos con IA (Pasándole la API Key que el usuario escribió)
    print("\n🧠 Paso 2: Gemini está buscando los mejores momentos (Storytimes, Polémicas)...")
    momentos_virales = analizar_con_gemini(datos_transcripcion, api_key)

    if not momentos_virales:
        print("🛑 No se detectaron momentos virales o hubo un error con la IA.")
        return

    # 6. Cortar y generar los clips finales
    print("\n✂️ Paso 3: Cortando y subtitulando clips...")
    cortar_y_subtitular(ruta_video, momentos_virales)
    
    print(f"\n🚀 ¡Proceso terminado! Revisa tu carpeta de clips finales.")
    print(f"📁 El video original quedó guardado intacto en: {ruta_video}")

if __name__ == "__main__":
    procesar_stream()