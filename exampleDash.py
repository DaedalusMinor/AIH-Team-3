import random
import numpy
import math
import dash
import dash_html_components as html
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.javascript import Namespace
from dash.dependencies import Input, Output

n = 1440 * 5
x = numpy.zeros(n)
y = numpy.zeros(n)
start_location=[40.4259,-86.9081]
locations=dict()
locations['lon'] = []
locations['lat'] = []

#for i in range(1, n): 
def genwalk(i):
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

    #locations['lon'].append([x[i] + start_location[0]])
    #locations['lat'].append([y[i] + start_location[1]])
    return [x[i] , y[i]]

# Create some markers.
points = [dict(lat=40.4259 + genwalk(i)[0], lon=-86.9081 + genwalk(i)[1], value=random.random()) for i in range(n)]
#points = locations
data = dlx.dicts_to_geojson(points)  
# Create geojson.
ns = Namespace("dlx", "scatter")
#geojson = dl.GeoJSON(data=data, cluster=True, options=dict(pointToLayer=ns("pointToLayer")))
geojson = dl.GeoJSON(data=data, options=dict(pointToLayer=ns("pointToLayer")), cluster=True, hideout=dict(colorscale=['#088F8F']))
# Create the app.
app = dash.Dash(external_scripts=["https://cdnjs.cloudflare.com/ajax/libs/chroma-js/2.1.0/chroma.min.js"])
app.layout = html.Div([
    dl.Map([dl.TileLayer(),
    geojson, dl.LayerGroup(id="layer")], id="map",
    center=(40.4259, -86.9081), zoom=8, style={'height': '50vh'}),
])

# Add map click event.
# once click the map, there will be a pin on the map shows the coordinates of the pin.
@app.callback(Output("layer", "children"), [Input("map", "click_lat_lng")])
def map_click(click_lat_lng):
    return [dl.Marker(position=click_lat_lng, children=dl.Tooltip("({:.3f}, {:.3f})".format(*click_lat_lng)))]

if __name__ == '__main__':
    app.run_server()
