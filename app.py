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
from urllib.request import urlopen
import json

################
### DASH APP ###    
################
theme = ['ggplot2', 'seaborn', 'simple_white','plotly_white', 'plotly_dark']
indicators = ['Share of population 65+ (%)','Share of population 85+ (%)']

#FIPS
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)
    
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN],
                meta_tags=[{'name': 'viewport',
                'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.8,'}])
server = app.server

#Dash tab styles
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

app.title = 'Aging-USA' 

app.layout = html.Div([                   
        dbc.Row([
            
                dbc.Col(
                        html.H3('The Visual Chronicle of an Aging Nation',
                        style={'textAlign': 'center', 'marginTop': '0.1em', 
                               'marginBottom': '2em', 'color': '#1f77b4'}),
                        width={'size': '7', 'offset':3},
                        lg={'size': '6'})]),
                html.Div([ html.H5('Alvaro A. Montoya',
                                 style={'textAlign': 'center', 'marginTop': '0em', 
                               'marginBottom': '0em', 'color': 'black'}
                                  ),
                          html.H6('December 2022',
                                 style={'textAlign': 'center', 'marginTop': '0.2em', 
                               'marginBottom': '2em', 'color': 'black'}
                                  ),
                    html.P("\
                                 Despite being relatively young for a developed nation, the United States (US) is aging fast. \
                                 According to population estimates from the Census Bureau (CB), in 2035 the number of adults \
                                 aged 65 and older will outnumber the number of children under 18 (77 million versus 76.7 million) \
                                 (Census, 2019). The aging process started decades ago and will accelerate its pace in the following \
                                 two decades. In 1990 there were approximately 30 million elderly citizens, representing 12% of the \
                                 total US population. In 2022 the number of adults 65 and older has doubled to about 60 million, with \
                                 a population share of 17%. This demographic shift will continue until the end of the century (UNPF, 2022), \
                                 with relevant consequences for public policies related to social protection and health.\
                                 With the aim of helping policymakers explore the demographic process from different optics, \
                                 this blog post illustrates the US's aging process through a set of interactive visuals\
                                 that provide demographic data at three geographical levels: National, State, and Counties.",
                         style={'marginTop': '2em','marginBottom': '1em','offset':3,
                        'textAlign': 'justify', "width": "75%", 'marginLeft': '10em'}
                                ),
                        ],
                            style = {'display': 'inline-block', 'vertical-align': 'middle',
                                     'marginBottom': '1em'}),
                
                dbc.Col(html.Iframe(src="https://public.tableau.com/views/demographics_usa/Dashboard1?:showVizHome=no&:embed=true",
                        style={"height": "630px", "width": "70%", 'display': 'inline-block',
                               "marginLeft":"13em", "border":"1px"
                       })),
                html.Div([html.P("\
                                 For the first time in human history, many countries are being referred to as “Super Age” \
                                 populations (having at least 20 percent of their population aged 65 and older). The data \
                                 presented in this briefing indicates that several US states could already be considered as \
                                 Super Age populations. The next figure displays the share of people aged 65 and older in each\
                                 state by gender. Three facts derive from this graph. First, given that women live \
                                 longer than men on average, the share of elderly women is higher than that of men in all states. \
                                 Also, if they were countries, several US states would already be considered Super Age nations. \
                                 It is also evident that northern New England (e.g. Maine) and retiree-magnet (e.g. Florida) states \
                                 have the highest share of men and women aged 65 and older.",
                         style={'marginTop': '2em','marginBottom': '1em',
                        'textAlign': 'justify', "width": "75%", 'marginLeft': '10em'}
                                ),
                        ],
                            style = {'display': 'inline-block', 'vertical-align': 'middle',
                                     'marginBottom': '1em'}),
                dbc.Col(html.Iframe(src="https://public.tableau.com/views/demographics_usa_gender/Dashboard1?:showVizHome=no&:embed=true",
                        style={"height": "1150px", "width": "72%", 'display': 'inline-block',
                               "marginLeft":"13em", "border":"1px"
                       })),

                html.Div([html.P("\
                                 As the two figures presented so far show, demographic data can help us \
                                 understand the current stage of the demographic shift, as well as the most probable \
                                 direction different population subgroups will take. Furthermore, granularity can highlight \
                                 relevant differences between population subgroups such as gender or state. In this vein, \
                                 the following maps provide a deep dive into the aging process at the \
                                 county level, with the ultimate goal of helping policymakers identify sub-regional demographic \
                                 trends for the US. Each map presents, respectively, the share of the population aged 65 and older and 85 older at the county \
                                 level. The drop-down menu allows users to select each age group",
                         style={'marginTop': '1em','marginBottom': '1em',
                        'textAlign': 'justify', "width": "75%", 'marginLeft': '10em'}
                                ),
                        ],
                            style = {'display': 'inline-block', 'vertical-align': 'middle',
                                     'marginBottom': '1em'}),
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
                dcc.Loading(
                    id="loading-1",
                    children=[html.Div([html.Div(id="loading-output-1"),
                    dbc.Row([
                            dbc.Col(dcc.Graph(id='graph1',
                                    style={"displaylogo": False},
                                  config = {'displaylogo': False,
                                             'modeBarButtonsToRemove': ['toImage']},
                                  ),
                                  width={'size': '12', 'offset': '4'},
                                lg={'size': '12', 'offset': '0'}
                                ),
                                ]),
                            ]),
                      ], type="cube"),
                        html.Div([html.P("\
                         Studying the aging process at the county level is relevant for several reasons. \
                         First, the aging process is a complex phenomenon that can vary greatly across \
                         different regions and communities. By studying the aging process at the county level,\
                         researchers can gain a more detailed and nuanced understanding of how aging affects \
                         different parts of the country. Second, understanding the aging process at the county \
                         level can help policymakers and local governments to better anticipate and address the \
                         challenges and opportunities that come with an aging population. For example, they can \
                         use this information to develop targeted policies and programs to support older adults \
                         and their families and to plan for the future needs of the aging population.",
                 style={'marginTop': '6em','marginBottom': '2em',
                'textAlign': 'justify', "width": "75%", 'marginLeft': '7em'}
                        ),
                                 html.P("\
                         Finally, studying \
                         the aging process at the county level can help researchers to identify trends and patterns in \
                         the data, which can inform the development of more effective interventions and policies. \
                         For example, researchers may find that certain counties are experiencing a faster rate of \
                         aging than others, or that certain groups of older adults are more likely to face certain \
                         challenges (e.g., poverty in old age). This information can be used to develop more tailored \
                         approaches to addressing the needs of older adults in the US.",
                 style={'marginTop': '0em','marginBottom': '4em',
                'textAlign': 'justify', "width": "75%", 'marginLeft': '7em'}
                        )
                ],
                    style = {'display': 'inline-block', 'vertical-align': 'middle',
                             'marginBottom': '1em', 'marginLeft': '3em',
                             'textAlign': 'justified'}),
                ]),
                ],
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

    table = pd.read_csv('pop_county.csv', index_col=0,encoding="utf-8",
             dtype={'0': 'int32', '26': 'int32', '27': 'int32',
                    '%65+': 'float64', '%85+': 'float64',
                    'county': 'str', 'fips': 'str'})
    
    if xaxis_column_name == 'Share of population 65+ (%)':
        fig = px.choropleth(table, geojson=counties, locations='fips', color='%65+',
                                   color_continuous_scale='Blues',
                                   range_color=(0, 60),
                                   scope="usa",
                                   hover_name ='county',
                                   labels={'%65+':'Share of population 65+ (%) '},
                                                                          )
        fig.update_layout(hovermode="x")
        fig.update_layout(margin={'r':0,'t':30,'l':0,'b':0})

        fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
        fig.update_layout(title_text = 'National Average in 2021 (Census Bureau): 16.5%',                
                          title_font_color="black",
                          title_font_size=18, legend_title_font_color="black",
                          title={'x':0.4,'xanchor':'center'}
                                 )
        fig.data[0].colorbar.x=0.9

        return fig
    
    if xaxis_column_name == 'Share of population 85+ (%)':
        fig = px.choropleth(table, geojson=counties, locations='fips', color='%85+',
                                   color_continuous_scale='Reds',
                                   range_color=(0, 15),
                                   scope="usa",
                                   hover_name ='county',
                                   labels={'%85+':'Share of population 85+ (%) '}
                                  )
        fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
        fig.update_layout(title_text = 'National Average in 2021 (Census Bureau): 1.9%',                
                          title_font_color="black",
                          title_font_size=18, legend_title_font_color="black",
                          title={'x':0.4,'xanchor':'center'}
                                 )
        fig.data[0].colorbar.x=0.9
        return fig
    

if __name__ == '__main__':
    app.run_server()


