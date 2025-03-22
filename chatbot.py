import pandas as pd
import os
import re
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

# ========== CONFIGURACIÓN ==========
load_dotenv()
GEMINI_API_KEY = os.getenv("API_KEY_GEMINI")
if not GEMINI_API_KEY:
    raise ValueError("❌ ERROR: La clave API de Gemini no se ha cargado correctamente. Asegúrate de tener un archivo .env con API_KEY_GEMINI=tu_clave")

# ========== MODELO DE GEMINI ==========
class LLModel():
    def __init__(self):
        self.llm = self.__configurateModel()
    def __configurateModel(self):
        return ChatGoogleGenerativeAI(
            model="gemini-1.5-flash-latest",
            google_api_key=GEMINI_API_KEY,
            temperature=0.4
        )

llm = LLModel().llm

# ========== CARGAR DATASETS ==========
# homicidios_df = pd.read_csv("mdi_homicidiosintencionales_pm_2023_enero_septiembre.csv", sep=';', encoding='latin1')
# turismo_df = pd.read_csv("atractivos_tur.csv", encoding='latin1')
# peligros_df = pd.read_excel("SGR_EventosPeligrosos_2010_2022Diciembre.xlsx")

# ========== PLANTILLA ==========
template = """
Eres SafeGuide, un asistente virtual experto en turismo seguro en Ecuador.

Tu función principal es ayudar a los usuarios a planificar viajes informados, seguros y agradables dentro del país. Para ello, debes responder preguntas relacionadas con:

- Qué provincias, ciudades o cantones vale la pena visitar en Ecuador.
- Qué lugares se deben visitar con precaución por temas de delincuencia o eventos peligrosos.
- Qué zonas son más concurridas o recomendadas para cierto tipo de turismo.
- Dónde están los mejores atractivos turísticos del país.
- Cuáles son los sitios con más riesgos o alertas recientes.
- Qué lugares son ideales para ciertos perfiles (familias, mochileros, culturales, gastronómicos, etc.).

Si la pregunta del usuario está relacionada con cualquiera de estos temas, responde con información clara y útil para planificar un viaje por Ecuador.

⚠️ Si la pregunta NO está relacionada en absoluto con turismo en Ecuador (por ejemplo, si es sobre otro país, vuelos internacionales, clima global, inteligencia artificial, recetas o temas generales), responde únicamente lo siguiente en el mismo idioma del usuario:
"Estoy enfocado en la guía turística, para otra consulta puedes utilizar otra herramienta"

Usuario: "{input}"

Responde de forma clara, amigable y en el idioma detectado del usuario.
"""

prompt = PromptTemplate.from_template(template)

# ========== FUNCIÓN DEL CHATBOT ==========
def interactuar_con_safeguide():
    chat_history = []
    print("\n🧭 SafeGuide - Asistente de Turismo Seguro en Ecuador")
    print("Consulta sobre provincias, ciudades o lugares para visitar en Ecuador.\nEscribe 'salir', 'adios', 'exit', 'quit' para finalizar.\n")

    while True:
        user_input = input("Tú: ")
        if user_input.lower() in ['salir', 'adios', 'exit', 'quit']:
            print("\nSafeGuide: Gracias por usar SafeGuide. ¡Buen viaje! ✈️")
            break

        full_prompt = prompt.invoke({"input": user_input})

        try:
            response = llm.invoke(full_prompt).content
            print(f"SafeGuide: {response}\n")
            chat_history.append({"input": user_input, "response": response})
        except Exception as e:
            print(f"❌ Error al procesar la respuesta: {e}")

# Ejecutar el chatbot
if __name__ == '__main__':
    interactuar_con_safeguide()
