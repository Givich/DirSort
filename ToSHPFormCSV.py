# -*- coding: utf-8 -*-
"""
Created on 04.09.2015 16:48

@author: Garvas
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-

import shapefile



"""
Make function!
Need integrate with other function!
"""
listCord = [3419261.8406793284, 8484744.62704141, 3493039.2666373765, 8463055.814794006, 3485980.486037629, 8439298.331971422, 3412424.606584053, 8460849.476686725]
b = ['1',' ','11.04.2015 11:57:42','RSP','GEOTONP','1','-','0.705140631130823','0','0:10:45.033879','0041_0102_10061_1_00083_02_10_003.tif','1','Restriction','-','-']
print b[2]
w = shapefile.Writer(shapefile.POLYGON)

w.poly(shapeType=5, parts=[[[listCord[0],listCord[1]], [listCord[2],listCord[3]], [listCord[4],listCord[5]],[listCord[6],listCord[7]]]])

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

w.save('shapefiles/test/testshp_1v1')
prjFile = open('shapefiles/test/testshp_1v1.prj','wb')

# Not need?
#prjFile.write('PROJCS["WGS_84_Pseudo_Mercator",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]],PROJECTION["Mercator"],PARAMETER["central_meridian",0],PARAMETER["false_easting",0],PARAMETER["false_northing",0],UNIT["Meter",1],PARAMETER["standard_parallel_1",0.0]]')




