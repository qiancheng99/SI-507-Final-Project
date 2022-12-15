import math
import json
import numpy as np
import pandas as pd
import networkx as nx
import cartopy
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
# from IPython.display import Image

def draw_network(plot=True):
    f = open('airlines_us.json')
    data = json.load(f)
    edges=[]
    for ori in data.keys():
        for des in data[ori][-1].keys():
            if [des,ori] in edges:continue
            edges.append([ori,des])
#     print(len(edges))
    edges=np.asarray(edges)
    g = nx.from_edgelist(edges)
    sg = next((g.subgraph(c) for c in nx.connected_components(g)))
    if plot:
#         fig, ax = plt.subplots(1, 1, figsize=(100,100))
#         nx.draw_networkx(sg, ax=ax, node_size=333,
#                          font_size=30, alpha=.5,
#                          width=1.2,node_color='red',font_color='blue')
#         ax.set_axis_off()
        fig, ax = plt.subplots(1, 1, figsize=(100,100))
        nx.draw_networkx(sg, ax=ax, node_size=10,
                         font_size=10, alpha=.5,
                         width=1,node_color='red',font_color='blue')
        ax.set_axis_off()
        plt.show()

    return edges, sg

def draw_map():
    edges,sg=draw_network(False)
    f = open('airport_dict.json')
    airport_dict = json.load(f)

    names = ('id,name,city,country,iata,icao,lat,lon,'
             'alt,timezone,dst,tz,type,source').split(',')
    airports = pd.read_csv(
        'https://github.com/ipython-books/'
        'cookbook-2nd-data/blob/master/'
        'airports.dat?raw=true',
        header=None,
        names=names,
        index_col=4,
        na_values='\\N')
    airports_us = airports
    unique_index = set(airports_us.index)
    unique_index.remove(np.nan)
    airports_us_index = airports_us.index.isin(unique_index)
    airports_us = airports_us[airports_us_index]
    pos = {airport: (v['lon'], v['lat'])
           for airport, v in
           airports_us.to_dict('index').items() if airport in airport_dict}
    deg = nx.degree(sg)
    sizes = [5 * deg[iata] for iata in sg.nodes]
    altitude = airports_us['alt']
    altitude = [altitude[iata] for iata in sg.nodes]
    labels = {iata: iata if deg[iata] >= 20 else ''
              for iata in sg.nodes}
    crs = ccrs.PlateCarree()
    fig, ax = plt.subplots(
        1, 1, figsize=(12, 8),
        subplot_kw=dict(projection=crs))
    ax.coastlines()
    ax.set_extent([-128, -62, 20, 50])
    nx.draw_networkx(sg, ax=ax,
                     font_size=16,
                     alpha=.5,
                     width=.075,
                     node_size=sizes,
                     labels=labels,
                     pos=pos,
                     node_color=altitude,
                     cmap=plt.cm.autumn)
    plt.show()
    
def draw_line(trace):
    edges=[]
    for i in range(len(trace)-1):
        edges.append([trace[i],trace[i+1]])
        
#     edges=[[ori,des]]
    edges=np.asarray(edges)
    g = nx.from_edgelist(edges)
    sg = next((g.subgraph(c) for c in nx.connected_components(g)))

    names = ('id,name,city,country,iata,icao,lat,lon,'
             'alt,timezone,dst,tz,type,source').split(',')
    airports = pd.read_csv(
        'https://github.com/ipython-books/'
        'cookbook-2nd-data/blob/master/'
        'airports.dat?raw=true',
        header=None,
        names=names,
        index_col=4,
        na_values='\\N')
    # airports_us = airports[(airports['country'] =='United States') | (
    #                         airports['country'] =="Puerto Rico")]
    airports_us = airports
    unique_index = set(airports_us.index)
    unique_index.remove(np.nan)
    airports_us_index = airports_us.index.isin(unique_index)
    airports_us = airports_us[airports_us_index]
    pos={}
    for loc in trace:
        pos[loc]=(airports_us.to_dict('index')[loc]['lon'],airports_us.to_dict('index')[loc]['lat'])
#     pos[des]=(airports_us.to_dict('index')[des]['lon'],airports_us.to_dict('index')[des]['lat'])
    
    deg = nx.degree(sg)
    sizes = [5 * deg[iata] for iata in sg.nodes]
    altitude = airports_us['alt']
    altitude = [altitude[iata] for iata in sg.nodes]
    labels = {iata: iata
              for iata in sg.nodes}
    crs = ccrs.PlateCarree()
    fig, ax = plt.subplots(
        1, 1, figsize=(12, 8),
        subplot_kw=dict(projection=crs))
    ax.coastlines()
    # Extent of continental US.
    ax.set_extent([-128, -62, 20, 50])
    nx.draw_networkx(sg, ax=ax,
                     font_size=15,
                     width=.75,
                     node_size=sizes,
                     labels=labels,
                     pos=pos,
                     alpha=None,
                     node_color=altitude,
                     edge_color="red",
                     font_color='blue',
                     cmap=plt.cm.autumn
                    )
    plt.show()
