import ollama
import json
import os

class AnalizadorClips:
    def __init__(self, modelo="llama3"):
        self.modelo = modelo
        print(f"Analizador inicializado conectado a Ollama usando el modelo: {self.modelo}")

    def analizar_transcripcion(self, ruta_json_transcripcion):
        """
        Lee la transcripción y le pide al LLM que identifique los momentos más interesantes.
        """
        if not os.path.exists(ruta_json_transcripcion):
            print(f"Error: No se encontró {ruta_json_transcripcion}.")
            return None

        # Leemos el archivo JSON que creó el módulo anterior
        with open(ruta_json_transcripcion, 'r', encoding='utf-8') as archivo:
            datos_transcripcion = archivo.read()

        print("Analizando el contenido para encontrar clips... (esto puede tomar un minuto)")

        # Este es el "Prompt". Es crucial darle instrucciones claras a la IA.
        prompt = f"""
        Eres un experto productor de video viral. Te daré una transcripción en formato JSON. 
        Cada segmento tiene un 'inicio', un 'fin' y un 'texto'.
        
        Tu tarea es identificar los 3 a 5 momentos más interesantes, polémicos, graciosos o de mayor valor educativo de esta transcripción. Cada momento debe durar entre 15 y 60 segundos.
        
        Devuélveme ÚNICAMENTE un arreglo JSON válido con múltiples objetos. Usa esta estructura estricta, sin texto extra:
        [
            {{
                "titulo": "Un título atractivo para el clip 1",
                "inicio": tiempo_inicio_1,
                "fin": tiempo_fin_1
            }},
            {{
                "titulo": "Un título atractivo para el clip 2",
                "inicio": tiempo_inicio_2,
                "fin": tiempo_fin_2
            }}
        ]
        
        Aquí está la transcripción:
        {datos_transcripcion}
        """

        try:
            # Enviamos el prompt al modelo que corre localmente en Ollama
            respuesta = ollama.generate(model=self.modelo, prompt=prompt)
            texto_respuesta = respuesta['response'].strip()
            
            # Limpiamos la respuesta en caso de que la IA agregue comillas invertidas de código
            if texto_respuesta.startswith("```json"):
                texto_respuesta = texto_respuesta[7:]
            if texto_respuesta.endswith("```"):
                texto_respuesta = texto_respuesta[:-3]
                
            clips_sugeridos = json.loads(texto_respuesta.strip())
            
            # Guardamos las instrucciones de corte para el siguiente paso
            with open("cortes_sugeridos.json", 'w', encoding='utf-8') as f:
                json.dump(clips_sugeridos, f, indent=4, ensure_ascii=False)
                
            print("¡Análisis completado! Se ha creado 'cortes_sugeridos.json'")
            return clips_sugeridos

        except json.JSONDecodeError:
            print("Error: La IA no devolvió un JSON válido.")
            print("Respuesta cruda de la IA:")
            print(texto_respuesta)
            return None
        except Exception as e:
            print(f"Error al conectar con Ollama: {e}")
            print("¿Te aseguraste de instalar Ollama y descargar el modelo (ollama run llama3)?")
            return None

# Bloque de ejecución principal
if __name__ == "__main__":
    mi_analizador = AnalizadorClips()
    mi_analizador.analizar_transcripcion("transcripcion.json")