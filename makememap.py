import numpy
import random
import math
from math import *
import h3
import datetime
from datetime import timedelta
import pandas as pd
import dash
import dash_html_components as html
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.javascript import Namespace
from dash.dependencies import Input, Output
import os
import threading
MINUTES_IN_DAY = 1440

class Map:
    def __init__(self, n):
        self.markers = []
        self.times = []
        self.at_risk = []
        # defining the number of steps
        self.n = 1440
        self.create_markers(self.n)
        self.create_map()
        self.color_scheme = 'T'
        self.start = 0
        self.end = self.n - 1
        self.change_color_to_time()
        self.ispoly = True
        thread = threading.Thread(target=self.run)
        thread.start()
        
    def run(self):
        self.app.run_server(port=8080)

    def create_markers(self, n):
        #creating two array for containing x and y coordinate 
        #of size equals to the number of size and filled up with 0's 
        x = numpy.zeros(n)
        y = numpy.zeros(n)
        self.locations = []
        start_location=[40.4259, -86.9081]
        self.at_risk = numpy.random.uniform(low=0.0, high=1.1, size=(n,))
        self.start_time = 0
        self.map_dir = "index.html"
        self.start_date = datetime.datetime.now()
        self.times = list(range(0, n))
        time_index = 0
        self.datetimes = []

        for i in range(len(self.times)):
            noise = random.randint(1,5)
            self.times[i] = (self.times[i] + noise)
            self.datetimes.append(self.start_date + timedelta(minutes=self.times[i]))

        self.datetimeindex = pd.Series(range(0, n), index=self.datetimes)

        # filling the coordinates with random variables 
        for i in range(1, n): 
            val = random.randint(1, 4) 
            if val == 1: 
                x[i] = x[i - 1] + 0.001
                y[i] = y[i - 1] 
            elif val == 2: 
                x[i] = x[i - 1] - 0.001
                y[i] = y[i - 1] 
            elif val == 3: 
                x[i] = x[i - 1] 
                y[i] = y[i - 1] + 0.001
            else: 
                x[i] = x[i - 1] 
                y[i] = y[i - 1] - 0.001

            self.locations.append([x[i] + start_location[0], y[i] + start_location[1]])

    def create_map(self):
        self.ns = Namespace("dlx", "scatter")
        self.markers = [dl.Marker(dl.Tooltip(f"({pos[0]}, {pos[1]}), time:{self.times[i]}"), position=pos, id="marker{}".format(i)) for i, pos in enumerate(self.locations)]
        self.cluster = dl.MarkerClusterGroup(id="markers", children=self.markers, options={"polygonOptions": {"color": "red"}})
        self.app = dash.Dash(external_scripts=["https://cdnjs.cloudflare.com/ajax/libs/chroma-js/2.1.0/chroma.min.js"])
        self.polyline = dl.Polyline(positions=self.locations)
        self.app.layout = html.Div([
            dl.Map([
                dl.TileLayer(),
                self.cluster,
                self.polyline,
                dl.LayerGroup(id="layer")],
            id="map",
            center=(40.4259, -86.9081), zoom=8, style={'height': '100vh'}),
        ])
        # print(type(self.app.layout))
        # @self.app.callback(Output('id_marker_pattern','children'), [Input('interval','n_intervals')])
        # def update_polyline(b):
        #     if (self.ispoly == True):
        #         polyline = dl.Polyline(positions=self.locations)
        #     else:
        #         polyline = None
        #     return polyline

        # @self.app.callback(Output('new_markers','children'), [Input('interval', 'n_intervals')])
        # def update_metrics(a):
        #     self.locations.append([locations_base[a][0], locations_base[a][1]])
        #     if(len(self.locations) >= 100):
        #         self.locations.pop(0)
        #     new_markers = [dl.Marker(dl.Tooltip(f"({pos[0]}, {pos[1]}), time:{times[i]}"), position=pos, id="marker{}".format(i)) for i, pos in enumerate(self.locations)]
        #     return new_markers


    def rgb_to_hex(self, rgb):
        return ('%02x%02x%02x' % rgb)

    def get_time_interval(self, sd, ed):
        indices = self.datetimeindex[sd:ed].to_numpy()

    def change_color_to_time(self):
        self.color_scheme = 'T'
        for i in range(self.start, self.end, 1):
            time = self.times[i]
            r = 255 - math.trunc(255 * (time / MINUTES_IN_DAY))
            color_tuple = (r, r, r)
            rgb = self.rgb_to_hex(color_tuple)
            icon = {
                "iconUrl": f"http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|{rgb}&chf=a,s,ee00FFFF",
                "iconSize": [20, 30],  # size of the icon
            }
            self.markers[i].icon = icon

    def change_color_to_risk(self):
        self.color_scheme = 'R'
        for i in range(self.start, self.end, 1):
            time = self.times[i]
            risk = math.trunc(self.at_risk[i])

            if (risk == 1):
                icon = {
                    "iconUrl": "http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|FF0000&chf=a,s,ee00FFFF",
                    "iconSize": [20, 30],  # size of the icon
                }
            else:
                icon = {
                    "iconUrl": "http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|00FF00&chf=a,s,ee00FFFF",
                    "iconSize": [20, 30],  # size of the icon
                }
            self.markers[i].icon = icon

    def clamp(self, n, minn, maxn):
        return max(min(maxn, n), minn)

    def change_color_to_speed(self):
        self.color_scheme = 'S'
        speed=0
        avewalk=0.084
        speeddiff=0
            
        for i in range(self.start, self.end):
            if i == 0:
                speed=0
            elif (self.times[i]-self.times[i-1])==0:
                speed=0
            else:
                #coords_1 = [locations[i][0], locations[i][1]]
                #coords_2 = [locations[i-1][0], locations[i-1][1]]
                #distance = h3.point_dist(coords_1,coords_2)
                R = 6373.0
                lat1 = radians(self.locations[i][0])
                lon1 = radians(self.locations[i][1])
                lat2 = radians(self.locations[i-1][0])
                lon2 = radians(self.locations[i-1][1])
                dlon = lon2 - lon1
                dlat = lat2 - lat1
                a = 2
                ##sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
                c = 2 
                ##2 * atan2(sqrt(a), sqrt(1 - a))
                distance = R * c
                speed = abs(distance / (self.times[i]-self.times[i-1]))
            
            speeddiff=speed*1000/60 - 1.4
            r=self.clamp(100+speeddiff*300,0,255)    #grey normal, yellow fast, blue slow
            g=self.clamp(100+speeddiff*100,0,255)
            b=self.clamp(100-speeddiff*100,0,255)
            color_tuple = (int(r), int(g), int(b))
            rgb = self.rgb_to_hex(color_tuple)
            icon = {
                "iconUrl": f"http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|{rgb}&chf=a,s,ee00FFFF",
                "iconSize": [20, 30],  # size of the icon
            }
            self.markers[i].icon = icon
