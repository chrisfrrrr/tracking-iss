import ISS_Info
import turtle
import time
import threading
import math
#from mpl_toolkits.basemap import Basemap
#librerias predicciones
import urllib.request as url
import json
#import folium

import urllib.request as url
import json

from datetime import datetime, timezone

screen = turtle.Screen()
screen.title("ISS TRACKER")
screen.setup(720,360)
screen.setworldcoordinates(-180,-90,180,90)
screen.bgpic("world.png")
screen.register_shape("iss.gif")
#screen.register_shape("gt.gif")
iss = turtle.Turtle()
iss.shape("iss.gif")
iss.penup()

gt = turtle.Turtle()
#gt.shape("gt.gif")
gt.penup()

# Latitud y Logitud de Guatemala
latitud=15.783471
longitud=-90.230759
n=6 #número de veces que pasará la ISS
Pass=url.Request('http://api.open-notify.org/iss-pass.json?lat={}&lon={}&n={}'.format(latitud,longitud,n))
response_Pass= url.urlopen(Pass)

def pasoISS():
    Pass_obj = json.loads(response_Pass.read())
    #print (Pass_obj)
    pass_list=[]
    for count,item in enumerate(Pass_obj["response"], start=0):
        pass_list.append(Pass_obj['response'][count]['risetime'])
        print("Proximos pases sobre Guatemala")
        print(datetime.fromtimestamp(pass_list[count]).strftime('%d-%m-%Y %H:%M:%S'))



def tracker():
    pasoISS()
    while True:

        try:

            location = ISS_Info.iss_current_loc()
            lat = location['iss_position']['latitude']
            lon = location['iss_position']['longitude']
            screen.title("ISS TRACKER: (Latitude: {},  Longitude: {})".format(lat,lon))
            iss.goto(float(lon),float(lat))
            iss.pencolor("red")
            iss.dot(iss.goto(float(lon),float(lat)))
            gt.pencolor("orange")
            gt.dot(gt.goto(float(longitud),float(latitud)))
            time.sleep(5)
            print(float(lon),float(lat))
            az=float(math.tan((float(lat)/float(lon))))
            ro=float(math.sqrt((float(lat)**2)+((400000)**2)+((float(lon)))**2))
            print(ro,az)
        except Exception as e:
            print(str(e))
            break
t = threading.Thread(target=tracker())
t.start()
#pasoISS()
