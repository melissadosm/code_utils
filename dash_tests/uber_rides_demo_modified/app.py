#####
# Flask
#####
# A very simple Flask Hello World app for you to get started with...

from flask import Flask

server = Flask(__name__)

# @server.route('/')
# def hello_world():
#     return 'Hello from Flask!'

# Getting python version (different from bash version, so we have to user pip 3.7)
# Instal with pip3.7 install --user
import sys
print(sys.version)


#####
# Dash app 'app.py'
#####

# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import numpy as np

# from dash.dependencies import Input, Output
from plotly import graph_objs as go
# from plotly.graph_objs import *
from datetime import datetime as dt


app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server



# Dictionary of important locations in New York
list_of_locations = {
    "Madison Square Garden": {"lat": 40.7505, "lon": -73.9934},
    "Yankee Stadium": {"lat": 40.8296, "lon": -73.9262},
    "Empire State Building": {"lat": 40.7484, "lon": -73.9857},
    "New York Stock Exchange": {"lat": 40.7069, "lon": -74.0113},
    "JFK Airport": {"lat": 40.644987, "lon": -73.785607},
    "Grand Central Station": {"lat": 40.7527, "lon": -73.9772},
    "Times Square": {"lat": 40.7589, "lon": -73.9851},
    "Columbia University": {"lat": 40.8075, "lon": -73.9626},
    "United Nations HQ": {"lat": 40.7489, "lon": -73.9680},
}

# Initialize data frame
df1 = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/uber-rides-data1.csv",
    dtype=object,
)
# df2 = pd.read_csv(
#     "https://raw.githubusercontent.com/plotly/datasets/master/uber-rides-data2.csv",
#     dtype=object,
# )
# df3 = pd.read_csv(
#     "https://raw.githubusercontent.com/plotly/datasets/master/uber-rides-data3.csv",
#     dtype=object,
# )
# df = pd.concat([df1, df2, df3], axis=0)
df = df1
df["Date/Time"] = pd.to_datetime(df["Date/Time"], format="%Y-%m-%d %H:%M")
df.index = df["Date/Time"]
df.drop("Date/Time", 1, inplace=True)
totalList = []
for month in df.groupby(df.index.month):
    dailyList = []
    for day in month[1].groupby(month[1].index.day):
        dailyList.append(day[1])
    totalList.append(dailyList)
totalList = np.array(totalList)

# Table parameters for testing
params = [
    'Weight', 'Torque', 'Width', 'Height',
    'Efficiency', 'Power', 'Displacement'
]

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np

from dash.dependencies import Input, Output
from plotly import graph_objs as go
from plotly.graph_objs import *
from datetime import datetime as dt

# ---- GRAPHS!

# Map example
# Plotly mapbox public token
import plotly.graph_objects as go
import pandas as pd
us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")


# Plotly mapbox public token
mapbox_access_token = "pk.eyJ1IjoibWVsaXNzYW1vbnRlcyIsImEiOiJja2I4OGNtamcwMXJ0Mnlyc3QzemRhY2N4In0.5wjAPXAoVYra3Vem6F0Mrg"

import plotly.express as px

fig = px.scatter_mapbox(us_cities, lat="lat", lon="lon", hover_name="City", hover_data=["State", "Population"],
                        color_discrete_sequence=["fuchsia"], zoom=3, height=300)
fig.update_layout(mapbox_style="dark", mapbox_accesstoken=mapbox_access_token)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


