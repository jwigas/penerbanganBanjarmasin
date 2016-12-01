# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 10:23:14 2016

@author: lenovo 8
"""

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import csv,random
from collections import OrderedDict

#map = Basemap(projection='merc', lat_0=0, lon_0=125, \
#           resolution='l', area_thresh=0.1, \
#           llcrnrlon=94, llcrnrlat=-11, \
#           urcrnrlon=143, urcrnrlat=8)


map = Basemap(projection='merc', lat_0=0, lon_0=125, \
           resolution='l', area_thresh=0.1, \
           llcrnrlon=105, llcrnrlat=-11, \
           urcrnrlon=128, urcrnrlat=8)

filename = 'routes.csv'
maskapai = []
pembanding = ''
counter = -1
kotaTujuan = []

with open(filename) as f:
    reader = csv.reader(f)
    
    for row in reader:
        if (row[2] == "BDJ"):
            kotaTujuan.append(row[4])
            if pembanding != row[0]:
                counter = counter + 1
                pembanding = row[0]
                maskapai.append([row[0],[row[2],row[4]]])
            else:
                maskapai[counter].append([row[2],row[4]])

        else:
            None
            
#removing duplicated data
kotaTujuan= set(kotaTujuan)

#print ('maskapai',maskapai)
#print ('Kota Tujuan',kotaTujuan)

# Open the data file
filename = 'airports.csv'

# Empty list
bandara = []
kota = []
lats, lons = [],[]
IATA = []

# parsing
with open(filename) as f:
    reader = csv.reader(f)
    
    for row in reader:
        if row[4] == "BDJ":
            bandara.append(row[1])
            kota.append(row[2])
            lats.append(float(row[6]))
            lons.append(float(row[7]))
            IATA.append(row[4])
        else:
            for dest in kotaTujuan:
                if row[4] == dest:
                    bandara.append(row[1])
                    kota.append(row[2])
                    lats.append(float(row[6]))
                    lons.append(float(row[7]))
                    IATA.append(row[4])

#print ('kota',kota)
#print ('bandara',bandara)
for maskapai in maskapai:
    counter=0
    for destinasi in maskapai:
        if counter == 0:
            warna=[random.random(),random.random(),random.random()]
        else:
            map.drawgreatcircle(lons[IATA.index(destinasi[0])], lats[IATA.index(destinasi[0])], 
                                     lons[IATA.index(destinasi[1])], lats[IATA.index(destinasi[1])],
                                          linewidth=1,color=warna,label=maskapai[0])         
        counter +=1

map.drawmapboundary(fill_color='aqua')
map.bluemarble()
map.drawcoastlines()
map.drawcountries()


x, y = map(lons,lats)
map.plot(x,y,'ro',markersize=5)

#label
x_offsets = 10000
y_offsets = 5000

for kota, xpt, ypt in zip(kota, x, y):
    if kota == 'Banjarmasin':
        print("Banjarmasin Detected")
        plt.text(xpt+x_offsets, ypt-50000, kota, fontsize=9, color='yellow')
    else:
        plt.text(xpt+x_offsets, ypt+y_offsets, kota, fontsize=9, color='yellow')

#draw province boundaries
#map.readshapefile('IDN_adm/IDN_adm1', 'IDN_adm1', drawbounds = False)
#for info, shape in zip(map.IDN_adm1_info, map.IDN_adm1):
#    x, y = zip(*shape) 
#    map.plot(x, y, marker=None,color='m')

#title_string = "Flug von Banjarmasin\n"
#title_string += "Served by Lion Air"
#plt.title(title_string.decode('utf-8'))

###removing any duplicated labels
handles, labels = plt.gca().get_legend_handles_labels()
by_label = OrderedDict(zip(labels, handles))

leg = plt.legend(by_label.values(), by_label.keys(),bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

# set the linewidth of each legend object
for legobj in leg.legendHandles:
    legobj.set_linewidth(4.0)


plt.show()