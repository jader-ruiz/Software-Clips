import whisper
import os
import json

def transcribir_video(ruta_video):
    # 1. Crear carpeta exclusiva para las transcripciones
    carpeta_salida = "transcripciones"
    os.makedirs(carpeta_salida, exist_ok=True)
    
    # 2. Generar la ruta del archivo JSON basándonos en el nombre del video
    nombre_base = os.path.splitext(os.path.basename(ruta_video))[0]
    ruta_json = os.path.join(carpeta_salida, f"{nombre_base}.json")
    
    # 3. Caché de desarrollo (evita esperar horas si se te corta el internet)
    if os.path.exists(ruta_json):
        print(f"✅ [Caché] Transcripción ya existe, cargando desde: {ruta_json}")
        with open(ruta_json, "r", encoding="utf-8") as f:
            return json.load(f)
            
    # 4. Proceso de Whisper si el JSON no existe
    print("⏳ Cargando modelo Whisper...")
    modelo = whisper.load_model("base") # Puedes usar "small" o "medium" si lo prefieres
    
    print("🎙️ Transcribiendo audio (esto puede tomar varios minutos)...")
    resultado = modelo.transcribe(ruta_video)
    
    # 5. Guardar archivo ordenado en su carpeta
    with open(ruta_json, "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=4, ensure_ascii=False)
        
    print(f"📁 JSON de transcripción guardado en: {ruta_json}")
    return resultado