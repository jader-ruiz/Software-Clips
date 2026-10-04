import google.generativeai as genai
import json

def analizar_con_gemini(datos_transcripcion, api_key):
    print("🧠 Conectando con Gemini para analizar la narrativa...")
    
    # Configuramos la API con la clave proporcionada en la terminal
    genai.configure(api_key=api_key)
    
    modelo = genai.GenerativeModel('gemini-1.5-flash')
    
    if isinstance(datos_transcripcion, dict) and "text" in datos_transcripcion:
        texto_a_analizar = datos_transcripcion["text"]
    else:
        texto_a_analizar = str(datos_transcripcion)
        
    prompt = f"""
    Eres un Productor de TikTok experto y Director de Contenido para streamers de la categoría "Just Chatting" (Charlas/IRL). 
    Tu único objetivo es analizar la siguiente transcripción y extraer fragmentos que tengan un potencial viral masivo.

    BUSCA ESPECÍFICAMENTE ESTOS 4 PATRONES (EL ORO DEL IRL):
    1. El "Storytime" (Anécdotas): Historias personales locas, situaciones incómodas o bizarras.
    2. La Polémica (Hot Takes): Opiniones fuertes, controversiales o muy sinceras.
    3. El Remate (Comedia): Respuestas rápidas, sarcásticas o inesperadas.
    4. El "Real Talk" (Reflexión): Un consejo de vida duro o momento de vulnerabilidad.

    REGLAS DE ORO PARA EL CORTE (RETENCIÓN):
    - EL GANCHO (HOOK): El clip DEBE empezar en el milisegundo exacto de la acción. Elimina toda la basura introductoria.
    - AUTOSUFICIENCIA: El clip debe tener sentido absoluto sin contexto previo.
    - DURACIÓN: Entre 20 y 60 segundos. Ni un segundo de relleno al final.
    - EXHAUSTIVIDAD: Extrae la cantidad máxima de clips posibles.

    Devuelve ÚNICAMENTE un arreglo JSON válido. No incluyas texto antes ni después. Estructura estricta:
    [
        {{"titulo": "Storytime_Loco", "inicio": 12.5, "fin": 45.0}},
        {{"titulo": "Opinion_Fuerte_Dinero", "inicio": 120.0, "fin": 160.5}}
    ]
    
    Transcripción a analizar:
    {texto_a_analizar}
    """

    try:
        respuesta = modelo.generate_content(prompt)
        texto_respuesta = respuesta.text
        
        texto_limpio = texto_respuesta.replace("```json", "").replace("```", "").strip()
        momentos_virales = json.loads(texto_limpio)
        print(f"✅ Gemini encontró {len(momentos_virales)} momentos con potencial viral.")
        
        return momentos_virales
        
    except json.JSONDecodeError:
        print("❌ Error: La IA no devolvió un formato JSON válido.")
        print("Respuesta cruda de la IA para depurar:", texto_respuesta)
        return []
    except Exception as e:
        print(f"❌ Error al procesar con la API de Gemini: {e}")
        return []