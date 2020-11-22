#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 10:43:02 2020

@author: angelinejayanegara
"""
import dash
import dash.dependencies as dd
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go

import numpy as np

from dash.dependencies import Input, Output
import dash_table
import dash_bootstrap_components as dbc

from io import BytesIO

import pandas as pd
from wordcloud import WordCloud
import base64
import plotly.express as px
import collections
#import plotly.graph_objects as go


# bootstrap theme
# https://bootswatch.com/lux/
external_stylesheets = [dbc.themes.LUX]

print("Loading")

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.title = "Market Analysis - Data Science Project"

#all data
raw = pd.read_csv('All_Data.csv', encoding='Latin-1')
raw.pop("Singleton")
raw.pop('Length')
alldata = raw.replace(np.nan, '', regex=True)

#all conferences data
df = pd.read_csv("all_highlighted_conferences.csv")
#print(df[:5])
df0 = pd.read_csv("GTC_conference.csv")
df1 = pd.read_csv("bigdata2019_conference.csv")
df2 = pd.read_csv("bigdata2020_conference.csv")
df3 = pd.read_csv("digwork_conference.csv")
df4 = pd.read_csv("oracle_conference.csv")

#all industries data
dfin1 = pd.read_csv("aerospaceLab.csv")
dfin2 = pd.read_csv("engineeringTransportation.csv")
dfin3 = pd.read_csv("healthcare.csv")
dfin4 = pd.read_csv("highereducation.csv")
dfin5 = pd.read_csv("software.csv")

#All companies data
dfc1 = pd.read_csv("amazon.csv")
dfc2 = pd.read_csv("Google.csv")
dfc3 = pd.read_csv("IBM.csv")
dfc4 = pd.read_csv("Microsoft.csv")
dfc5 = pd.read_csv("NVIDIA.csv")
dfc6 = pd.read_csv("Oracle.csv")

app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Market Analysis"), className="mb-2")
        ]),
        dbc.Row([
            dbc.Col(html.H6(children='Visualizing the highlights and similarities between conferences or industries in the market'), className="mb-4")
        ]),

        dbc.Row([
            dbc.Col(dbc.Card(html.H4(children='Companies Clustering and Conferences Similarities',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
                    , className="mb-4")
        ]),
        
    dbc.Row(
                    [
                        dbc.Col(html.Img(src="/assets/meanclustering.jpg")),
                        dbc.Col(html.Img(src="/assets/voronoi.jpg")),
                    ]),
    dbc.Row(html.Br()),
    
    dbc.Row([
            dbc.Col(dbc.Card(html.H4(children='Highlighted Topics in Conferences',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
                    , className="mt-4 mb-5")
    ]),
    
    dbc.Row([
            dbc.Col(html.H6(id='output_container', children=[]), className="mb-4")
        ]),
    
    dcc.Dropdown(
        id='ddconferences',
        options=[
            {'label': 'All conferences','value': 'All'},
            {'label': 'GTC',            'value': 'GTC'},
            {'label': 'Big Data 2019',  'value': 'Big Data 2019'},
            {'label': 'Big Data 2020',  'value': 'Big Data 2020'},
            {'label': 'Digital Work',        'value': 'Digwork'},
            {'label': 'Oracle',         'value': 'Oracle'}
        ],
        value='All',
        style={'width': '48%', 'margin-left':'5px'}
        ),
    

    dcc.Graph(id='conference_graph',figure={}),

    dbc.Row([
            dbc.Col(dbc.Card(html.H4(children='Highlighted Topics in Industries according to NVIDIA GTC conference',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
                    , className="mt-4 mb-5")
        ]),
        
    dbc.Row([
            dbc.Col(html.H6(id='output_container2', children=[]), className="mb-4")
        ]),

    dcc.Dropdown(
        id='industries',
        options=[
            {'label': 'Aerospace', 'value': 'aerospaceLab'},
            {'label': 'Engineering & Transportation', 'value': 'engineeringTransportation'},
            {'label': 'Healthcare', 'value': 'healthcare'},
            {'label': 'Higher Education', 'value': 'highereducation'},
            {'label': 'Software', 'value': 'software'},
            {'label': 'All industries', 'value': 'All'}
        ],
        value='aerospaceLab',
        style={'width': '48%', 'margin-left':'5px'}
        ),
    
    dcc.Graph(id='topics_graph',figure={}),
    
    #companies highlights
    dbc.Row(dbc.Col(html.Br())),
    
    dbc.Row([
            dbc.Col(dbc.Card(html.H4(children='Highlighted Topics of Companies',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
                    , className="mt-4 mb-5")
    ]),
    
    dbc.Row([
            dbc.Col(html.H6(id='output_container3', children=[]), className="mb-4")
        ]),
    
    dcc.Dropdown(
        id='ddcompanies',
        options=[
            {'label': 'Amazon',   'value': 'Amazon'},
            {'label': 'Google',   'value': 'Google'},
            {'label': 'IBM',      'value': 'IBM'},
            {'label': 'Microsoft','value': 'Microsoft'},
            {'label': 'NVIDIA',   'value': 'NVIDIA'},
            {'label': 'Oracle',   'value': 'Oracle'}
        ],
        value='Amazon',
        style={'width': '48%', 'margin-left':'5px'}
        ),

    dcc.Graph(id='companies_graph1',figure={}),
    
    dcc.Input(
            id='searchinput',
            type="text",
            placeholder="write a company name here",
            value='Amazon',
            style={'width': '48%', 'margin-left':'5px'}
            ),
    
    dcc.Graph(id='companies_graph',figure={})
    
    ])

])



# page callbacks

@app.callback(
    [Output(component_id='output_container2' , component_property='children'),
     Output(component_id='topics_graph' , component_property='figure')],    
    Input(component_id='industries', component_property='value'))

def update_graph2(option_slctd):
    
    container = "The industry chosen by user is: {}".format(option_slctd)
    
    if option_slctd=='All': dff = df0
    elif option_slctd=='aerospaceLab': dff = dfin1
    elif option_slctd=='engineeringTransportation': dff = dfin2
    elif option_slctd=='healthcare': dff = dfin3
    elif option_slctd=='highereducation': dff = dfin4
    elif option_slctd=='software': dff = dfin5
    
    fig = px.bar(dff, x="Keyword", y="Frequency", color ='Frequency', barmode="group")
    # Update remaining layout properties
    fig.update_layout(
        title_text="Highlighted Keywords",
        showlegend=False,
        )
    return container, fig

@app.callback(
    [Output(component_id='output_container' , component_property='children'),
     Output(component_id='conference_graph' , component_property='figure')],    
    Input(component_id='ddconferences', component_property='value'))

def update_graph(option_slctd):
    
    container = "The conference chosen by user is: {}".format(option_slctd)
    
    if option_slctd=='All': dff = df
    elif option_slctd=='GTC': dff = df0
    elif option_slctd=='Big Data 2019': dff = df1
    elif option_slctd=='Big Data 2020': dff = df2
    elif option_slctd=='Digwork': dff = df3
    elif option_slctd=='Oracle': dff = df4
    
    fig = px.bar(dff, x="Keyword", y="Frequency", color ='Frequency', barmode="group")
    # Update remaining layout properties
    fig.update_layout(
        title_text="Highlighted Keywords",
        showlegend=False,
        )
    return container, fig

@app.callback(
    [Output(component_id='output_container3' , component_property='children'),
     Output(component_id='companies_graph' , component_property='figure')],
    Input(component_id='searchinput', component_property='value'))

def highlightedTopic(text):
    
    container = "The company chosen by user is: {}".format(text)

   
    filter = alldata[alldata['Inc'] == text]
    train = list(filter.Keywords)
    t = [item.split(',') for item in train]
    flat_list = []
    for sublist in t:
        for item in sublist:
            flat_list.append(item)
    counter = collections.Counter(flat_list)
    c= counter.most_common()
    data = c[:10]
    dataframe = pd.DataFrame(data, columns =['Keyword', 'Frequency'])
    fig = px.bar(dataframe, x="Keyword", y="Frequency", color ='Frequency', barmode="group")
    # Update remaining layout properties
    fig.update_layout(
        title_text="Highlighted Keywords",
        showlegend=False,)
    return container, fig

@app.callback(
    [Output(component_id='output_container3' , component_property='children'),
     Output(component_id='companies_graph1' , component_property='figure')],    
    Input(component_id='ddcompanies', component_property='value'))

def update_graph3(option_slctd):
    
    container = "The company chosen by user is: {}".format(option_slctd)
    
    if option_slctd=='Amazon': dff = dfc1
    elif option_slctd=='Google': dff = dfc2
    elif option_slctd=='IBM': dff = dfc3
    elif option_slctd=='Microsoft': dff = dfc4
    elif option_slctd=='NVIDIA': dff = dfc5
    elif option_slctd=='Oracle': dff = dfc6
    
    fig = px.bar(dff, x="Keyword", y="Frequency", color ='Frequency', barmode="group")
    # Update remaining layout properties
    fig.update_layout(
        title_text="Highlighted Keywords",
        showlegend=False,
        )
    return container, fig 


if __name__ == '__main__':
    app.run_server(host='127.0.0.1', debug=False)
