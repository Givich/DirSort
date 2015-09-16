# -*- coding: utf-8 -*-
"""
Created on 02.09.2015 16:48

@author: Garvas
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import re
import csv
import math
import shapefile #https://github.com/GeospatialPython/pyshp
from xml.dom.minidom import parseString
from osgeo import ogr
from osgeo import osr
from osgeo import gdal
import psycopg2

Folder = u"C:\\Users\\RSA\\Documents\\07.08.2015\\5383-РП_Ленинградская обл_геотон_КШМСА_ВР\\293610_Всеволжский район_геотон"
targetFolder = os.path.normpath(Folder)


def find_dir(targetFolder):
    """
    Find for all files in a directory corresponding to the regular expression
    :param targetFolder: directory
    :return: list of the absolute filenames
    """
    allFile = []
    ext = re.compile(r"^.+\.(?:xml)$", re.IGNORECASE + re.UNICODE)
    #unExt = re.compile(r"^.+\.(?:aux.xml)$", re.IGNORECASE + re.UNICODE)
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
    """
    Selects the data from the XML related tags
    :param fileName: absolute filename
    :return: String with parameters separated by semicolons (UTF-8)
    """
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
    sunAngTag = dom.getElementsByTagName('aSunElevC')[0].toxml()
    procLvlTag = dom.getElementsByTagName('cLevel')[0].toxml()

    #Format
    name = nameTag.replace('<cDataFileName>','').replace('</cDataFileName>','')
    date = dateTag.replace('<dSceneDate>','').replace('</dSceneDate>','').replace('/','-')
    time = timeTag.replace('<tSceneTime>','').replace('</tSceneTime>','')
    dateTime = date + ' ' + time[0:8]
    nameKA = nameKATag.replace('<cCodeKA>','').replace('</cCodeKA>','')
    device = deviceTag.replace('<cDeviceName>','').replace('</cDeviceName>','')
    chanalN = chanalNTag.replace('<nNChannel>','').replace('</nNChannel>','')
    chanalName = u'-'
    res = resTag.replace('<nPixelImg>','').replace('</nPixelImg>','')
    cloud = cloudTag.replace('1','0')
    sunAng = sunAngTag.replace('<aSunElevC>','').replace('</aSunElevC>','')

    procLvl = "3"
    #procLvl = procLvlTag.replace('<cLevel>','').replace('</cLevel>','')

    degSunAng = str(convert_Cord(sunAng))

    conditions = u'Restriction'
    History = u'-'
    project = u'-'

    meta = dateTime + ";" + nameKA + ";" + device + ";" + chanalN + ";" + chanalName + ";" + res + ";" + cloud + ";" + degSunAng + ";" +name + ";" + procLvl + ";" + conditions + ";" + History + ";" + project
    print meta
    return meta.encode('utf-8')

def get_Cord(fileName):
    """
    From XML Select is selected coordinates of the corners
    :param fileName: absolute filename
    :return: List of coordinates in the projection EPSG: 3857
    """

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
    """
    The function creates a file "meta.csv" in the root folder, which stores all metadata
    Calls the extraction coordinate and create a shapefile
    :param listFileXML: List absolute filename
    :param targetFolder: Directory
    :return: NONE! Print "Done!"
    """
    csvfile = open(targetFolder + "\\meta.csv", "wb")
    print csvfile
    fCSV = csv.writer(csvfile, delimiter='\t')
    print fCSV
    i=1
    for fileXML in listFileXML:
        tmp = [str(i)+';1' + ';' + getElem_XML(fileXML)]
        fCSV.writerow(tmp)
        lstMeta = tmp[0].split(';')
        i=i+1
        lstCord = get_Cord(fileXML)
        create_Shape(lstCord,lstMeta)
        bound_raster(fileXML, lstMeta)

    csvfile.close()

    print u'Done!'


def convert_Cord(cord):
    """
    Converts coordinates from format DD:MM:SS.SSSSS to format DD.DDDDDD
    :param cord: coordinate DD:MM:SS.SSSSS
    :return: coordinate DD.DDDDDD
    """
    newCord = float(cord[0:2]) + (float(cord[3:5]))/60 + (float(cord[6:15]))/3600

    return newCord

def latLong_ToMerc(lat, lon):
    """
    Recounts the latitude-longitude to Mercator (EPSG: 3857)
    # Formula: http://gis-lab.info/qa/dd2mercator.html
    :param lat: coordinate latitude
    :param lon: coordinate longitude
    :return: List of the two coordinates for a single point
    """

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

def create_Shape(listCord, listMeta):
    """
    Creates a vector file format SHP.
    Creates a folder in path of where to put all the files with the names of duplicate names image files
    :param listCord: Coordinate list
    :param listMeta: List of metadata
    :return: NONE! Only print, that all good :)
    """

    b = listMeta # For short, later removed
    w = shapefile.Writer(shapefile.POLYGON)
    w.poly(shapeType=5, parts=[[[listCord[0],listCord[1]], [listCord[2],listCord[3]], [listCord[4],listCord[5]],[listCord[6],listCord[7]]]])

    """Create fields. Need rename and may be add attributes"""
    w.field('a1')
    w.field('a2')
    w.field('a3')
    w.field('a4')
    w.field('a5')
    w.field('a6')
    w.field('a7')
    w.field('a8')
    w.field('a9')
    w.field('a10')
    w.field('a11')
    w.field('a12')
    w.field('a13')
    w.field('a14')
    w.field('a15')

    w.record(a1=b[0], a2=b[1], a3=b[2], a4=b[3], a5=b[4], a6=b[5], a7=b[6], a8=b[7], a9=b[8], a10=b[9], a11=b[10], a12=b[11], a13=b[12], a14=b[13], a15=b[14])

    w.save(targetFolder + "//shapefiles//" + b[10].replace('.tiff','').replace('.tif',''))

    print u"File recorded to: "+targetFolder+u"/shapefiles/"


def bound_raster(fileNameXML, listMeta):
    """
    Try open file TIFF or TIF file, if its imposible write ERROR
    If file have not metadata sys.exit(1)
    When this function is done, it will be cut to form a new shapefile,
    by calculating the intersection of the outline of the image formed from the shapefile and metadata.
    Yes, they do not match!
    Create new shapefile by ogr tools
    :param fileNameXML: name XML file
    :param listMeta: list of metadata for this file
    :return: NONE!
    """

    try:
        try:
            fileName = fileNameXML.replace('.xml','.tiff')
            # open dataset
            dataset = gdal.Open(fileName)
            print u'Драйвер: ', dataset.GetDriver().ShortName, u'/', dataset.GetDriver().LongName
            print u'Размер ',dataset.RasterXSize, u'x', dataset.RasterYSize, u'x', dataset.RasterCount
            print u'Проекция ', dataset.GetProjection()
            geotransform = dataset.GetGeoTransform()
            if not geotransform is None:
                print u'Начало координат (',geotransform[0], u',',geotransform[3],u')'
                print u'Размер пиксела = (',geotransform[1], u',',geotransform[5],u')'

        except:
            fileName = fileNameXML.replace('.xml','.tif')
            # open dataset
            dataset = gdal.Open(fileName)
            print u'Драйвер: ', dataset.GetDriver().ShortName, u'/', dataset.GetDriver().LongName
            print u'Размер ',dataset.RasterXSize, u'x', dataset.RasterYSize, u'x', dataset.RasterCount
            print u'Проекция ', dataset.GetProjection()
            geotransform = dataset.GetGeoTransform()
            if not geotransform is None:
                print u'Начало координат (',geotransform[0], u',',geotransform[3],u')'
                print u'Размер пиксела = (',geotransform[1], u',',geotransform[5],u')'


    except:
        print u"Error file format"
        sys.exit(1)


    if not geotransform[0]==0:
        if not geotransform[3]==0:
            # Get cord of corners for points shapefiles
            newXA = geotransform[0]
            newYA = geotransform[3]
            print newXA, newYA


            newXB = geotransform[0] + dataset.RasterXSize*geotransform[1]
            newYB = geotransform[3]
            print newXB, newYB

            newXC = geotransform[0] + dataset.RasterXSize*geotransform[1]
            newYC = geotransform[3] + dataset.RasterYSize*geotransform[5]
            print newXC, newYC

            newXD = geotransform[0]
            newYD = geotransform[3] + dataset.RasterYSize*geotransform[5]
            print newXD, newYD

            # Create ring from points corner raster
            ring = ogr.Geometry(ogr.wkbLinearRing)
            ring.AddPoint_2D(newXA, newYA)
            ring.AddPoint_2D(newXB, newYB)
            ring.AddPoint_2D(newXC, newYC)
            ring.AddPoint_2D(newXD, newYD)
            ring.AddPoint_2D(newXA, newYA)

            # Create polygon
            poly = ogr.Geometry(ogr.wkbPolygon)
            poly.AddGeometry(ring)

            print poly.ExportToWkt()


            file = open(fileNameXML)
            data = file.read()
            file.close()
            dom = parseString(data)

            # Cordinats Tag. Check coord system
            coordCodeTag = dom.getElementsByTagName('nCoordSystCode')[0].toxml()
            coordCode = coordCodeTag.replace('<nCoordSystCode>','').replace('</nCoordSystCode>','')

            # Change prjection FROM
            source = osr.SpatialReference() #https://pcjericks.github.io/py-gdalogr-cookbook/projection.html#reproject-a-geometry
            source.ImportFromEPSG(int(coordCode))

            # Change prjection TO
            target = osr.SpatialReference()
            target.ImportFromEPSG(3857)

            transform = osr.CoordinateTransformation(source, target)

            poly.Transform(transform)
            print poly.ExportToWkt()
            print u"POLY:",poly
            #-----------------------------------------------------------------------

            (head, tail) = os.path.split(fileNameXML)
            print tail

            # Get a Layer's Extent
            inShapefile = targetFolder + "/shapefiles/" + tail.replace('.xml', '.shp')
            print inShapefile
            inDriver = ogr.GetDriverByName("ESRI Shapefile")
            inDataSource = inDriver.Open(inShapefile, 0)
            inLayer = inDataSource.GetLayer()
            for feature in inLayer:
                geom = feature.GetGeometryRef()
                print u"InSHP>>:"+geom.ExportToWkt()

            layerSpaFil = geom.Intersection(poly)

            print u"RESULT:",layerSpaFil.ExportToWkt()

            # Save to a new Shapefile
            outShapefile = targetFolder + "/shapefiles//" + tail.replace('.xml', '_c.shp')
            print outShapefile
            outDriver = ogr.GetDriverByName("ESRI Shapefile")

            # Remove output shapefile if it already exists
            if os.path.exists(outShapefile):
                outDriver.DeleteDataSource(outShapefile)

            outDataSource = outDriver.CreateDataSource(outShapefile)
            outLayer = outDataSource.CreateLayer("spatial", geom_type=ogr.wkbPolygon)

            # Add fields (create with ogr type)
            outLayer.CreateField(ogr.FieldDefn("ogc_fid", ogr.OFTInteger))
            outLayer.CreateField(ogr.FieldDefn("id", ogr.OFTInteger))
            outLayer.CreateField(ogr.FieldDefn("session_ti", ogr.OFTString))
            outLayer.CreateField(ogr.FieldDefn("ka", ogr.OFTString))
            outLayer.CreateField(ogr.FieldDefn("device", ogr.OFTString))
            outLayer.CreateField(ogr.FieldDefn("channels_c", ogr.OFTInteger))
            outLayer.CreateField(ogr.FieldDefn("channels", ogr.OFTString))
            outLayer.CreateField(ogr.FieldDefn("resolution", ogr.OFTReal))
            outLayer.CreateField(ogr.FieldDefn("cloud_cove", ogr.OFTInteger))
            outLayer.CreateField(ogr.FieldDefn("sun_angle", ogr.OFTString))
            outLayer.CreateField(ogr.FieldDefn("name", ogr.OFTString))
            outLayer.CreateField(ogr.FieldDefn("proc_level", ogr.OFTString))
            outLayer.CreateField(ogr.FieldDefn("conditions", ogr.OFTString))
            outLayer.CreateField(ogr.FieldDefn("history_or", ogr.OFTString))
            outLayer.CreateField(ogr.FieldDefn("projects_c", ogr.OFTString))

            featureDefn = outLayer.GetLayerDefn()
            feature = ogr.Feature(featureDefn)

            #add data
            feature.SetField("ogc_fid", listMeta[0])
            feature.SetField("id", listMeta[1])
            feature.SetField("session_ti", listMeta[2])
            feature.SetField("ka", listMeta[3])
            feature.SetField("device", listMeta[4])
            feature.SetField("channels_c", listMeta[5])
            feature.SetField("channels", listMeta[6])
            feature.SetField("resolution", listMeta[7])
            feature.SetField("cloud_cove", listMeta[8])
            feature.SetField("sun_angle", listMeta[9])
            feature.SetField("name", listMeta[10])
            feature.SetField("proc_level", listMeta[11])
            feature.SetField("conditions", listMeta[12])
            feature.SetField("history_or", listMeta[13])
            feature.SetField("projects_c", listMeta[14])

            feature.SetGeometry(layerSpaFil)
            outLayer.CreateFeature(feature)

            geo = layerSpaFil.ExportToWkt()
            print u">>>> "+geo

            # dbData = parce_db_data (u"D:\SUAI\PyCharm\BD_spiiras.xml")
            # print "dbname="+dbData[0]+" host=:"+dbData[1]+" port="+dbData[2]+" user="+dbData[3]+" password="+dbData[4]
            #
            # try:
            #     conn = psycopg2.connect("dbname="+dbData[0]+" host="+dbData[1]+" port="+dbData[2]+" user="+dbData[3]+"password="+dbData[4])
            #     print u"connecting is OK!"
            # except:
            #     print "I am unable to connect to the database"
            #     sys.exit(1)
            #
            # cur = conn.cursor()
            #
            # sql = '''INSERT INTO public.spc_vector_contur (geom, ogc_fid, id, session_ti, ka, device, channels_c, channels, resolution, cloud_cove, sun_angle, name, proc_level, conditions, history_or, projects_c) VALUES (ST_GeomFromText(%s, 3857), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            # param = [geo, listMeta[0], listMeta[1], listMeta[2], listMeta[3], listMeta[4], listMeta[5], listMeta[6], listMeta[7], listMeta[8], listMeta[9], listMeta[10], listMeta[11], listMeta[12], listMeta[13], listMeta[14]]
            # print param
            #
            # cur.execute(sql, param)
            # conn.commit()
            #
            # cur.close()
            # conn.close()

            feature.Destroy()
            inDataSource.Destroy()

dbFile = u"D:\SUAI\PyCharm\BD_spiiras.xml"

def parce_db_data (dbFile):

    file = open(dbFile)
    data = file.read()
    file.close()
    dom = parseString(data)

    listDbData = []

    # DB data
    name = (dom.getElementsByTagName('NameBD')[0].toxml()).replace('<NameBD>',"'").replace('</NameBD>',"'")
    listDbData.append(name)
    host = (dom.getElementsByTagName('Host')[0].toxml()).replace('<Host>',"'").replace('</Host>',"'")
    listDbData.append(host)
    port = (dom.getElementsByTagName('Port')[0].toxml()).replace('<Port>',"'").replace('</Port>',"'")
    listDbData.append(port)
    user = (dom.getElementsByTagName('User')[0].toxml()).replace('<User>',"'").replace('</User>',"'")
    listDbData.append(user)
    passw = (dom.getElementsByTagName('Pass')[0].toxml()).replace('<Pass>',"'").replace('</Pass>',"'")
    listDbData.append(passw)

    return listDbData


"""
Fuctions
"""

# if __name__ == '__main__':
#     args = sys.argv[ 1: ]
#     inPath = args[ 0 ]
#     outPath = args[ 1 ]
#     print inPath,u"dfgdf",outPath

listFileXML = find_dir(targetFolder)
write_CSV(listFileXML, targetFolder)

#get_Cord(u'Z:/SiteliteIMG/Ленобл_Ресурс-П/2/0041_0102_10061_1_00083_02_10_003.xml')

#convert_Cord(u"29:57:10.965841")
