import folium
import numpy
import random
import math

# defining the number of steps 
n = 1440 * 5

#creating two array for containing x and y coordinate 
#of size equals to the number of size and filled up with 0's 
x = numpy.zeros(n)
y = numpy.zeros(n)
locations = []
start_location=[40.4259,-86.9081]
m = folium.Map(location=start_location, zoom_start=13)
start_time = 0
map_dir = "index.html"
MINUTES_IN_DAY = 1440
times = list(range(start_time, (start_time + n)))

for i in range(len(times)):
    noise = random.randint(1,5)
    times[i] = (times[i] + noise) % MINUTES_IN_DAY
  
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


def rgb_to_hex(rgb):
    return '#' + ('%02x%02x%02x' % rgb)

def change_color_to_time():
    new_map = folium.Map(location=start_location)
    #folium.PolyLine(locations).add_to(new_map)
    for i in range(len(locations)):
        time = times[i]
        r = 255 - math.trunc(255 * (time / MINUTES_IN_DAY))
        color_tuple = (r, r, r)
        rgb = rgb_to_hex(color_tuple)
        folium.CircleMarker(location=[locations[i][0], locations[i][1]],
                            fill_color=rgb,
                            fill=True,
                            fill_opacity=1.0,
                            color="#888888").add_to(new_map)
    

    new_map.save(map_dir)

change_color_to_time()

        
