# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 10:01:59 2022

@author: unily
"""

#Dash infrastructure
import dash
from dash import dcc
from dash import html
import pandas as pd
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc   
import plotly.express as px

################
### DASH APP ###    
################
theme = ['ggplot2', 'seaborn', 'simple_white','plotly_white', 'plotly_dark']
indicators = ['Share of population 65+ (%)','Share of population 85+ (%)']

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])
server = app.server

#Tab styles
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

app.layout = html.Div([                   
        dbc.Row(children = [
                     dbc.Col(
                        html.H3('Basic Aging App',
                        style={'textAlign': 'left', 'marginTop': '0.1em', 
                               'marginBottom': '1em', 'color': '#1f77b4'}),
                        width={'size': '7'},
                        lg={'size': '6'})]),
        dcc.Tabs([
            dcc.Tab(label='Animated scatterplot', style=tab_style, selected_style=tab_selected_style,
            children=[
                html.Div([html.P("Select a template:",
                 style={'marginTop': '2em','marginBottom': '1em', "font-weight": "bold",
                        }),
                dcc.Dropdown(
                    id='xaxis-column',
                    options=[{'label': i, 'value': i} for i in theme],
                    placeholder='Select a theme',
                    value = 'plotly_white',
                    multi = False),
                    ],
                    style={'marginTop': '1em','marginBottom': '4em'}),
                dcc.Loading(
                    id="loading-1",
                    children=[html.Div([html.Div(id="loading-output-1"),
                    dbc.Row([
                            dbc.Col(dcc.Graph(id='graph1',
                                    style={"displaylogo": False},
                                  config = {'displaylogo': False,
                                             'modeBarButtonsToRemove': ['toImage']}),
                                  width={'size': '12', 'offset': '0'},
                                lg={'size': '12', 'offset': '0'}
                                ),]), ]),], type="cube")],),
            dcc.Tab(label='State maps', style=tab_style, selected_style=tab_selected_style,
            children=[
                html.Div([html.P("Select an indicator:",
                 style={'marginTop': '2em','marginBottom': '1em', "font-weight": "bold",
                        }),
                dcc.Dropdown(
                    id='xaxis-column2',
                    options=[{'label': i, 'value': i} for i in indicators],
                    placeholder='Select an indicator',
                    value = 'Share of population 65+ (%)',
                    multi = False),
                    ],
                    style={'marginTop': '1em','marginBottom': '4em'}),
                dcc.Loading(
                    id="loading-2",
                    children=[html.Div([html.Div(id="loading-output-2"),
                    dbc.Row([
                            dbc.Col(dcc.Graph(id='graph2',
                                    style={"displaylogo": False},
                                  config = {'displaylogo': False,
                                             'modeBarButtonsToRemove': ['toImage']}),
                                  width={'size': '12', 'offset': '0'},
                                lg={'size': '12', 'offset': '0'}
                                ),]), ]),], type="cube")],)]),],
                 style={'object-fit': 'contain', 
                'height':'Auto', 'width': '100wv',
                 'padding':'30px 30px 30px 30px'}
                )

#################################
# CALLBACKS
#################################
@app.callback(
    Output('graph1', 'figure'),
    [Input('xaxis-column', 'value')])

def update_graph1(xaxis_column_name):
    df = pd.read_csv('animation_data.csv')
    decades = [1950,1960,1970,1980,1990,2000,2010,2020,2030,2050,2060,2070,2080,2090,2100]
    df_d = df[df.Year.isin(decades)]
    fig = px.scatter(df_d, x="Share_65+", y="LifExp", animation_frame="Year", animation_group="Continent/Country", 
                     size_max=50,
           size="Pop", color="Continent/Country", hover_name="Continent/Country",
           title ='People are living longer and societies are aging worldwide' ,
           template = xaxis_column_name,
            range_x=[0,50], range_y=[4,100])
    fig.update_layout(showlegend=True, margin=dict(t=50, l=50),
                xaxis_title="Share of the population 65 years and older",
                yaxis_title="Life expectancy at birth",
                title_font_family="Arial Black",
                font_family="Arial",
                title_font_color="black",
                title_font_size=19,
                uniformtext_minsize=14)
    fig.update_xaxes(showline=False, linewidth=2, linecolor='black', showspikes=True)
    fig.update_yaxes(showline=False, linewidth=2, linecolor='black', showspikes=True)
    return fig

@app.callback(
    Output('graph2', 'figure'),
    [Input('xaxis-column2', 'value')])

def update_graph2(xaxis_column_name2):
    df_s = pd.read_csv('pop_states.csv')
    
    if xaxis_column_name2 == 'Share of population 65+ (%)':
        fig2 = px.choropleth(df_s,locationmode="USA-states",scope="usa",
                             title = 'Percentage of the Population 65 years and older by state',
                             locations= 'State ', color = "Share_65+ ", 
                             color_continuous_scale=px.colors.sequential.Blues)
        fig2.update_layout(margin={'r':0,'t':30,'l':0,'b':0})
        
        fig2.update_layout(coloraxis_colorbar=dict(title="Share of the population 65+"),
                            title_font_color="black",
                            title_font_size=18, legend_title_font_color="black",
                            title={'x':0.4,'xanchor':'center'})
        return fig2
    if xaxis_column_name2 == 'Share of population 85+ (%)':
        fig2 = px.choropleth(df_s,locationmode="USA-states",scope="usa",
                             title = 'Percentage of the Population 85 years and older by state',
                             locations= 'State ', color = "Share_85+ ", 
                             color_continuous_scale=px.colors.sequential.Blues)
        fig2.update_layout(margin={'r':0,'t':30,'l':0,'b':0})
        
        fig2.update_layout(coloraxis_colorbar=dict(title="Share of the population 85+"),
                            title_font_color="black",
                            title_font_size=18, legend_title_font_color="black",
                            title={'x':0.4,'xanchor':'center'})
        return fig2
    

if __name__ == '__main__':
    app.run_server()


