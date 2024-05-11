# -*- coding: utf-8 -*-
"""
Convert CSV to json
"""
import csv
import json
import os

csv_file = 'programm-themenwoche.csv'
json_file = 'programm-themenwoche.json'
names_list = []
titles = {}

with open(csv_file, mode='r', encoding='utf-8') as csv_file:
    csvfiledata = csv.DictReader(csv_file)
    json_list = []
    for r, row_data in enumerate(csvfiledata):
        fixed_data = {'short-event-name' if k == '\ufeffshort-event-name' else k:v for k,v in row_data.items()}

        json_list.append(fixed_data)
        names_list.append(fixed_data["id"])
        titles[fixed_data["id"]]=fixed_data["long-event-name"]

def makeMD(names):
    for name in names:
        fname = "../calendar-events/" + name + ".md"
        print(fname, os.path.exists(fname))
        if not os.path.exists(fname):
            with open(fname, 'w', encoding="utf-8") as file:
                file.write("# " + titles[name] + '  \n')
                file.write("## Ort (z.B, Senatsaal)  \n##### Adresse und Raum \n--- \n### Art der Veranstaltung (z.B. Workshop) \nLeitung: \\n**Name 1**  \n##### Einrichtung 1\ ")
                pass
        
def updateJSON(json_list):
    with open(json_file, 'w') as json_file:
        json_file.write(json.dumps(json_list, indent=4))

    