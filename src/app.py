import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc




# ID del archivo en Google Drive  
file_id = "146SA4xoONY7Tbrte8s-r8t8jEykNf5Cg"  
csv_url = f"https://drive.google.com/uc?id={file_id}" 

# Leer el CSV en bloques de 10,000 filas  
df_chunks = pd.read_csv(csv_url, chunksize=10000)  

# Unir los bloques en un solo DataFrame  
df_raw = pd.concat(df_chunks, ignore_index=True) 
dffinal = df_raw.copy()


# Variables
fuente = "https://catalog.data.gov/"
explicacion = "This dataset shows the Battery Electric Vehicles (BEVs) and Plug-in Hybrid Electric Vehicles (PHEVs) that are currently registered through Washington State Department of Licensing (DOL)."
list_e_utility=dffinal["Electric Utility"].unique()
cantidad_e_utility=len(dffinal["Electric Utility"].unique())
list_estados=dffinal["State"].unique()
list_make = dffinal["Make"].unique()
cantidad_estados=len(dffinal["State"].unique())
total_electricos_WA = dffinal.shape[0]
model_year_min = dffinal["Model Year"].min()
model_year_max = dffinal["Model Year"].max()
counties = dffinal["County"].unique()
markdown_inicio = dcc.Markdown(
    """   
        Bienvenido a este Dashboard interactivo, donde podrás explorar el estado actual y las tendencias  
        de adopción de vehículos eléctricos (EVs) en Washington (WA). A través de visualizaciones dinámicas,  
        descubrirás cómo han evolucionado las ventas de EVs, cuáles son las marcas y modelos más populares,  
        y cómo se distribuyen en el estado.
        
        📊 **¿Qué puedes encontrar aquí?**  
        🔹 Tendencias en la adopción de EVs 📈: Observa la evolución en el tiempo y descubre los picos en  
        la compra de vehículos eléctricos.  
        🔹 Distribución geográfica 🗺️: Analiza qué condados tienen mayor cantidad de EVs registrados.  
        🔹 Empresas proveedoras de energía ⚡: Descubre qué compañías suministran electricidad a los EVs y  
        cómo se divide el mercado.  
        🔹 Análisis de marcas y modelos 🚘: Conoce qué fabricantes dominan el mercado y cuáles son los  
        modelos más populares.  
        
        💡 **Funcionalidades destacadas**  
        ✔️ Gráficos interactivos: Filtra y explora la información con un solo clic.  
        ✔️ Mapas dinámicos: Visualiza la distribución geográfica de EVs en el estado.  
        ✔️ Comparaciones en el tiempo: Examina cómo ha cambiado la adopción de EVs por marca y ubicación.  

        📌 **Sobre los datos**  
        Los datos utilizados en este Dashboard provienen del _Departamento de Licencias del Estado de Washington_,  
        reflejando el parque automotor eléctrico en el estado. Este análisis es estático, lo que significa que  
        los datos no se actualizan automáticamente.

        🚀 **Explora y comparte**                
        🔍 ¡Explora los datos y obtén insights clave sobre el crecimiento de la movilidad eléctrica!
    """
, style={"flex":"2", "padding": "0px 0px 0px 30px", "textAlign": "justify" })

