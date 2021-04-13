import folium
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

# defining the number of steps 
n = 1440

#creating two array for containing x and y coordinate 
#of size equals to the number of size and filled up with 0's 
x = numpy.zeros(n)
y = numpy.zeros(n)
locations = []
start_location=[40.4259, -86.9081]
m = folium.Map(location=start_location, zoom_start=13)
at_risk = numpy.random.uniform(low=0.0, high=1.1, size=(n,))
start_time = 0
map_dir = "index.html"
MINUTES_IN_DAY = 1440
start_date = datetime.datetime.now()

times = list(range(0, n))
time_index = 0
datetimes = []


for i in range(len(times)):
    noise = random.randint(1,5)
    times[i] = (times[i] + noise)
    datetimes.append(start_date + timedelta(minutes=times[i]))

datetimeindex = pd.Series(range(0, n), index=datetimes)

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

    locations.append([x[i] + start_location[0], y[i] + start_location[1]])


ns = Namespace("dlx", "scatter")
markers = [dl.Marker(dl.Tooltip(f"({pos[0]}, {pos[1]}), time:{times[i]}"), position=pos, id="marker{}".format(i)) for i, pos in enumerate(locations)]
cluster = dl.MarkerClusterGroup(id="markers", children=markers, options={"polygonOptions": {"color": "red"}})
app = dash.Dash(external_scripts=["https://cdnjs.cloudflare.com/ajax/libs/chroma-js/2.1.0/chroma.min.js"])
app.layout = html.Div([
    dl.Map([dl.TileLayer(), cluster,
    dl.LayerGroup(id="layer")], id="map",
    center=(40.4259, -86.9081), zoom=8, style={'height': '100vh'}),
])

def rgb_to_hex(rgb):
    return ('%02x%02x%02x' % rgb)

def get_time_interval(sd, ed):
    indices = datetimeindex[sd:ed].to_numpy()
    print(indices)

def change_color_to_time():
    #folium.PolyLine(locations).add_to(new_map)
    for i in range(len(locations)):
        time = times[i]
        r = 255 - math.trunc(255 * (time / MINUTES_IN_DAY))
        color_tuple = (r, r, r)
        rgb = rgb_to_hex(color_tuple)
        icon = {
            "iconUrl": f"http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|{rgb}&chf=a,s,ee00FFFF",
            "iconSize": [20, 30],  # size of the icon
        }
        markers[i].icon = icon
    

def change_color_to_risk():
    #new_map = folium.Map(location=start_location)
    #folium.PolyLine(locations).add_to(new_map)
    for i in range(len(locations)):
        time = times[i]
        risk = math.trunc(at_risk[i])
        # color_tuple = (255 * (risk), 255 * (1 - risk), 0)
        # rgb = rgb_to_hex(color_tuple)
        
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
        markers[i].icon = icon
        print("risk")

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

def change_color_to_speed():
    new_map = folium.Map(location=start_location,control_scale=True) 
    speed=0
    avewalk=0.084
 
    speeddiff=0
        
    for i in range(len(locations)):
        if i == 0:
            speed=0
        elif (times[i]-times[i-1])==0:
            speed=0
        else:
            #coords_1 = [locations[i][0], locations[i][1]]
            #coords_2 = [locations[i-1][0], locations[i-1][1]]
            #distance = h3.point_dist(coords_1,coords_2)
            R = 6373.0
            lat1 = radians(locations[i][0])
            lon1 = radians(locations[i][1])
            lat2 = radians(locations[i-1][0])
            lon2 = radians(locations[i-1][1])
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = 2
            ##sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
            c = 2 
            ##2 * atan2(sqrt(a), sqrt(1 - a))
            distance = R * c
            speed = abs(distance / (times[i]-times[i-1]))
        
        speeddiff=speed*1000/60 - 1.4
        r=clamp(100+speeddiff*300,0,255)    #grey normal, yellow fast, blue slow
        g=clamp(100+speeddiff*100,0,255)
        b=clamp(100-speeddiff*100,0,255)
        color_tuple = (int(r), int(g), int(b))
        rgb = rgb_to_hex(color_tuple)
        icon = {
            "iconUrl": f"http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|{rgb}&chf=a,s,ee00FFFF",
            "iconSize": [20, 30],  # size of the icon
        }
        markers[i].icon = icon

#change_color_to_speed()
#get_time_interval(str(datetime.datetime.now()), str(datetime.datetime.now() + timedelta(minutes=4)))
if __name__ == '__main__':
    app.run_server()
