# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 10:01:59 2022

@author: unily
"""

# Dash infrastructure
import dash
from dash import dcc
from dash import html
import pandas as pd
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc   
import plotly.express as px

df = pd.read_csv('animation_data.csv', encoding='latin-1')

################
### DASH APP ###    
################
    
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN],
                meta_tags=[{'name': 'viewport',
                'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.8,'}])
server = app.server

indicators = ['Explicit Subsidies','Implicit Subsidies','Total Subsidies']

# Dash tab styles
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '20px',
    'fontWeight': 'bold',
    'color': '#1f77b4'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#1f77b4',
    'color': 'white',
    'padding': '20px'
}

app.title = 'Fossil Fuel Subsidies in LAC' 

app.layout = html.Div([                   
    dbc.Row(children = [dbc.Col(
                        html.H2('Energy Subsidies in LAC',
                                style={'color':'black'}),
                        width={'size': '7'},
                        lg={'size': '6'}),
                dbc.Col(children= [
                        dbc.CardImg(src="/assets/logo.jpg", 
                        top=True, style={"width": "5rem"}),
                        ], width={'size': '2', 'offset': '3'},
                        lg={'size': '2', 'offset': '4'}),
                        ]),                      
                dbc.Col( children = [  html.Div([
                    
                    html.P("Select an indicator:",
                     style={'marginTop': '1em','marginBottom': '1em', "font-weight": "bold",
                            'display': 'inline-block','marginBottom': '0.5em', 'marginLeft': '9em'})
                    ]),
                    dcc.Dropdown(
                        id='xaxis-column',
                        options=[{'label': i, 'value': i} for i in indicators],
                        placeholder='Select an indicator',
                        value = 'Share of population 65+ (%)',
                        multi = False,
                        style={'marginTop': '0em','marginBottom': '4em', 
                               'marginLeft': '4.5em','width':'87%'},
                        
                              ),
    dbc.Row([
        dcc.Loading(
            id="loading-1",
            children=[html.Div([html.Div(id="loading-output-1"),
                dbc.Row([
                    dbc.Col(dcc.Graph(id='graph1',
                        style={"displaylogo": False},
                        config={'displaylogo': False, 'modeBarButtonsToRemove': ['toImage']}),
                        width={'size': 12, 'offset': 0},
                        lg={'size': 12, 'offset': 0}
                    ),
                ]),
            ]),
            ],
            type="cube"
        ),
    ]),
                    html.P("\
                            Notes: Country-year GDP values determine the size of the bubble. \
                            Oil rents are the difference between the value of crude oil production at regional \
                            prices and total costs of production. \
                            See: https://data.worldbank.org/indicator/NY.GDP.PETR.RT.ZS?end=2021&start=2010 \
                            ",
                     style={'marginTop': '2em','marginBottom': '1em','offset':3,
                    'textAlign': 'justify', "width": "75%", 'marginLeft': '10em'}
                            ),
                    ],
                        style = {'display': 'inline-block', 'vertical-align': 'middle',
                                 'marginBottom': '1em'})
                    ])


@app.callback(
    Output('graph1', 'figure'),
    [Input('xaxis-column', 'value')])

def update_graph1(xaxis_column_name):
    df = pd.read_csv('animation_data.csv')
    decades = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
    df_d = df[df.Year.isin(decades)]

    # Remove percentage signs and convert to numeric
    df_d["Oil rent (% of GDP)"] = df_d["Oil rent (% of GDP)"].str.rstrip('%').astype('float')
    df_d["Total Subsidies"] = df_d["Total Subsidies"].str.rstrip('%').astype('float')
    df_d["Explicit Subsidies"] = df_d["Explicit Subsidies"].str.rstrip('%').astype('float')
    df_d["Implicit Subsidies"] = df_d["Implicit Subsidies"].str.rstrip('%').astype('float')

    if xaxis_column_name == 'Explicit Subsidies':
    # Sort the DataFrame by the desired columns
        df_d = df_d.sort_values(by=["Country","Year","Oil rent (% of GDP)", "Total Subsidies","Explicit Subsidies","Implicit Subsidies"])
    
        graph1 = px.scatter(df_d, x="Oil rent (% of GDP)", y="Explicit Subsidies", animation_frame="Year", animation_group="Country",
                            color="Country", hover_name="Country", size='GDP',
                            title='LAC: Trends in oil revenues & fossil fuel subsidies',
                            range_x=[-0.5,25], range_y=[0,25], size_max=50)
        graph1.update_layout(showlegend=True,
                             xaxis_title="Oil rent (% of GDP, WB (2024))",
                             yaxis_title="Explicit Subsidies (% of GDP, IMF (2023))",
                             title_font_family="Arial Black",
                             font_family="Arial",
                             title_font_color="black",
                             title_font_size=19,
                             uniformtext_minsize=14,
                             width =1200,
                             height=800,  # Increase height as needed
        # Set animation frame duration to 1000 milliseconds (1 second)
                             updatemenus=[dict(type="buttons", buttons=[dict(
                                                                              args=[None, {"frame": {"duration": 1000}}])])])
        graph1.update_xaxes(showline=False, linewidth=2, linecolor='black', showspikes=True)
        graph1.update_yaxes(showline=False, linewidth=2, linecolor='black', showspikes=True)
        
        return graph1

    if xaxis_column_name == 'Implicit Subsidies':
    # Sort the DataFrame by the desired columns
        df_d = df_d.sort_values(by=["Country","Year","Oil rent (% of GDP)", "Implicit Subsidies"])
    
        graph1 = px.scatter(df_d, x="Oil rent (% of GDP)", y="Implicit Subsidies", animation_frame="Year", animation_group="Country",
                            color="Country", hover_name="Country", size='GDP',
                            title='LAC: Trends in oil revenues & fossil fuel subsidies',
                            range_x=[-0.5,25], range_y=[0,25], size_max=50)
        graph1.update_layout(showlegend=True,
                             xaxis_title="Oil rent (% of GDP, WB (2024))",
                             yaxis_title="Implicit Subsidies (% of GDP, IMF (2023))",
                             title_font_family="Arial Black",
                             font_family="Arial",
                             title_font_color="black",
                             title_font_size=19,
                             uniformtext_minsize=14,
                             width =1200,
                             height=800,  # Increase height as needed
        # Set animation frame duration to 1000 milliseconds (1 second)
                             updatemenus=[dict(type="buttons", buttons=[dict(
                                                                              args=[None, {"frame": {"duration": 1000}}])])])
        graph1.update_xaxes(showline=False, linewidth=2, linecolor='black', showspikes=True)
        graph1.update_yaxes(showline=False, linewidth=2, linecolor='black', showspikes=True)
        
        return graph1

    if xaxis_column_name == 'Total Subsidies':
    # Sort the DataFrame by the desired columns
        df_d = df_d.sort_values(by=["Country","Year","Oil rent (% of GDP)", "Total Subsidies"])
    
        graph1 = px.scatter(df_d, x="Oil rent (% of GDP)", y="Total Subsidies", animation_frame="Year", animation_group="Country",
                            color="Country", hover_name="Country", size='GDP',
                            title='LAC: Trends in oil revenues & fossil fuel subsidies',
                            range_x=[-0.5,25], range_y=[0,25], size_max=50)
        graph1.update_layout(showlegend=True,
                             xaxis_title="Oil rent (% of GDP, WB (2024))",
                             yaxis_title="Implicit Subsidies (% of GDP, IMF (2023))",
                             title_font_family="Arial Black",
                             font_family="Arial",
                             title_font_color="black",
                             title_font_size=19,
                             uniformtext_minsize=14,
                             width =1200,
                             height=800,  # Increase height as needed
        # Set animation frame duration to 1000 milliseconds (1 second)
                             updatemenus=[dict(type="buttons", buttons=[dict(
                                                                              args=[None, {"frame": {"duration": 1000}}])])])
        graph1.update_xaxes(showline=False, linewidth=2, linecolor='black', showspikes=True)
        graph1.update_yaxes(showline=False, linewidth=2, linecolor='black', showspikes=True)
        
        return graph1


if __name__ == '__main__':
    app.run_server(debug=True)