# -----Insights---
analisis_1= "Analizando la tendencia a lo largo del tiempo, observamos que el mercado de vehículos eléctricos en Washington alcanzó su punto máximo histórico en 2023, impulsado por un crecimiento constante desde 2020. Este auge sugiere que los programas de incentivos fiscales y políticas de apoyo jugaron un papel clave en el aumento de la adopción de EVs."
analisis_2= "El mapa de Washington revela una alta concentración de vehículos eléctricos en los condados donde se encuentra Seattle y Tacoma, donde se pueden encontrar, en su mayoría, modelos fabricados a partir de 2020."
analisis_3 = "El análisis de los registros de vehículos eléctricos en Washington reveló que aproximadamente el 0.21 pct de ellos se encuentran fuera del estado. Gran parte de estos corresponden a vehículos Tesla y otras marcas que, aunque operan en otros estados, fueron registrados en Washington debido a que la empresa propietaria tiene su domicilio fiscal allí. Esto sugiere que algunas compañías aprovecharon los incentivos fiscales del estado para adquirir EVs, independientemente de su ubicación real de uso."
analisis_4 = '''
El gráfico de barras revela un dato significativo sobre la adopción de vehículos eléctricos en el condado de King. Este condado, que incluye la ciudad de Seattle, concentra un volumen de registros de EVs equivalente al de los siguientes nueve condados combinados.
Este comportamiento puede estar influenciado por varios factores. En primer lugar, King County es el área metropolitana más grande del estado de Washington, con una alta densidad poblacional y un mayor poder adquisitivo, lo que facilita la adopción de nuevas tecnologías como los vehículos eléctricos. Además, la infraestructura de carga en la región está más desarrollada en comparación con otros condados, lo que reduce la barrera para la transición a EVs.
Otro factor clave es la presencia de incentivos locales y estatales dirigidos a la movilidad sostenible, junto con una mayor conciencia ambiental entre los residentes de Seattle y sus alrededores. También es posible que la concentración de empresas tecnológicas y la disponibilidad de opciones de leasing corporativo impulsen la adquisición de estos vehículos.
En contraste, los otros condados en el ranking presentan una distribución más fragmentada, lo que sugiere que la adopción de EVs fuera de King County avanza a un ritmo más lento, posiblemente debido a limitaciones de infraestructura, costos iniciales o menor acceso a incentivos. 
'''
analisis_5 = '''
El gráfico de dona muestra que el Tesla Model Y domina el mercado de vehículos eléctricos con un 35 pct de participación, seguido por el Tesla Model 3 con 25.7%. Esto indica que Tesla tiene un fuerte liderazgo en la adopción de EVs, ya que solo estos dos modelos representan más del 60 pct del total registrado.
Por otro lado, el Nissan Leaf, con 9.99%, es el modelo no Tesla más popular, lo que sugiere que sigue siendo una opción relevante para quienes buscan un EV más asequible. Modelos como el Bolt EV (5.18%) y el Model S (5.68%) tienen una presencia menor, lo que puede estar relacionado con su posicionamiento en el mercado o la oferta disponible.
En general, este análisis sugiere que los consumidores en este mercado priorizan los modelos de Tesla, probablemente debido a su infraestructura de carga, rendimiento y percepción de marca, aunque hay una diversidad de opciones en el segmento.
'''
analisis_6 = '''
El gráfico muestra que Puget Sound Energy y City of Tacoma son, por un margen significativo, las empresas eléctricas más utilizadas por los propietarios de EVs en Washington. Puget Sound Energy lidera con más de 84,000 registros, lo que indica su dominio en la provisión de electricidad para vehículos eléctricos en el estado.
La diferencia con el resto de las empresas es notable, ya que la segunda y tercera compañías en el ranking tienen alrededor de 40,000 a 45,000 registros, lo que sugiere que la infraestructura de carga y distribución de estas dos empresas es clave para la adopción de EVs en la región.
Este análisis destaca la importancia de estas compañías en la transición hacia la movilidad eléctrica y su posible papel en futuros incentivos o mejoras en la red de carga.
'''    

# Graficos
# -----------------------------------------------------------------------
# ¿Cuales son las marcas de vehiculos electricos más populares en WA?
# recuento de vehiculos por marca y modelo
marcas = dffinal.groupby(["Make"]).size().reset_index(name="Count").sort_values(by="Count", ascending=False)
marcas = marcas.head(10)

fig_top_10_marcas = px.bar(marcas,
            x="Make",
            y="Count", 
            color="Make",
            color_discrete_sequence=px.colors.qualitative.Dark2_r,
            title="Marcas de Evs más populares Registradas en WA<br>(Top 10)", 
            barmode="stack"
            )
fig_top_10_marcas.update_layout(paper_bgcolor="white", 
                  plot_bgcolor="White", 
                  yaxis={"gridcolor": "lightgrey", "gridwidth": 0.5})

# Modelos mas Populares por la marca
marcas_modelos_treemap = dffinal.groupby(["Make", "Model", "Electric Vehicle Type"]).size().reset_index(name="Count").sort_values(by="Count", ascending=False)
marcas_modelos_treemap = marcas_modelos_treemap.head(20)
fig_modelos_por_marcas = px.treemap(marcas_modelos_treemap, 
                path=["Make", "Model"], 
                values="Count", 
                color_discrete_sequence=px.colors.qualitative.Dark2_r,
                height=700,
                width=1200,
                title="Distribución de Modelos por Marca más Populares en WA")

