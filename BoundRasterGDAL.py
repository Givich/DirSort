# -*- coding: utf-8 -*-
"""
Created on 09.09.2015 21:22

@author: Garvas
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
from osgeo import ogr
from osgeo import osr
from osgeo import gdal
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
fileName = u"Z:/SiteliteIMG/293623_Приозерский район, Раздольевское сельское поселение_КШМСА_ВР/fr_0042_0102_02150_1_02143_02_G_40_6.tiff"



# open dataset
dataset = gdal.Open(fileName)

print u'Драйвер: ', dataset.GetDriver().ShortName, u'/', dataset.GetDriver().LongName
print u'Размер ',dataset.RasterXSize, u'x', dataset.RasterYSize, u'x', dataset.RasterCount
print u'Проекция ', dataset.GetProjection()

geotransform = dataset.GetGeoTransform()
if not geotransform is None:
    print u'Начало координат (',geotransform[0], u',',geotransform[3],u')'
    print u'Размер пиксела = (',geotransform[1], u',',geotransform[5],u')'



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




# source = osr.SpatialReference() #https://pcjericks.github.io/py-gdalogr-cookbook/projection.html#reproject-a-geometry
# source.ImportFromEPSG(32635)
#
# target = osr.SpatialReference()
# target.ImportFromEPSG(3857)
#
# transform = osr.CoordinateTransformation(source, target)
#
# point = ogr.CreateGeometryFromWkt("POINT (652787.03736 6726699.89956)")
# point.Transform(transform)
#
# print point.ExportToWkt()

pointList = southPointList

firstPoint = pointList[0]
lastPoint = pointList[len(pointList)-1]
(a,b) = firstPoint
(c,d) = lastPoint

newA = geotransform[0] + a * geotransform[1]
newB = geotransform[3] + b * geotransform[1]
newC = geotransform[0] + c * geotransform[1]
newD = geotransform[3] + d * geotransform[1]


source = osr.SpatialReference() #https://pcjericks.github.io/py-gdalogr-cookbook/projection.html#reproject-a-geometry
source.ImportFromEPSG(32635)

target = osr.SpatialReference()
target.ImportFromEPSG(3857)

transform = osr.CoordinateTransformation(source, target)

point1 = ogr.CreateGeometryFromWkt("POINT"+" ("+str(newA)+" "+str(newB)+")")
point1.Transform(transform)

bb = point1.ExportToWkt()
print bb

point2 = ogr.CreateGeometryFromWkt("POINT"+" ("+str(newC)+" "+str(newD)+")")
point2.Transform(transform)

print point2.ExportToWkt()



