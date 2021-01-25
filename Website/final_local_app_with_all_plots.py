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
from sklearn.manifold import TSNE

import pandas as pd
from wordcloud import WordCloud
import base64
import plotly.express as px
import collections
import networkx as nx

#import plotly.graph_objects as go


# bootstrap theme
# https://bootswatch.com/lux/
external_stylesheets = [dbc.themes.LUX]

print("Loading")

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.title = "Market Analysis - Data Science Project"

#all data
raw = pd.read_csv('ALL_DATA.csv', encoding='Latin-1')
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

#Vectorizations data
vec = pd.read_csv('vectors_inc.csv', encoding="utf-8-sig") 
model = pd.read_csv('vecdf.csv', encoding="utf-8-sig")

tsne = TSNE(random_state=1991,n_iter=1500,metric='cosine',n_components=2)

embd_tr = tsne.fit_transform(model)

figvec = px.scatter(x=embd_tr[:,0], y=embd_tr[:,1], color=vec['Inc'].values, hover_data= [vec['Inc']], width=1100, height=700)
figvec1 = figvec.update_traces(showlegend=False)

#Distance Matrix
dm = pd.read_csv("companyDis.csv")
cn = pd.read_csv("CompName.csv")

app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Market Analysis"), className="mb-2")
        ]),
        dbc.Row([
            dbc.Col(html.H6(children='Visualizing the highlights and similarities between conferences, industries, or companies in the market'), className="mb-4")
        ]),
        #Companies Similarities Scatter Plot
        dbc.Row([
            dbc.Col(dbc.Card(html.H4(children='Companies Representation Scatter Plot',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
                    , className="mb-4")
        ]),
        
    dbc.Row( dcc.Graph(id='vectorization1', figure=figvec1)),
    
    dbc.Row(html.Br()),
    
    #Companies Similarities Network Graph
    dbc.Row(dbc.Col(html.Br())),
    
    dbc.Row([
            dbc.Col(dbc.Card(html.H4(children='Companies Similarities Network Graph',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
                    , className="mt-4 mb-5")
    ]),
    
    dbc.Row([
            dbc.Col(html.H6(id='output_container0', children=[]), className="mb-4")
        ]),
    
    #Search input
    dcc.Input(
            id='searchinput0',
            type="text",
            placeholder="write a company name here",
            value='Amazon',
            style={'width': '48%', 'margin-left':'5px'}
            ),
    
    dcc.Graph(id='companies_graph0',figure={}),
    
    dbc.Row(dbc.Col(html.Br())),
    
    #Highlighted Topics in Conferences
    
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
            {'label': 'Digital Work',   'value': 'Digwork'},
            {'label': 'Oracle',         'value': 'Oracle'}
        ],
        value='All',
        style={'width': '48%', 'margin-left':'5px'}
        ),
    

    dcc.Graph(id='conference_graph',figure={}),
    
    #Highlighted Topics in Industries according to NVIDIA GTC conference

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
    
    dcc.Graph(id='topics_graph',figure=figvec),
    
    #Companies Highlights
    dbc.Row(dbc.Col(html.Br())),
    
    dbc.Row([
            dbc.Col(dbc.Card(html.H4(children='Highlighted Topics of Companies',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
                    , className="mt-4 mb-5")
    ]),
    
    dbc.Row([
            dbc.Col(html.H6(id='output_container3', children=[]), className="mb-4")
        ]),
    
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
    [Output(component_id='output_container0' , component_property='children'),
     Output(component_id='companies_graph0' , component_property='figure')],
    Input(component_id='searchinput0', component_property='value'))

def CompSim_2(name):
    
    container = "The company chosen by user is: {}".format(name)
    
    distanceMatrix = dm.values
    LP = list(vec.Inc.unique())
    index = LP.index(name)  
    sortingL = []
    for i in range(0,280):
        sortingL.append((distanceMatrix[index][i],LP[i],i))
    res1 = sorted(sortingL,key=lambda x: x[0],reverse=False)[:9]
    res2 = [i[2] for i in res1]
    compName = [i[1] for i in res1]
    resMatrix = np.zeros((len(res2), len(res2)))
    for i in range(0,len(res2)):
        for j in range(0,len(res2)):
            resMatrix[i][j] = distanceMatrix[res2[i]][res2[j]]
    forComp = pd.DataFrame(resMatrix,compName,compName)
    
    #plotting
    dist_df = forComp
    G = nx.Graph()
    for i, row_i in dist_df.iterrows():
        for j, row_j in dist_df.iterrows():
            G.add_edge(i,j,weight=dist_df.loc[i][j]*2)
            
    pos = nx.kamada_kawai_layout(G)
    edge_trace = go.Scatter(x=[],y=[],line={'width':0.5,'color':'#888'},hoverinfo='none',mode='lines')
    for edge in G.edges():
        x0,y0=pos.get(edge[0])
        x1,y1=pos.get(edge[1])
        edge_trace['x']+=tuple([x0,x1])
        edge_trace['y']+=tuple([y0,y1])

    node_trace = go.Scatter(x=[], y=[], text=[], mode='markers', hoverinfo='text') 
    for node in G.nodes():
        x, y=pos.get(node)
        node_trace['x']+=tuple([x])
        node_trace['y']+=tuple([y])
    node_trace.text = compName

        #    return{"data":[edge_trace, node_trace],
    fig= go.Figure(data=[edge_trace, node_trace])

    fig.update_layout(width=800, height=800, showlegend=False, hovermode='closest',
                      margin={'b': 20, 'l': 5, 'r': 5, 't': 40},
                      xaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
                      yaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False})
    
    return container, fig


if __name__ == '__main__':
    app.run_server(host='127.0.0.1', debug=False)
