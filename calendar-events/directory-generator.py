# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 11:18:54 2024

@author: spithana
"""
import os
import sys
from xml.etree import ElementTree as ET
import csv

os.chdir(os.path.dirname(__file__))
events_list = []
#reading csv file to get ID (e.g. "event-auftakt")
csv_file = '../files/programm-themenwoche.csv'
with open(csv_file, mode='r', encoding='utf-8') as csv_file:
    csvfiledata = csv.DictReader(csv_file, delimiter=';')
    for r, row_data in enumerate(csvfiledata):
        events_list.append(row_data["id"])



html = ET.Element('html')
head = ET.Element('head')
html.append(head)
title = ET.Element('title')
meta = ET.Element('meta', attrib={"charset": "utf-8"})
head.append(title)
head.append(meta)
title.text="Events"
body = ET.Element('body')
html.append(body)

for event_id in events_list:
    div0 = ET.Element('div', attrib={'class': 'event-info'})
    
    
    div1 = ET.Element('div', attrib={'class': 'md-container white-fade'})
    pHashtag = ET.Element('p', attrib={'class': 'hashtag'})
    mdBlock = ET.Element('md-block')
    div1.append(pHashtag); div1.append(mdBlock)
    div0.append(div1)
    
    spanEL = ET.Element('span', attrib={'class': 'event-links'})
    aMoreInfo = ET.Element('a', attrib={'class': 'moreInfoLink',
                                        'href': '#0'})
    aMoreInfo.text = r'&#128279; Mehr Infos & Anmeldung'
    
    aCal = ET.Element('a', attrib={'class': 'addToCalendar',
                                        'href': '#0'})
    aCal.text = r'&#x1F4C5; &nbsp; zum Kalender hinzufügen (.ics)'
    
    spanEL.append(aMoreInfo)
    spanEL.append(aCal)
    div0.append(spanEL)
    body.append(div0)
    
ET.indent(html, '  ')
# with open("edir-test.html", "w") as f:
# ET.ElementTree(html).write(sys.stdout, encoding='unicode',
#                            method='html')
with open("edir-test.html", "w") as f:
    ET.ElementTree(html).write(f, encoding='unicode',
                            method='html')

# replace &amp; with "&"
with open('edir-test.html', 'r') as f:
    filedata = f.read()
filedata = filedata.replace('&amp;', '&')
with open('edir-test.html', 'w') as f:
    f.write(filedata)