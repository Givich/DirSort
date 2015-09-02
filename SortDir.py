__author__ = 'RSA'
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 15:37:49 2015

@author: RSA
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re

targetFolder = u"D:/COLD/293610_Всеволжский район_геотон"

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

print find_dir(targetFolder)

# def find_all_dir(listDir):
#     for dir in listDir:
#         find_dir(dir)


