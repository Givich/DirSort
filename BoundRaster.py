# -*- coding: utf-8 -*-
"""
Created on 09.09.2015 15:35

@author: RSA
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image
from xml.dom.minidom import parseString
import math

Image.MAX_IMAGE_PIXELS = None
fileName = u"Z:/SiteliteIMG/Ленобл_Ресурс-П/2/0041_0102_10061_1_00083_02_10_003.tif"
fileNameXML = u"Z:/SiteliteIMG/Ленобл_Ресурс-П/2/0041_0102_10061_1_00083_02_10_003.xml"

im = Image.open(fileName,'r')


(x,y) = im.size
print x, y

westPointList =[]
eastPointList =[]
northPointList =[]
southPointList =[]

for j in range(y):
    px = im.getpixel((0,j))
    if px != 0:
        westPointList.append((0,j))

print(westPointList)

for j in range(y):
    px = im.getpixel((x-1,j))
    if px != 0:
        eastPointList.append((x-1,j))

print(eastPointList)

for i in range(x):
    px = im.getpixel((i,0))
    if px != 0:
        northPointList.append((i,0))

print(northPointList)

for i in range(x):
    px = im.getpixel((i,y-1))
    if px != 0:
        southPointList.append((i,y-1))

print(southPointList)

'''For Test'''
def convert_Cord(cord):

    newCord = float(cord[0:2]) + (float(cord[3:5]))/60 + (float(cord[6:15]))/3600

    return newCord

#-38317,714896928 , 38037,2854839695

def get_Cord(fileName):

    file = open(fileName)
    data = file.read()
    file.close()
    dom = parseString(data)

    #Cordinats Tag

    latNW_Tag = dom.getElementsByTagName('aNWLat')[0].toxml()
    lonNW_Tag = dom.getElementsByTagName('aNWLong')[0].toxml()
    latNE_Tag = dom.getElementsByTagName('aNELat')[0].toxml()
    lonNE_Tag = dom.getElementsByTagName('aNELong')[0].toxml()
    latSE_Tag = dom.getElementsByTagName('aSELat')[0].toxml()
    lonSE_Tag = dom.getElementsByTagName('aSELong')[0].toxml()
    latSW_Tag = dom.getElementsByTagName('aSWLat')[0].toxml()
    lonSW_Tag = dom.getElementsByTagName('aSWLong')[0].toxml()

    #Cordinates

    latNW = convert_Cord(latNW_Tag.replace('<aNWLat>','').replace('</aNWLat>',''))
    lonNW = convert_Cord(lonNW_Tag.replace('<aNWLong>','').replace('</aNWLong>',''))
    latNE = convert_Cord(latNE_Tag.replace('<aNELat>','').replace('</aNELat>',''))
    lonNE = convert_Cord(lonNE_Tag.replace('<aNELong>','').replace('</aNELong>',''))
    latSE = convert_Cord(latSE_Tag.replace('<aSELat>','').replace('</aSELat>',''))
    lonSE = convert_Cord(lonSE_Tag.replace('<aSELong>','').replace('</aSELong>',''))
    latSW = convert_Cord(latSW_Tag.replace('<aSWLat>','').replace('</aSWLat>',''))
    lonSW = convert_Cord(lonSW_Tag.replace('<aSWLong>','').replace('</aSWLong>',''))

    listNewCord = latLong_ToMerc(latNW, lonNW) + latLong_ToMerc(latNE, lonNE) + latLong_ToMerc(latSE, lonSE) + latLong_ToMerc(latSW, lonSW)
    #listNewCord = [latNW, lonNW, latNE, lonNE, latSE, lonSE, latSW, lonSW]

    print listNewCord
    return listNewCord

def latLong_ToMerc(lat, lon):

    #Pereschev gradusov EPSG:3857
    # Formula: http://gis-lab.info/qa/dd2mercator.html

    if lat>89.5:
        lat=89.5
    if lat<-89.5:
        lat=-89.5

    rLat = math.radians(lat)
    rLong = math.radians(lon)

    a=6378137.0
    b=6378137.0
    f=(a-b)/a
    e=math.sqrt(2*f-f**2)
    x=a*rLong
    y=a*math.log(math.tan(math.pi/4+rLat/2)*((1-e*math.sin(rLat))/(1+e*math.sin(rLat)))**(e/2))
    return [x, y]

a = get_Cord(fileNameXML)

'''/For Test'''

# res1 = a[0] - a[2]
# res2 = a[4] - a[6]
# print res1
# print res2
#
# res3 = a[1] - a[3]
# res4 = a[5] - a[7]
# print res3
# print res4