import pandas as pd
import os
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.express as px
import folium
from folium.plugins import MarkerCluster
from io import BytesIO
import base64
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

# Configurar entorno y cargar modelo Gemini
load_dotenv()
GEMINI_API_KEY = os.getenv("API_KEY_GEMINI")
if not GEMINI_API_KEY:
    raise ValueError("API_KEY_GEMINI no encontrado en .env")

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

# Template de prompt
template = PromptTemplate.from_template("""
Eres SafeGuide, un asistente virtual experto en turismo seguro en Ecuador.

Tu función principal es ayudar a los usuarios a planificar viajes informados, seguros y agradables dentro del país. Para ello, debes responder preguntas relacionadas con:
- Qué provincias, ciudades o cantones vale la pena visitar en Ecuador.
- Qué lugares se deben visitar con precaución por temas de delincuencia o eventos peligrosos.
- Qué zonas son más concurridas o recomendadas para cierto tipo de turismo.
- Dónde están los mejores atractivos turísticos del país.
- Cuáles son los sitios con más riesgos o alertas recientes.
- Qué lugares son ideales para ciertos perfiles (familias, mochileros, culturales, gastronómicos, etc.).

Si la pregunta del usuario está relacionada con estos temas, responde con información clara y útil.
Si NO está relacionada con turismo en Ecuador, responde:
"Estoy enfocado en la guía turística, para otra consulta puedes utilizar otra herramienta"

Usuario: "{input}"
""")

# Cargar datasets
homicidios_df = pd.read_csv("mdi_homicidiosintencionales_pm_2023_enero_septiembre.csv", sep=';', encoding='latin1')
turismo_df = pd.read_csv("atractivos_tur.csv", encoding='latin1')
peligros_df = pd.read_excel("SGR_EventosPeligrosos_2010_2022Diciembre.xlsx")

# Crear mapas
m_turismo = folium.Map(location=[-1.8312, -78.1834], zoom_start=6)
cluster_turismo = MarkerCluster(name="Atractivos Turísticos").add_to(m_turismo)

for _, row in turismo_df.dropna(subset=['lat', 'lon']).iterrows():
    try:
        lat = float(row['lat'])
        lon = float(row['lon'])
        nombre = row['nombre']
        categoria = row['categoria']
        tipo = row['tipo']
        popup_text = f"<b>{nombre}</b><br>{categoria}<br>{tipo}"
        folium.Marker(location=[lat, lon], popup=popup_text, icon=folium.Icon(color='green')).add_to(cluster_turismo)
    except Exception as e:
        print(f"Error marcador turístico: {e}")

map_html_turismo = BytesIO()
m_turismo.save(map_html_turismo, close_file=False)
map_html_turismo.seek(0)
map_turismo_src = "data:text/html;base64," + base64.b64encode(map_html_turismo.read()).decode()

m_eventos = folium.Map(location=[-1.8312, -78.1834], zoom_start=6)
cluster_eventos = MarkerCluster(name="Eventos Peligrosos").add_to(m_eventos)

eventos_filtrados = peligros_df[
    peligros_df['EVENTO'].astype(str).str.strip().str.upper().isin([
        'INTOXICACIÓN', 'PERTURBACIÓN EN EVENTOS MASIVOS'
    ])
].dropna(subset=['LATITUD', 'LONGITUD'])

for _, row in eventos_filtrados.iterrows():
    try:
        lat = float(row['LATITUD'])
        lon = float(row['LONGITUD'])
        evento = row['EVENTO'].title()
        descripcion = row.get('DESCRIPCIÓN GENERAL DEL EVENTO', '')
        provincia = row.get('PROVINCIA', '')
        canton = row.get('CANTON', '')
        popup_text = f"<b>{evento}</b><br>{descripcion}<br><i>{provincia} - {canton}</i>"
        folium.Marker(location=[lat, lon], popup=popup_text, icon=folium.Icon(color='red')).add_to(cluster_eventos)
    except Exception as e:
        print(f"Error marcador evento: {e}")

