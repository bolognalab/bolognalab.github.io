# -*- coding: utf-8 -*-
"""
Convert CSV to json
"""
import csv
import json

csv_file = 'programm-themenwoche.csv'
json_file = 'programm-themenwoche.json'

with open(csv_file, mode='r', encoding='utf-8') as csv_file:
    csvfiledata = csv.DictReader(csv_file)
    json_list = []
    for r, row_data in enumerate(csvfiledata):
        fixed_data = {'short-event-name' if k == '\ufeffshort-event-name' else k:v for k,v in row_data.items()}
        # word = fixed_data
        # s = "-".join([word["Kana"], word["English"][:15], word["Category"]])
        # swaps = [("{", "X"), ("}", "X"), ("/", "L")]
        # for old, new in swaps:
        #     s = s.replace(old, new)
        # fixed_data['id']=s
        # print(fixed_data)
        json_list.append(fixed_data)
# print(json_list)
with open(json_file, 'w') as json_file:
    json_file.write(json.dumps(json_list, indent=4))

    