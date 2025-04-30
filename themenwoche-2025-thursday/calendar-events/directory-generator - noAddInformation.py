# -*- coding: utf-8 -*-
# Um die Blöcke "Mehr Informationen" und "Zum Kalender hinzufügen automatisch anzeigen zu lassen, müssen Zeilen 57-58 (die jetzt kommentiert sind) wieder aktiviert werden und die Datei "events-dir.html" wieder gelöscht werden
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
    div0 = ET.Element('div', attrib={'class': 'event-info',
                                     'id': event_id})
    
    
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
                                        'href': '#0',
                                        "target": '_blank'
                                        })
    aCal.text = r'&#x1F4C5; &nbsp; zum Kalender hinzuf&#xFC;gen (.ics)'
    
    # spanEL.append(aMoreInfo)
    # spanEL.append(aCal)
    div0.append(spanEL)
    body.append(ET.Comment("         " + event_id + "           "))
    body.append(div0)
    
    
ET.indent(html, '   ')
ET.ElementTree(html).write(sys.stdout, encoding='unicode',
                            method='html')

fname = "events-dir.html"
if not os.path.exists(fname):
    with open(fname, "w") as f:
        ET.ElementTree(html).write(f, encoding='unicode',
                                method='html')

    # replace &amp; with "&"
    with open(fname, 'r') as f:
        filedata = f.read()
    filedata = filedata.replace('&amp;', '&')

    with open(fname, 'w') as f:
        f.write(filedata)
        f.close()
else:
    print("\n \n The file 'events-dir.html' already exists. If you really want to replace it with an automatically generated one, please delete the existing file and run this script again. \n \n",
          "Die Datei 'events-dir.html' existiert bereits. Wenn Sie sie wirklich durch eine automatisch generierte Datei ersetzen wollen, löschen Sie bitte die bestehende Datei und führen Sie dieses Python-Skript erneut aus. \n \n")