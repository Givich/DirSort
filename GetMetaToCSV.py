# -*- coding: utf-8 -*-
"""
Created on 02.09.2015 16:48

@author: Garvas
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re, csv, math
from xml.dom.minidom import parseString

targetFolder = u"Z:/SiteliteIMG/Ленобл_Ресурс-П/2/"

def find_dir(targetFolder):

    allFile = []
    ext = re.compile(r"^.+\.(?:xml)$", re.IGNORECASE + re.UNICODE)
    for root, dirs, files in os.walk(targetFolder):
        for name in files:
            if ext.match(name):
                fullname = os.path.join(root, name)
                #>>>>>>  dopilit' na proverku musora!!!
                print fullname
                allFile.append(fullname)

    print allFile
    return allFile

def getElem_XML(fileName):

    file = open(fileName)
    data = file.read()
    file.close()
    dom = parseString(data)

    #Metadata
    nameTag = dom.getElementsByTagName('cDataFileName')[0].toxml()
    timeTag = dom.getElementsByTagName('tSceneTime')[0].toxml()
    dateTag = dom.getElementsByTagName('dSceneDate')[0].toxml()
    nameKATag = dom.getElementsByTagName('cCodeKA')[0].toxml()
    deviceTag = dom.getElementsByTagName('cDeviceName')[0].toxml()
    chanalNTag = dom.getElementsByTagName('nNChannel')[0].toxml()
    resTag = dom.getElementsByTagName('nPixelImg')[0].toxml()
    cloudTag = u'1'
    sunAngTag = dom.getElementsByTagName('aAngleSum')[0].toxml()
    procLvlTag = dom.getElementsByTagName('cLevel')[0].toxml()

    #Format
    name = nameTag.replace('<cDataFileName>','').replace('</cDataFileName>','')
    date = dateTag.replace('<dSceneDate>','').replace('</dSceneDate>','').replace('/','.')
    time = timeTag.replace('<tSceneTime>','').replace('</tSceneTime>','')
    dateTime = date+' '+time[0:8]
    nameKA = nameKATag.replace('<cCodeKA>','').replace('</cCodeKA>','')
    device = deviceTag.replace('<cDeviceName>','').replace('</cDeviceName>','')
    chanalN = chanalNTag.replace('<nNChannel>','').replace('</nNChannel>','')
    chanalName = u'-'
    res = resTag.replace('<nPixelImg>','').replace('</nPixelImg>','')
    cloud = cloudTag.replace('1','0')
    sunAng = sunAngTag.replace('<aAngleSum>','').replace('</aAngleSum>','')
    procLvl = procLvlTag.replace('<cLevel>','').replace('</cLevel>','')

    conditions = u'Restriction'
    History = u'-'
    project = u'-'

    meta = dateTime + ";" + nameKA + ";" + device + ";" + chanalN + ";" + chanalName + ";" + res + ";" + cloud + ";" + sunAng + ";" +name + ";" + procLvl + ";" + conditions + ";" + History + ";" + project
    print meta
    return meta.encode('utf-8')

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

def write_CSV(listFileXML, targetFolder):

    csvfile = open(targetFolder + "\\meta.csv", "wb")
    print csvfile
    fCSV = csv.writer(csvfile, delimiter='\t')
    print fCSV
    i=1
    for fileXML in listFileXML:
        fCSV.writerow([str(i)+';' + ';' + getElem_XML(fileXML)])
        i=i+1

    csvfile.close()

    print u'Done!'

def convert_Cord(cord):

    newCord = float(cord[0:2]) + (float(cord[3:5]))/60 + (float(cord[6:15]))/3600

    return newCord

def latLong_ToMerc(lat, lon):

    #Pereschev gradusov EPSG:3857

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

"""
Fuctions
"""
listFileXML = find_dir(targetFolder)

write_CSV(listFileXML, targetFolder)

get_Cord(u'Z:/SiteliteIMG/Ленобл_Ресурс-П/2/0041_0102_10061_1_00083_02_10_003.xml')

convert_Cord(u"29:57:10.965841")
