# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 13:40:40 2013

@author: malte
"""
from os import listdir
from os.path import isfile, join
import MySQLdb
import urllib,urllib2


db=MySQLdb.connect(host="localhost",user="",db="test")
c = db.cursor()
c.execute("select group_concat(ID) as duplicates, chr, position from exome_analysis group by chr, position having count(ID) > 1")
all_duplicates = c.fetchall()
for dup in all_duplicates:
    IDs = dup[0].split(',')
    d = db.cursor()
    d.execute('UPDATE exome_analysis SET exclude = 1 where ID = %i' % (int(IDs[1])))
    d.close()
    db.commit()