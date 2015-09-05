# -*- coding: utf-8 -*-
"""
Created on 29.08.2015 16:48

@author: Garvas
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re

targetFolder = u'Z:/SiteliteIMG/Ленобл_Ресурс-П'

ext = re.compile(r"^.+\.(?:hdf|temp|dbf|shp|shx|smd|tif|tiff|txt|log)$", re.IGNORECASE + re.UNICODE)

def sort_dir(targetFolder, ext):

    print 'Processing ' + targetFolder

    for fileName in os.listdir(targetFolder):
        filePath = os.path.join(targetFolder, fileName)
        if os.path.isfile(filePath):
            if ext.match(fileName):
                dirPath = os.path.join(targetFolder, (os.path.splitext(fileName)[0]).strip())
                if not os.path.exists(dirPath):
                    os.mkdir(dirPath)
                    os.rename(filePath, os.path.join(dirPath, fileName))
                else:
                    os.rename(filePath, os.path.join(dirPath, fileName))

    print 'Done!'

#sort_dir(targetFolder,ext)