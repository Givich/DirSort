# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 15:37:49 2015

@author: RSA
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re, csv
from xml.dom.minidom import parseString

targetFolder = u"Z:/SiteliteIMG/Ленобл_Ресурс-П"

def find_dir(targetFolder):

    allFile = []
    ext = re.compile(r"^.+\.(?:xml)$", re.IGNORECASE + re.UNICODE)
    for root, dirs, files in os.walk(targetFolder):
        for name in files:
            if ext.match(name):
                fullname = os.path.join(root, name)
                #print fullname
                allFile.append(fullname)

    return allFile

listFileXML = find_dir(targetFolder)

def getElem_XML(fileName):

    file = open(fileName)
    data = file.read()
    file.close()
    dom = parseString(data)

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


def write_CSV(listFileXML, targegetFolder):

    csvfile = open(targetFolder + "\\meta.csv", "wb")
    fCSV = csv.writer(csvfile, delimiter='\t')
    print fCSV
    i=1
    for fileXML in listFileXML:
        fCSV.writerow([str(i)+';' + ';' + getElem_XML(fileXML)])
        i=i+1

    csvfile.close()

    print u'Done!'

write_CSV(listFileXML, targetFolder)