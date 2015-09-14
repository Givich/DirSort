# -*- coding: utf-8 -*-
"""
Created on 09.09.2015 21:22

@author: Garvas
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
from osgeo import ogr
from osgeo import gdal
import os

fileName = u"Z:/SiteliteIMG/Ленобл_Ресурс-П/4/0041_0102_10061_1_00083_02_10_007.tif"

"""
When this function is done, it will be cut to form a new shapefile,
by calculating the intersection of the outline of the image formed from the shapefile and metadata.
Yes, they do not match!
"""

# open dataset
dataset = gdal.Open(fileName)

print u'Драйвер: ', dataset.GetDriver().ShortName, u'/', dataset.GetDriver().LongName
print u'Размер ',dataset.RasterXSize, u'x', dataset.RasterYSize, u'x', dataset.RasterCount
print u'Проекция ', dataset.GetProjection()

geotransform = dataset.GetGeoTransform()
if not geotransform is None:
    print u'Начало координат (',geotransform[0], u',',geotransform[3],u')'
    print u'Размер пиксела = (',geotransform[1], u',',geotransform[5],u')'

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
        ring.AddPoint(newXA, newYA)
        ring.AddPoint(newXB, newYB)
        ring.AddPoint(newXC, newYC)
        ring.AddPoint(newXD, newYD)
        ring.AddPoint(newXA, newYA)

        # Create polygon
        poly = ogr.Geometry(ogr.wkbPolygon)
        poly.AddGeometry(ring)

        print poly.ExportToWkt()

        # Change prjection FROM
        source = osr.SpatialReference() #https://pcjericks.github.io/py-gdalogr-cookbook/projection.html#reproject-a-geometry
        source.ImportFromEPSG(32635)

        # Change prjection TO
        target = osr.SpatialReference()
        target.ImportFromEPSG(3857)

        transform = osr.CoordinateTransformation(source, target)

        poly.Transform(transform)
        print poly.ExportToWkt()
        print u"POLY:",poly
        #-----------------------------------------------------------------------

        # Get a Layer's Extent
        inShapefile = u"Z:/SiteliteIMG/Ленобл_Ресурс-П/shapefiles/0041_0102_10061_1_00083_02_10_007.shp"
        inDriver = ogr.GetDriverByName("ESRI Shapefile")
        inDataSource = inDriver.Open(inShapefile, 0)
        inLayer = inDataSource.GetLayer()
        for feature in inLayer:
            geom = feature.GetGeometryRef()
            print geom.ExportToWkt()

        layerSpaFil = geom.Intersection(poly)

        print u"RESULT:",layerSpaFil.ExportToWkt()

        # Save to a new Shapefile
        outShapefile = u"Z:/SiteliteIMG/293623_Приозерский район, Раздольевское сельское поселение_КШМСА_ВР/shapefiles/fr_0042_0102_02150_1_02143_02_G_40_6_test.shp"
        outDriver = ogr.GetDriverByName("ESRI Shapefile")

        # Remove output shapefile if it already exists
        if os.path.exists(outShapefile):
            outDriver.DeleteDataSource(outShapefile)

        outDataSource = outDriver.CreateDataSource(outShapefile)
        outLayer = outDataSource.CreateLayer("spatial", geom_type=ogr.wkbPolygon)


        featureDefn = outLayer.GetLayerDefn()
        feature = ogr.Feature(featureDefn)
        # #feature.SetField("id", 1)
        feature.SetGeometry(layerSpaFil)
        outLayer.CreateFeature(feature)

#wkt = "POLYGON ((-103.81402655265633 50.253951270672125,-102.94583419409656 51.535568561879401,-100.34125711841725 51.328856095555651,-100.34125711841725 51.328856095555651,-93.437060743203844 50.460663736995883,-93.767800689321859 46.450441890315041,-94.635993047881612 41.613370178339181,-100.75468205106476 41.365315218750681,-106.12920617548238 42.564247523428456,-105.96383620242338 47.277291755610058,-103.81402655265633 50.253951270672125))"



# im = Image.open(fileName,'r')
#
# (x,y) = im.size
# print x, y
#
# westPointList =[]
# eastPointList =[]
# northPointList =[]
# southPointList =[]
#
# for j in range(y):
#     px = im.getpixel((0,j))
#     if px != 0:
#         westPointList.append((0,j))
#
# print(westPointList)
#
# for j in range(y):
#     px = im.getpixel((x-1,j))
#     if px != 0:
#         eastPointList.append((x-1,j))
#
# print(eastPointList)
#
# for i in range(x):
#     px = im.getpixel((i,0))
#     if px != 0:
#         northPointList.append((i,0))
#
# print(northPointList)
#
# for i in range(x):
#     px = im.getpixel((i,y-1))
#     if px != 0:
#         southPointList.append((i,y-1))
#
# print(southPointList)




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





