from google import genai
from google.genai import types
import json
import os

class AnalizadorClips:
    def __init__(self, api_key):
        # Inicializamos el nuevo cliente oficial de Google
        self.client = genai.Client(api_key=api_key)
        print("Analizador inicializado con el nuevo SDK de Gemini en la nube.")

    def analizar_transcripcion(self, ruta_json_transcripcion):
        if not os.path.exists(ruta_json_transcripcion):
            print(f"Error: No se encontró {ruta_json_transcripcion}.")
            return None

        with open(ruta_json_transcripcion, 'r', encoding='utf-8') as archivo:
            datos_transcripcion = archivo.read()

        print("Enviando transcripción a la nube para análisis... (tomará unos segundos)")

        prompt = f"""
        Eres un Productor de TikTok experto y Director de Contenido para streamers de la categoría "Just Chatting" (Charlas/IRL). 
        Tu único objetivo es analizar la siguiente transcripción JSON y extraer fragmentos que tengan un potencial viral masivo.

        BUSCA ESPECÍFICAMENTE ESTOS 4 PATRONES (EL ORO DEL IRL):
        1. El "Storytime" (Anécdotas): Historias personales locas, situaciones incómodas o bizarras que el streamer le cuenta al chat.
        2. La Polémica (Hot Takes): El streamer dando una opinión fuerte, controversial o muy sincera sobre relaciones, dinero, sociedad u otros creadores.
        3. El Remate (Comedia): Una respuesta rápida, sarcástica o inesperada a un comentario del chat que genere risa inmediata.
        4. El "Real Talk" (Reflexión): Un consejo de vida duro, motivación genuina o un momento de vulnerabilidad.

        REGLAS DE ORO PARA EL CORTE (RETENCIÓN):
        - EL GANCHO (HOOK): El clip DEBE empezar en el milisegundo exacto de la acción. Elimina toda la basura introductoria (ej. "Eh, bueno chat, les iba a contar que...", "A ver..."). El primer segundo del clip debe ser una frase que obligue al espectador a quedarse (ej. "La peor cita de mi vida fue...").
        - AUTOSUFICIENCIA: El clip debe tener sentido absoluto para alguien que jamás en su vida ha visto a este streamer. Si le falta contexto, no sirve.
        - DURACIÓN: Entre 20 y 60 segundos. Ni un segundo de relleno al final. Corta justo después del "punchline" o la conclusión.
        - EXHAUSTIVIDAD: Extrae la cantidad máxima de clips posibles que cumplan esta calidad premium.

        Devuelve ÚNICAMENTE un arreglo JSON válido. No incluyas texto antes ni después. Estructura estricta:
        [
            {{"titulo": "Storytime_Loco", "inicio": 12.5, "fin": 45.0}},
            {{"titulo": "Opinion_Fuerte_Dinero", "inicio": 120.0, "fin": 160.5}}
        ]
        
        Transcripción a analizar:
        {datos_transcripcion}
        """

        try:
            # Actualizado a la versión 3.8 que exige el servidor
            respuesta = self.client.models.generate_content(
                model='gemini-3.8-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            
            clips_sugeridos = json.loads(respuesta.text)
            print(f"¡Éxito! La IA de la nube encontró {len(clips_sugeridos)} clips potenciales.")
            
            return clips_sugeridos

        except Exception as e:
            print(f"Error al conectar con la API: {e}")
            return None