import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import folium
from io import BytesIO
import base64

# Cargar datasets
homicidios_df = pd.read_csv("mdi_homicidiosintencionales_pm_2023_enero_septiembre.csv", sep=';', encoding='latin1')
turismo_df = pd.read_csv("atractivos_tur.csv", encoding='latin1')  # usa coma por defecto


# Crear mapa Folium
m = folium.Map(location=[-1.8312, -78.1834], zoom_start=6)  # Centro de Ecuador

for _, row in turismo_df.iterrows():
    try:
        lat = float(row['lat'])
        lon = float(row['lon'])
        nombre = row['nombre']
        categoria = row['categoria']
        tipo = row['tipo']
        popup_text = f"<b>{nombre}</b><br>{categoria}<br>{tipo}"
        folium.Marker(location=[lat, lon], popup=popup_text).add_to(m)
    except:
        continue  # Saltar si lat/lon están mal

# Guardar el mapa como HTML en memoria
map_html = BytesIO()
m.save(map_html, close_file=False)
map_html.seek(0)
map_src = "data:text/html;base64," + base64.b64encode(map_html.read()).decode()

# Crear la app Dash
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard de Homicidios y Turismo en Ecuador", style={'textAlign': 'center'}),

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
    ], style={'width': '40%', 'display': 'inline-block', 'padding': '0 20px'}),

    html.Div([
        dcc.Graph(id='grafico-homicidios')
    ]),

    html.H2("Mapa de Atractivos Turísticos en Ecuador"),
    html.Iframe(src=map_src, width='100%', height='600')
])

@app.callback(
    Output('grafico-homicidios', 'figure'),
    Input('provincia-dropdown', 'value'),
    Input('tipo-dropdown', 'value')
)
def update_grafico(provincia, tipo):
    df_filtrado = homicidios_df[
        (homicidios_df['Provincia'] == provincia) &
        (homicidios_df['Tipo Muert.'] == tipo)
    ]

    fig = px.histogram(df_filtrado, x='Arma', color='Sexo',
                       title=f"Homicidios por arma en {provincia} ({tipo})",
                       labels={'Arma': 'Tipo de arma'}, barmode='group')
    return fig

if __name__ == '__main__':
    app.run()
