import csv
import geopy.distance
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
import math
import requests
import time


def mid_pt(a, b):
    return [(a[0]+b[0])/2,  (a[1]+b[1])/2]


def PrintDistances(triangle):
    #[0,0], [1,1], [2,2]
    
    print( Haversine(triangle[0],triangle[1]).meters,    Haversine(triangle[1],triangle[2]).meters,     Haversine(triangle[0],triangle[2]).meters )

    #location of label, should be along the mid point of the

    a = mid_pt(triangle[0], triangle[1])
    plt.text(a[0],a[1],str(Haversine(triangle[0],triangle[1]).meters)+"("+ str(Haversine(triangle[0],triangle[1]).walk_time_mins)+")" )

    a = mid_pt(triangle[1], triangle[2])
    plt.text(a[0],a[1],str(Haversine(triangle[1],triangle[2]).meters)+"("+ str(Haversine(triangle[1],triangle[2]).walk_time_mins)+")"  )

    a = mid_pt(triangle[0], triangle[2])
    plt.text(a[0],a[1],str(Haversine(triangle[0],triangle[2]).meters)+"("+ str(Haversine(triangle[0],triangle[2]).walk_time_mins)+")"  )
    


class Route:
    '''
    used to store routes between points
    '''

    def __init__(self, start_name, end_name, start_pt, end_pt):
      
        self.route_walk_distance = 0
        self.route_walk_time = 0

        this_route = Haversine(start_pt,end_pt)
        self.route_distance = this_route.meters
        self.route_time = this_route.walk_time_seconds

        self.start_node=start_name
        self.end_node =end_name

        self.start_pt = start_pt
        self.end_pt = end_pt
        

    def __eq__(self, other):

        if self.start_node == other.start_node and self.end_node == other.end_node or  self.start_node == other.end_node and self.end_node ==  other.start_node:
            return True
        else:
            return False

    def __str__(self):
        
        return self.start_node + "<-->" + self.end_node


    def start_str(self):

        #return str(self.start_pt)
        return str(self.start_pt[0] ) + ","+ str(self.start_pt[1])


    def end_str(self):

        #return str(self.end_pt)
        return str(self.end_pt[0] ) + ","+ str(self.end_pt[1])

class Haversine:
    '''
    use the haversine class to calculate the distance between
    two lon/lat coordnate pairs.
    output distance available in kilometers, meters, miles, and feet.
    example usage: Haversine([lon1,lat1],[lon2,lat2]).feet
    
    '''
    def __init__(self,coord1,coord2):
        lon1,lat1=coord1
        lon2,lat2=coord2
        
        R=6371000                               # radius of Earth in meters
        phi_1=math.radians(lat1)
        phi_2=math.radians(lat2)

        delta_phi=math.radians(lat2-lat1)
        delta_lambda=math.radians(lon2-lon1)

        a=math.sin(delta_phi/2.0)**2+\
           math.cos(phi_1)*math.cos(phi_2)*\
           math.sin(delta_lambda/2.0)**2
        c=2*math.atan2(math.sqrt(a),math.sqrt(1-a))
        
        self.meters=round(R*c,0)                         # output distance in meters
        self.km=self.meters/1000.0              # output distance in kilometers
        self.miles=self.meters*0.000621371      # output distance in miles
        self.feet=self.miles*5280               # output distance in feet
        self.walk_time_hours = self.km/5.1
        self.walk_time_mins = round(self.walk_time_hours * 60,1)
        self.walk_time_seconds = self.walk_time_mins * 60



file = open("gps_locations.csv")
csvreader = csv.reader(file)
header = next(csvreader)
#print(header)
rows = []
longitude =[]
latitude = []
desc = []
points = []
loc_code =[]

for row in csvreader:
    rows.append(row)
    longitude.append(float(row[5]))
    latitude.append(float(row[4]))
    desc.append(row[1])
    loc_code.append(row[2])
    points.append([float(row[5]),float(row[4])])
                  

npts = np.array(points)

tri = Delaunay(npts)
print(tri)


print(rows)
file.close()


print(rows[0][2])





print(tri.simplices.copy())

routes =[]
sides = []

for row in tri.simplices.copy():
    #create route entries based on this row!
    print(loc_code[int(row[0])]+ "->" + loc_code[int(row[1])])

    #create the 3 routes and try and add them to the system
    
    route_a = Route( loc_code[int(row[0])],loc_code[int(row[1])], points[int(row[0])], points[int(row[1])] )
    route_b = Route( loc_code[int(row[1])],loc_code[int(row[2])], points[int(row[1])], points[int(row[2])]  )
    route_c = Route( loc_code[int(row[2])], loc_code[int(row[0])], points[int(row[2])], points[int(row[0])] )

    if route_a  not in routes:
        routes.append(route_a)


    if route_b not in routes:
        routes.append(route_b)

    if route_c not in routes:
        routes.append(route_c)

for route in routes:
    print(route)


print(len(routes), " Routes Found")

for r in routes:

    print(".", end="")


    api_url = 'https://api.openrouteservice.org/v2/directions/foot-walking?api_key=5b3ce3597851110001cf624812e9de2e87744b798dabef123f936cff&start='+r.start_str()+ "&end="+r.end_str()
    #print(api_url)
    response = requests.get(api_url)
    a = response.json()
    #print(a)
    try:
        r.route_walk_distance = a['features'][0]['properties']['summary']['distance']
        r.route_walk_time = a['features'][0]['properties']['summary']['duration']
    except:
        print(a)
    time.sleep(3)
   
# open the file in the write mode
f = open('routes.csv', 'w')

# create the csv writer

print("start_loc,end_loc,walk_distance,walk_time,distance,time", file=f)

for r in routes:
    # write a row to the csv file
    print(r.start_node, r.end_node, r.route_walk_distance, r.route_walk_time, r.route_distance, r.route_time, sep=',',file=f)

# close the file
f.close()