map_html_eventos = BytesIO()
m_eventos.save(map_html_eventos, close_file=False)
map_html_eventos.seek(0)
map_eventos_src = "data:text/html;base64," + base64.b64encode(map_html_eventos.read()).decode()

# App Dash
app = dash.Dash(__name__)
app.title = "SafeGuide"

app.layout = html.Div([
    html.H1("SafeGuide - Turismo Seguro en Ecuador", style={'textAlign': 'center'}),

    html.Div([
        html.H2("Filtros de homicidios:"),
        dcc.Dropdown(id='provincia-dropdown', options=[{'label': p, 'value': p} for p in sorted(homicidios_df['Provincia'].unique())], value='PICHINCHA'),
        dcc.Dropdown(id='tipo-dropdown', options=[{'label': t, 'value': t} for t in sorted(homicidios_df['Tipo Muert.'].unique())], value='ASESINATO'),
        dcc.Graph(id='grafico-homicidios')
    ], style={'width': '100%', 'marginBottom': '30px'}),

    html.Div([
        html.H2("Eventos peligrosos (SGR):"),
        dcc.Dropdown(id='evento-dropdown', options=[{'label': e, 'value': e} for e in sorted(peligros_df['EVENTO'].dropna().unique())], value='INTOXICACIÓN'),
        dcc.Graph(id='grafico-eventos')
    ], style={'width': '100%', 'marginBottom': '30px'}),

    html.H2("Mapa de Atractivos Turísticos"),
    html.Iframe(src=map_turismo_src, width='100%', height='600'),

    html.H2("Mapa de Eventos Peligrosos (SGR)"),
    html.Iframe(src=map_eventos_src, width='100%', height='600'),

    html.H2("Asistente Virtual - SafeGuide"),
    dcc.Input(id='chat-input', type='text', placeholder='Haz tu pregunta sobre turismo en Ecuador...', style={'width': '80%'}),
    html.Button('Enviar', id='chat-submit', n_clicks=0),
    html.Div(id='chat-output', style={'whiteSpace': 'pre-line', 'marginTop': '10px', 'padding': '10px', 'border': '1px solid #ccc'})
])

@app.callback(
    Output('grafico-homicidios', 'figure'),
    Input('provincia-dropdown', 'value'),
    Input('tipo-dropdown', 'value')
)
def update_grafico(provincia, tipo):
    df_filtrado = homicidios_df[(homicidios_df['Provincia'] == provincia) & (homicidios_df['Tipo Muert.'].astype(str) == tipo)]
    fig = px.histogram(df_filtrado, x='Arma', color='Sexo', title=f"Homicidios por arma en {provincia} ({tipo})", labels={'Arma': 'Tipo de arma'}, barmode='group')
    return fig

@app.callback(
    Output('grafico-eventos', 'figure'),
    Input('evento-dropdown', 'value')
)
def update_eventos(evento):
    df_evento = peligros_df[peligros_df['EVENTO'] == evento]
    fig = px.histogram(df_evento, x='PROVINCIA', color='CANTON', title=f"Eventos registrados: {evento}", labels={'PROVINCIA': 'Provincia', 'CANTON': 'Cantón'}, barmode='stack')
    return fig

@app.callback(
    Output('chat-output', 'children'),
    Input('chat-submit', 'n_clicks'),
    State('chat-input', 'value')
)
def responder_chat(n_clicks, pregunta):
    if not pregunta:
        return "Por favor, ingresa una pregunta."
    prompt_text = template.invoke({"input": pregunta})
    try:
        respuesta = llm.invoke(prompt_text).content
        return f"Tú: {pregunta}\nSafeGuide: {respuesta}"
    except Exception as e:
        return f"Error al procesar la respuesta: {e}"

if __name__ == '__main__':
    app.run()