# Modelos de Vehiculos mas Populares
modelos = dffinal.groupby(["Make","Model"]).size().reset_index(name="count").sort_values(by="count", ascending=False)
modelos = modelos.head(10)

fig_pct_mercado_modelos = px.pie(modelos, 
            names="Model", 
            values="count",
            color_discrete_sequence=px.colors.qualitative.Dark2,
            #color="Make", 
             title="Distribución de Marcas Más Populares", hole=0.6)  # Donut Chart

fig_pct_mercado_modelos.update_layout(paper_bgcolor="white", 
                  plot_bgcolor="White", 
)

# Evolucion de los vehiculos por año de fabricación
df_time_line = dffinal.copy()
df_time_line["Model Year"] = pd.to_datetime(df_time_line["Model Year"], format='%Y')
df_time_line["Model Year"] = df_time_line["Model Year"].dt.year
evo_tiempo = df_time_line.groupby(["Model Year"]).size().reset_index(name="Count").sort_values(by="Model Year", ascending=False)

fig_time_line_evs = px.line(evo_tiempo,
            x="Model Year",
            y="Count", 
            title="Evolución de los EVs por Año en WA", 
            )
fig_time_line_evs.update_layout(paper_bgcolor="white", 
                  plot_bgcolor="White",
                  yaxis={"gridcolor": "lightgrey", "gridwidth": 0.5})
fig_time_line_evs.update_traces(line=dict(color="green"))

# Cauntos EVs estan registrados en Washington (WA)
# Extraer la longitud y latitud de las ciudades de la columna "Vehicle Location"
dffinal[['lon', 'lat']] = dffinal['Vehicle Location'].str.extract(r'POINT \(([-\d.]+) ([-\d.]+)\)')
dffinal[['lon', 'lat']] = dffinal[['lon', 'lat']].astype(float)  # Convertir a valores numéricos

# Mapa de Evs registrados por ciudad
fig_mapa_cluster = px.scatter_map(dffinal, 
                    lat="lat", 
                    lon="lon", 
                    title="Ubicación de los EVs registrados en WA al rededor de EEUU", 
                    map_style="carto-darkmatter",
                    hover_name="City",
                    zoom=2)

fig_mapa_cluster.update_traces(cluster=dict(enabled=True))

fig_mapa_cluster.update_layout(
    margin={"r":0, "t":40, "l":0, "b":0}
)

#  scatter_map de WA EVs
fig_scatter_map = px.scatter_map(dffinal, 
                        lat="lat", 
                        lon="lon", 
                        color="Model Year", 
                        color_continuous_scale="Plasma",
                        title="Ubicación de los EVs registrados en WA", 
                        hover_name="Model",
                        custom_data="Model",
                        center={"lat": 47.62912311820097, "lon": -121.04921709398583},
                        map_style="carto-darkmatter",
                        zoom=5)

fig_scatter_map.update_traces(marker=dict(#color="green", 
                        opacity=0.5),
                 hovertemplate=None)

fig_scatter_map.update_layout(
    margin={"r":0, "t":40, "l":0, "b":0}
)

# Como se distribuyen los Evs segun el county
count_couties = dffinal.groupby(["County"]).size().reset_index(name="Count").sort_values(by="Count", ascending=False)
count_couties = count_couties.head(10)

fig_counties = px.bar(count_couties,
            y="County",
            x="Count", 
            color="County",
            color_discrete_sequence=px.colors.qualitative.Dark2_r,
            title="Top 10 Counties más Populares en EVs", 
            barmode="stack"
            )

fig_counties.update_layout(paper_bgcolor="white", 
                  plot_bgcolor="White", 
                  xaxis={"gridcolor": "lightgrey", "gridwidth": 0.5})

# Empresas de suministro de energia en WA
cuota_mercado= dffinal.groupby(["Electric Utility"]).size().reset_index(name="Count").sort_values(by="Count", ascending=False).head(10)

fig_utilities = px.bar(cuota_mercado, 
                 x="Electric Utility", 
                 y="Count",
                 color="Electric Utility",  # Colores por empresa
                 color_discrete_sequence=px.colors.qualitative.Dark2_r,
                 title="Top 10  Empresas de Energía Electrica más Populares para EVs en WA<br>(Pasar el mouse sobre la barra para ver detalle)",
                )

