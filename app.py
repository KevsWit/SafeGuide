import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import folium
from folium.plugins import MarkerCluster
from io import BytesIO
import base64

# Cargar datasets
homicidios_df = pd.read_csv("mdi_homicidiosintencionales_pm_2023_enero_septiembre.csv", sep=';', encoding='latin1')
turismo_df = pd.read_csv("atractivos_tur.csv", encoding='latin1')
peligros_df = pd.read_excel("SGR_EventosPeligrosos_2010_2022Diciembre.xlsx")

# Crear mapa de atractivos turísticos
m_turismo = folium.Map(location=[-1.8312, -78.1834], zoom_start=6)
cluster_turismo = MarkerCluster(name="Atractivos Turísticos").add_to(m_turismo)

# Marcadores turísticos
turismo_df = turismo_df.dropna(subset=['lat', 'lon'])
for _, row in turismo_df.iterrows():
    try:
        lat = float(row['lat'])
        lon = float(row['lon'])
        nombre = row['nombre']
        categoria = row['categoria']
        tipo = row['tipo']
        popup_text = f"<b>{nombre}</b><br>{categoria}<br>{tipo}"
        folium.Marker(location=[lat, lon], popup=popup_text, icon=folium.Icon(color='green')).add_to(cluster_turismo)
    except Exception as e:
        print(f"Error al agregar marcador turístico: {e}")
        continue

map_turismo_html = BytesIO()
m_turismo.save(map_turismo_html, close_file=False)
map_turismo_html.seek(0)
map_turismo_data = map_turismo_html.read()
map_turismo_src = "data:text/html;base64," + base64.b64encode(map_turismo_data).decode()

# Crear mapa de eventos peligrosos
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
        print(f"Error al agregar marcador de evento peligroso: {e}")
        continue

map_eventos_html = BytesIO()
m_eventos.save(map_eventos_html, close_file=False)
map_eventos_html.seek(0)
map_eventos_data = map_eventos_html.read()
map_eventos_src = "data:text/html;base64," + base64.b64encode(map_eventos_data).decode()

# Crear la app Dash
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard de Homicidios, Eventos y Turismo en Ecuador", style={'textAlign': 'center'}),

    html.Div([
        html.H2("Filtros de homicidios:"),
        dcc.Dropdown(
            id='provincia-dropdown',
            options=[{'label': p, 'value': p} for p in sorted(homicidios_df['Provincia'].unique())],
            value='PICHINCHA',
            placeholder="Selecciona una provincia"
        ),
        dcc.Dropdown(
            id='tipo-dropdown',
            options=[{'label': t, 'value': t} for t in sorted(homicidios_df['Tipo Muert.'].unique())],
            value='ASESINATO',
            placeholder="Selecciona tipo de muerte"
        ),
        dcc.Graph(id='grafico-homicidios')
    ], style={'width': '48%', 'display': 'inline-block', 'padding': '0 20px', 'verticalAlign': 'top'}),

    html.Div([
        html.H2("Filtros de eventos peligrosos (SGR):"),
        dcc.Dropdown(
            id='evento-dropdown',
            options=[{'label': e, 'value': e} for e in sorted(peligros_df['EVENTO'].dropna().unique())],
            value='INTOXICACIÓN',
            placeholder="Selecciona un tipo de evento"
        ),
        dcc.Graph(id='grafico-eventos')
    ], style={'width': '48%', 'display': 'inline-block', 'padding': '0 20px', 'verticalAlign': 'top'}),

    html.H2("Mapa de Atractivos Turísticos en Ecuador"),
    html.Iframe(src=map_turismo_src, width='100%', height='600'),

    html.H2("Mapa de Eventos Peligrosos en Ecuador (SGR)"),
    html.Iframe(src=map_eventos_src, width='100%', height='600')
])

@app.callback(
    Output('grafico-homicidios', 'figure'),
    Input('provincia-dropdown', 'value'),
    Input('tipo-dropdown', 'value')
)
def update_grafico(provincia, tipo):
    df_filtrado = homicidios_df[
        (homicidios_df['Provincia'] == provincia) &
        (homicidios_df['Tipo Muert.'].astype(str) == tipo)
    ]
    fig = px.histogram(df_filtrado, x='Arma', color='Sexo',
                       title=f"Homicidios por arma en {provincia} ({tipo})",
                       labels={'Arma': 'Tipo de arma'}, barmode='group')
    return fig

@app.callback(
    Output('grafico-eventos', 'figure'),
    Input('evento-dropdown', 'value')
)
def update_eventos(evento):
    df_evento = peligros_df[peligros_df['EVENTO'] == evento]
    fig = px.histogram(df_evento, x='PROVINCIA', color='CANTON',
                       title=f"Eventos registrados: {evento}",
                       labels={'PROVINCIA': 'Provincia', 'CANTON': 'Cantón'}, barmode='stack')
    return fig

if __name__ == '__main__':
    app.run()
