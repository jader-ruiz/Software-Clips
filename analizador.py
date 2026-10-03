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
        Eres un Director de Contenido viral experto. Analiza la siguiente transcripción JSON.
        
        OBLIGATORIO: Extrae TODOS los momentos de alto impacto (polémicos, graciosos, debates o gran valor educativo) que existan en el video. 
        - Si el video es largo, extrae la mayor cantidad posible.
        - Cada momento debe durar entre 15 y 60 segundos.
        
        Devuelve ÚNICAMENTE un arreglo JSON válido.
        [
            {{"titulo": "El_mejor_titulo_sin_espacios", "inicio": 10.5, "fin": 35.0}},
            {{"titulo": "Otro_titulo_impactante", "inicio": 45.0, "fin": 75.5}}
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