fig_utilities.update_layout(showlegend=False,
                xaxis=dict(showticklabels=False),
                xaxis_title="Electric Utility Company", 
                yaxis_title="Count",
                paper_bgcolor="white", plot_bgcolor="White", 
                yaxis={"gridcolor": "lightgrey", "gridwidth": 0.5})



#  -------Inicializar la aplicación con el tema de Bootstrap----------
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY, "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"], suppress_callback_exceptions=True)
#server = app.server
app.title = "Washintong EVs Dashboard"

# Sidebar con navegación
sidebar = dbc.Col([html.Br(),
    html.H2("Washintong EVs Dashboard", className="text-center text-light"),
    html.Hr(),
    dbc.Nav([
        dbc.NavLink([html.I(className="fa fa-home me-2"),"Inicio"], href="/", active="exact"),
        dbc.NavLink([html.I(className="fa fa-chart-line me-2"),"Distribución y Tendencias"], href="/tendencias", active="exact"),
        dbc.NavLink([html.I(className="fa fa-map-marker-alt me-2"),"Ubicación y Geografía"], href="/ubicacion", active="exact"),
        dbc.NavLink([html.I(className="fa fa-car me-2"),"Marcas y Modelos"], href="/caracteristicas", active="exact"),
        html.Span(children=[html.P("Elaborado por: "),
                                html.B("Alejandro Maldonado "),html.Br(),
                                html.I("Analista de Datos")], style={"padding": "510px 0px 0px 0px", "font-size": "12px"}),
    ], vertical=True, pills=True, className="bg-dark text-light p-2"),
], width=2, className="bg-dark text-light vh-100 position-fixed")

# Contenido principal dinámico
content = dbc.Col([
    dcc.Location(id="url", refresh=False),
    html.Div(id="tab-content")
], width=10, style={"margin-left": "20%", "padding": "20px 0px 0px 0px"})  # Ajustar margen para que no se superponga con el sidebar

# Dropdown con la lista de marcas
dropdown = dcc.Dropdown(
            id="make_dd",
            options=[{"label": make, "value": make} for make in list_make],
            placeholder="Fabricante",
            className="dropdown"            
)


# ----------Layout del dashboard---------------
app.layout = dbc.Container([
    dbc.Row([
        html.Div(sidebar, className="sidebar"),
        html.Div(content, className="graph-container")
    ]),
], fluid=True)