# Bar plot
animals=['giraffes', 'orangutans', 'monkeys']
fig_bar = go.Figure([go.Bar(x=animals, y=[20, 14, 23])])
fig_bar.update_layout(
    title={
        'text': "Modalidad del contrato",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    # margin=go.layout.Margin(l=10, r=0, t=0, b=50),
    plot_bgcolor="#1E1E1E",
    paper_bgcolor="#1E1E1E",
    font=dict(
        color="#f2f2f2",
        family="Open Sans"
    )
)

# ------ Tab Styles
tabs_styles = {
    'height': '44px',
    'width': '100%'
}
tab_style = {
    'borderTop': '1px solid #31302F',
    'borderBottom': '1px solid #31302F',
    'borderLeft': '1px solid #31302F',
    'borderRight': '1px solid #31302F',
    'padding': '6px',
    'backgroundColor': '#3f413f'
}

tab_selected_style = {
    'borderTop': '1px solid #31302F',
    'borderBottom': '1px solid #31302F',
    'borderLeft': '1px solid #31302F',
    'borderRight': '1px solid #31302F',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

# Layout of Dash App
app.layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                # Column for user controls
                html.Div(
                    className="three columns div-user-controls",
                    children=[
                        html.Img(
                            className="logo", src=app.get_asset_url("dash-logo-new.png")
                        ),
                        html.H3("COVID19 - ALERTAS DE CONTRATACION"),
                        html.P(
                            """
                            A. En esta sección podrás acceder a diferentes tipos de visualización por medio de una búsqueda básica con
                            preguntas o avanzada que permite el cruce de una o más variables de tu interés.
                            B. Puedes descargar las gráficas que desees haciendo click en el botón de descarga
                            C. Al hacer click en los datos de la visualización de tu interés también podrás acceder al listado de hechos
                            de corrupción asociados a la variable. Puedes acceder a todo el contenido de la ficha del hecho haciendo click en "ver más"."""
                        ),
                        html.Div(
                            className="div-for-radio",
                            children=[
                                dcc.RadioItems(
                                    options=[
                                        {'label': 'Alerta 1', 'value': 'Alert1'},
                                        {'label': 'Alerta 2', 'value': 'Alert2'},
                                    ],
                                    value='Alert1',
                                    labelStyle={'display': 'inline-block'}
                                )
                            ],
                        ),
                        html.Div(
                            className="div-for-dropdown",
                            children=[
                                dcc.DatePickerSingle(
                                    id="date-picker",
                                    min_date_allowed=dt(2014, 4, 1),
                                    max_date_allowed=dt(2014, 9, 30),
                                    initial_visible_month=dt(2014, 4, 1),
                                    date=dt(2014, 4, 1).date(),
                                    display_format="MMMM D, YYYY",
                                    style={"border": "0px solid black"},
                                )
                            ],
                        ),
                        # Change to side-by-side for mobile layout
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown for locations on map
                                        dcc.Dropdown(
                                            id="nivel-entidad-dropdown",
                                            options=[
                                                {"label": i, "value": i}
                                                for i in list_of_locations
                                            ],
                                            placeholder="Nivel de la entidad",
                                        )
                                    ],
                                ),
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown for locations on map
                                        dcc.Dropdown(
                                            id="location-dropdown",
                                            options=[
                                                {"label": i, "value": i}
                                                for i in list_of_locations
                                            ],
                                            placeholder="Ubicacion",
                                        )
                                    ],
                                ),
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown to select times
                                        dcc.Dropdown(
                                            id="modalidad-dropdown",
                                            options=[
                                                {
                                                    "label": str(n) + ":00",
                                                    "value": str(n),
                                                }
                                                for n in range(24)
                                            ],
                                            multi=True,
                                            placeholder="Modalidad de contrato",
                                        )
                                    ],
                                ),
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown to select times
                                        dcc.Dropdown(
                                            id="objeto-selector",
                                            options=[
                                                {
                                                    "label": str(n) + ":00",
                                                    "value": str(n),
                                                }
                                                for n in range(24)
                                            ],
                                            multi=True,
                                            placeholder="Objeto del contrato",
                                        )
                                    ],
                                ),
                                html.Div(
                                    className="div-for-input",
                                    children=[
                                        # Input to contratante
                                        dcc.Input(
                                            id="contratante-input",
                                            placeholder='Contratante',
                                            type='text'
                                        )
                                    ],
                                ),
                                html.Div(
                                    className="div-for-input",
                                    children=[
                                        # Input to contratista
                                        dcc.Input(
                                            id="contratista-input",
                                            placeholder='Contratista',
                                            type='text'
                                        )
                                    ],
                                ),
                            ],
                        ),
                        html.P(id="total-rides"),
                        html.P(id="total-rides-selection"),
                        html.P(id="date-value"),
                        dcc.Markdown(
                            children=[
                                "Fuentes: [SECOP I](https://www.datos.gov.co/Presupuestos-Gubernamentales/SECOP-I-2020/c82b-7jfi) | [SECOP II](https://www.datos.gov.co/Gastos-Gubernamentales/SECOP-II-Contratos-Electr-nicos/jbjy-vk9h)"
                            ]
                        ),
                    ],
                ),
                # Column for app graphs and plots
                html.Div(
                    className="nine columns div-for-dash-tables bg-grey",
                    children=[
                        dcc.Tabs(
                            id="tabs-with-classes",
                            value='tab-2',
                            style=tabs_styles,
                        children=[
                            dcc.Tab(
                                label='Alertas',
                                style=tab_style,
                                selected_style=tab_selected_style,
                                children=[
                                    # Title
                                    html.H2("Flagged contracts"),
                                    html.P(
                                        """
                                        A. En esta sección podrás acceder a diferentes tipos de visualización por medio de una búsqueda básica con
                                        preguntas o avanzada que permite el cruce de una o más variables de tu interés.
                                        B. Puedes descargar las gráficas que desees haciendo click en el botón de descarga
                                        C. Al hacer click en los datos de la visualización de tu interés también podrás acceder al listado de hechos
                                        de corrupción asociados a la variable. Puedes acceder a todo el contenido de la ficha del hecho haciendo click en "ver más".
                                        """
                                    ),
                                    # Dash table
                                    html.Div (
                                        className='div-for-table',
                                        children=[
                                            dash_table.DataTable(
                                                id='table-editing-simple',
                                                # Data
                                                columns=(
                                                    [{'id': 'Model', 'name': 'Model'}] +
                                                    [{'id': p, 'name': p} for p in params]
                                                ),
                                                data=[
                                                    dict(Model=i, **{param: 0 for param in params})
                                                    for i in range(1, 5)
                                                ],
                                                # Table interactivity
                                                # editable=True,
                                                # filtering=True,
                                                # sorting=True,
                                                # Table styling
                                                style_table={
                                                    'overflowX': 'auto',
                                                    'margin': '0',
                                                    'overflowY': 'scroll',
                                                },
                                                style_data={
                                                    'border': '0px'
                                                },
                                                # Style cell
                                                style_cell={
                                                    'fontFamily': 'Open Sans',
                                                    'height': '60px',
                                                    'padding': '2px 22px',
                                                    'whiteSpace': 'inherit',
                                                    'overflow': 'hidden',
                                                    'textOverflow': 'ellipsis',
                                                    'backgroundColor': 'rgb(49, 48, 47)',
                                                    'boxShadow': '0 0',

                                                },
                                                # Style header
                                                style_header={
                                                    'backgroundColor': 'rgb(63, 65, 63)',
                                                    'border': '0px'
                                                },
                                                # Style filter
                                                style_filter={
                                                    'fontFamily': 'Open Sans',
                                                    'height': '40px',
                                                    'backgroundColor': 'rgb(217, 217, 217)',
                                                    'fontColor': 'black',
                                                },
                                                page_action='native',
                                                sort_action='native',
                                                filter_action='native',
                                            )
                                        ]
                                    ),
                                    html.P(
                                        """
                                        Para filtrar los resultados de la busqueda
                                        """
                                    ),
                                    html.P(
                                        """
                                        Texto: Escriba el texto por el cual desea buscar. Por ejemplo, al filtrar la columna "A" por el texto "Cundinamarca" obtendra
                                        todos los contratos que contengan la palabra Cundinamarca.
                                        """
                                    ),
                                    html.P(
                                        """
                                        Numerico: Los siguientes operadores son permitidos para los filtros numericos: =, >, >=, <, <=. Por ejemplo, al filtrar
                                        la columna "A" con el siguiente filtro ">2000000", obtendra todos los contratos con "A" mayor a 2 millones de pesos.
                                        """
                                    ),
                                ]
                            ),
                            dcc.Tab(
                                label='Visor de datos',
                                style=tab_style,
                                selected_style=tab_selected_style,
                                children=[
                                    html.H4('Title'),
                                    html.Div(
                                        className="div-for-map",
                                        children=[
                                            dcc.Graph(figure=fig),
                                        ]
                                    ),
                                    html.Div(
                                        className="six columns div-for-bar-chart",
                                        children=[
                                            dcc.Graph(figure=fig_bar),
                                        ]
                                    ),
                                    html.Div(
                                        className="six columns div-for-bar-chart",
                                        children=[
                                            dcc.Graph(figure=fig_bar),
                                        ]
                                    ),
                                ]
                            ),
                            dcc.Tab(
                                label='Sobre este proyecto',
                                style=tab_style,
                                selected_style=tab_selected_style,
                                children=[
                                    html.H4('Title'),
                                    html.Div(
                                        className="div-for-map",
                                        children=[
                                            dcc.Graph(figure=fig),
                                        ]
                                    ),
                                    html.Div(
                                        className="six columns div-for-bar-chart",
                                        children=[
                                            dcc.Graph(figure=fig_bar),
                                        ]
                                    ),
                                    html.Div(
                                        className="six columns div-for-bar-chart",
                                        children=[
                                            dcc.Graph(figure=fig_bar),
                                        ]
                                    ),
                                ]
                            )
                        ])
                    ]
                )
            ]
        )
    ]
)


if __name__ == "__main__":
    app.run_server(debug=True)
