# -*- coding: utf-8 -*-
"""
Created on 08.09.2015 12:47

@author: Garvas
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2

connect = psycopg2.connect(database='postgres', user='postgres', host='localhost', password='go5kew0t')
cursor = connect.cursor()