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
at_risk = numpy.random.uniform(low=0.0, high=1.1, size=(n,))
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
                            radius=5,
                            popup="Location: " + str(locations[i][0]) + ", " + str(locations[i][1]) + "\nTime:" + str(time),
                            fill_opacity=1.0,
                            color="#888888").add_to(new_map)
    new_map.save(map_dir)
    
def change_color_to_risk():
    new_map = folium.Map(location=start_location)
    #folium.PolyLine(locations).add_to(new_map)
    for i in range(len(locations)):
        time = times[i]
        risk = math.trunc(at_risk[i])
        color_tuple = (255 * (risk), 255 * (1 - risk), 0)
        rgb = rgb_to_hex(color_tuple)
        folium.CircleMarker(location=[locations[i][0], locations[i][1]],
                            fill_color=rgb,
                            fill=True,
                            radius=5,
                            popup="Location: " + str(locations[i][0]) + ", " + str(locations[i][1]) + "\nTime:" + str(time),
                            fill_opacity=1.0,
                            color="#888888").add_to(new_map)
    new_map.save(map_dir)
def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

def change_color_to_speed():
    new_map = folium.Map(location=start_location,control_scale=True) 
    speed=0
    avewalk=0.084
 
    speeddiff=0
        
    for i in range(len(locations)):
        if i == 0:
            speed=0;
        elif (times[i]-times[i-1])==0:
            speed=0;
        else:
            coords_1 = [locations[i][0], locations[i][1]]
            coords_2 = [locations[i-1][0], locations[i-1][1]]
            distance = h3.point_dist(coords_1,coords_2)
            speed= abs(distance / (times[i]-times[i-1]))
        
        speeddiff=speed*1000/60 - 1.4
        r=clamp(100+speeddiff*300,0,255)    #grey normal, yellow fast, blue slow
        g=clamp(100+speeddiff*100,0,255)
        b=clamp(100-speeddiff*100,0,255)
        color_tuple = (int(r), int(g), int(b))
        rgb = rgb_to_hex(color_tuple)
        folium.CircleMarker(location=[locations[i][0], locations[i][1]],
                            fill_color=rgb,
                            fill=True,
                            popup="Speed: "+str(speed*1000/60)+" m/s",
                            fill_opacity=1.0,
                            color="#888888",radius=5).add_to(new_map)
        new_map.save(map_dir)

change_color_to_risk()