# Función para renderizar el contenido de cada página
def render_tab_content(pathname):
    if pathname == "/" or pathname == "/inicio":
        return html.Div([html.H1("Vehículos Eléctricos en Washington (EEUU)", className="text-center", style={"font-size":"60px"}), 
                         html.Br(),
                         html.Br(),
                         html.H3("Resumen:  ", className="text-center"),
                         html.Br(),
                         html.Div(children=[html.Img(src="https://i.postimg.cc/90SXfSY2/evs-cars.png",
                         style={"width": "20%", "flex": "1", "margin": "auto", "border-radius": "10px"}),
                         markdown_inicio], style={"display": "flex"})
                         ])
    elif pathname == "/tendencias":
        return dbc.Container([html.H6("Selecciona un Fabricante: "),dropdown,
            dbc.Row([dbc.Col(dcc.Graph(id="grafico_linea_tiempo", figure=fig_time_line_evs, className="dash-graph",style={"padding":"10px 0px 0px 0px"}), width=12),
            ]),
            dbc.Row([
                dbc.Col(
                    dbc.Accordion(
                        dbc.AccordionItem(analisis_1,
                                          title="Análisis: Evolución de los EVs por Años en WA", style={"textAlign": "justify"})
                    , start_collapsed=True)
                )
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id="grafico_scatter_map", figure=fig_scatter_map,className="dash-graph", style={"padding": "30px 0px 30px 0px"}), width=12),
            ]),
            html.Br(),
            html.Br(),
            html.Br(),
            dbc.Row([
                dbc.Col(
                    dbc.Accordion(
                        dbc.AccordionItem(analisis_2, title="Análisis: Ubicación de los EVs registrados en WA", style={"padding": "0px 0px 30px 0px","textAlign": "justify"} )
                    , start_collapsed=True)
                )
            ])
        ])
    elif pathname == "/ubicacion":
        return dbc.Container([
            dbc.Row([
                dbc.Col(dcc.Graph(id="mapa_cluster", figure=fig_mapa_cluster,className="dash-graph", style={"padding":"40px 0px 0px 0px"}), width=6),
                dbc.Col(dcc.Graph(id="counties_bar", figure=fig_counties,className="dash-graph" ,style={"padding":"40px 0px 0px 0px"}), width=6),
            ]),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            dbc.Row([
                dbc.Col(
                    dbc.Accordion(
                        [dbc.AccordionItem(analisis_3, title="Análisis: Ubicación de los EVs registrados en WA al rededor de EEUU", style={"padding": "10px 0px 0px 0px","textAlign": "justify"}),
                         dbc.AccordionItem(analisis_4, title="Análisis: Condados con mas EVs registrados", style={"padding": "10px 0px 0px 0px", "textAlign": "justify"})]
                    , start_collapsed=True)
                )
            ])
        ])
    elif pathname == "/caracteristicas":
        return dbc.Container([
            dbc.Row([
                dbc.Col(dcc.Graph(id="torta_modelos", figure=fig_pct_mercado_modelos,className="dash-graph"), width=6),
                dbc.Col(dcc.Graph(id="utility_energy", figure= fig_utilities,className="dash-graph"), width=6),
                dbc.Row(
                    dbc.Accordion(
                        [dbc.AccordionItem(analisis_5, title="Análisis: Marcas Populares WA", style={"padding": "10px 0px 0px 0px","textAlign": "justify"}),
                         dbc.AccordionItem(analisis_6, title="Análisis: Empresas Proveedoras de Energia", style={"padding": "10px 0px 0px 0px", "textAlign": "justify"})]
                    , start_collapsed=False)
                ),
                dbc.Col(dcc.Graph(id="treemap", figure= fig_modelos_por_marcas, className="dash-graph"), width=6),
            ])
        ])
    return html.Div([html.H3("Página no encontrada"), html.P("Seleccione una opción del menú.")])

# Callback para actualizar el contenido según la URL
@app.callback(
    Output("tab-content", "children"),
    Input("url", "pathname")
)
def update_tab(pathname):
    return render_tab_content(pathname)

# Dropdown modificando dos graficos
@app.callback(
    [Output("grafico_linea_tiempo", "figure"),
     Output("grafico_scatter_map", "figure")],
    Input("make_dd", "value")
)
def car_maker_select(selection):
    df_to_filter = dffinal.copy()
    if not selection:
        return fig_time_line_evs, fig_scatter_map
    else:
        df_filtered = df_to_filter[df_to_filter["Make"] == selection]
    df_filtered["Model Year"] = pd.to_datetime(df_filtered["Model Year"], format='%Y')
    df_filtered["Model Year"] = df_filtered["Model Year"].dt.year
    evo_tiempo_new = df_filtered.groupby(["Model Year"]).size().reset_index(name="Count").sort_values(by="Model Year", ascending=False)

    fig_time_line_evs_updated = px.line(evo_tiempo_new,
                x="Model Year",
                y="Count", 
                title=f"Evolución de {selection} por Año en WA", 
                )
    fig_time_line_evs_updated.update_layout(paper_bgcolor="white", 
                    plot_bgcolor="White",
                    yaxis={"gridcolor": "lightgrey", "gridwidth": 0.5})
    fig_time_line_evs_updated.update_traces(line=dict(color="green"))
    
    #  scatter_map de WA EVs
    df_filtered_map = df_filtered.copy()
    fig_scatter_map_updated = px.scatter_map(df_filtered_map, 
                            lat="lat", 
                            lon="lon", 
                            color="Model Year", 
                            color_continuous_scale="Plasma",
                            title=f"Ubicación de los EVs {selection} registrados en WA", 
                            hover_name="Model",
                            custom_data="Model",
                            center={"lat": 47.62912311820097, "lon": -121.04921709398583},
                            map_style="carto-darkmatter",
                            zoom=5)

    fig_scatter_map_updated.update_traces(marker=dict(#color="green", 
                            opacity=0.5),
                    hovertemplate=None)

    fig_scatter_map_updated.update_layout(
        margin={"r":0, "t":40, "l":0, "b":0}
    )
    return fig_time_line_evs_updated, fig_scatter_map_updated





# Ejecutar la aplicación
if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8080, debug=False)