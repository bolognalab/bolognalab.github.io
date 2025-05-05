# -*- coding: utf-8 -*-
# Um die komplette Vorlage (laut template.md) zu benutzen (anstatt von "Information folgt"), muss Zeile 37 "kommentiert werden" und Zeilen 38-39 wieder inkludiert werden. Alle .md Dateien müssen gelöscht werden, damit sie wieder generiert werden.
"""
Convert CSV to json
"""
import csv
import os

os.chdir(os.path.dirname(__file__))

csv_file = '../files/programm-themenwoche.csv'
template_file = 'template.md'
names_list = []
titles = {}

with open(csv_file, mode='r', encoding='utf-8') as csv_file:
    csvfiledata = csv.DictReader(csv_file, delimiter=';')
    json_list = []
    for r, row_data in enumerate(csvfiledata):
        fixed_data = {'short-event-name' if k == '\ufeffshort-event-name' else k:v for k,v in row_data.items()}
        json_list.append(fixed_data)
        names_list.append(fixed_data["id"])
        titles[fixed_data["id"]]=fixed_data["long-event-name"]


with open(template_file, 'r', encoding="utf-8") as file:
    linesToWrite = file.readlines()
print(linesToWrite)

for name in names_list:
    fname = name + ".md"
    print(fname, os.path.exists(fname))
    if not os.path.exists(fname):
        with open(fname, 'w', encoding="utf-8") as file:
            file.write("# " + titles[name] + '  \n')
            file.write("Information folgt")
            # for line in linesToWrite[1:]:
            #     file.write(line)
            pass


with open("test.md", 'w', encoding="utf-8") as file:
    file.write("# BigTitle \n")
    


# makeMD(names_list)