import os
import sys
import csv
import json

os.chdir(os.path.dirname(__file__))

# previous entries to update
with open("fragenUndSzenarien.json", mode='r', encoding='utf-8') as json_file:
    data = json.load(json_file)
    existing_questions = data['questions']
    existing_scenarios = data['scenarios']
    # print(existing_scenarios)

updated_scenarios = {}
list_of_scenarios = []

#importing scenarios from csv
csv_file = 'szenarien.csv'
with open(csv_file, mode='r', encoding='utf-8-sig') as csv_file:
    csvfiledata = csv.DictReader(csv_file, delimiter=',')
    # print(csvfiledata)
    for r, row_data in enumerate(csvfiledata):
        # extract code to use as identifier 
        key = row_data.pop("code")
        list_of_scenarios.append(key)
        # 'pop' has removed the 'code' from row_data, so now we are collecting the rest of the information
        subkeys = row_data.keys()
        subvalues = row_data.values()
        updated_scenarios[key] = dict(zip(subkeys, subvalues))

print(list_of_scenarios)

updated_questions = existing_questions.copy()

for key, val in existing_questions.items():
    answers = val['antworten']
    for akey, aname in answers.items():
        updated_questions[key]["antworten"][akey] = {
            "text": aname,
            "effects": []
        }
# print(updated_questions)

# MASS-POPULATE SOME EFFECTS
for code in list_of_scenarios:
    # question artLV excludes all options not matching the selected LV type
    if code.split('-')[0] not in ["vl", "so"]:
        effect = (code, -100)
        updated_questions["artLV"]["antworten"]["VL"]["effects"].append(effect)
    if code.split('-')[0] not in ["se", "so"]:
        effect = (code, -100)
        updated_questions["artLV"]["antworten"]["SE"]["effects"].append(effect)
    if code.split('-')[0] not in ["pr"]:
        effect = (code, -100)
        updated_questions["artLV"]["antworten"]["PR"]["effects"].append(effect)

    # LZiP: if essential learning goals in person, exclude hybrid and online options
    if code.split("-")[1] in ["async", "onl", "ringonl", "hyb", "ringhyb2"]:
        effect = (code, -100)
        updated_questions["LZiP"]["antworten"]["2"]["effects"].append(effect)

    # LZsy: if important learning goals are exclusively attainable synchronously, exclude all options that are fully asynchronous or offer asynchronous alternatives
    if code.split("-")[3] in ["3", "4"]:
        effect = (code, -100)
        updated_questions["LZsy"]["antworten"]["2"]["effects"].append(effect)

    # IntSync: if synchronous interaction is wished at different levels, exclude options with lower levels of interaction
    if code.split("-")[2] == "0":
        effect = (code, -100)
        updated_questions["IntSync"]["antworten"]["1"]["effects"].append(effect)
        updated_questions["IntSync"]["antworten"]["2"]["effects"].append(effect)
    if code.split("-")[2] == "1":
        effect = (code, -100)
        updated_questions["IntSync"]["antworten"]["2"]["effects"].append(effect)


    # question niePr; if some students can never make it to class in-person, then exclude all options exclusively in-person for students
    if code.split("-")[1] in ["praes", "ringpr", "rem", "ringhyb1", "wechs"]:
        # do not exclude options with asynchronous participation alternative
        if code.split("-")[3] != "3":
            effect = (code, -100)
            updated_questions["niePr"]["antworten"]["ja"]["effects"].append(effect)

    # if not allowed to teach online at all, exclude all online options
    if code.split("-")[1] in ["async", "onl", "ringonl"]:
        effect = (code, -100)
        updated_questions["onlErlLP"]["antworten"]["kein"]["effects"].append(effect)

    # if students not allowed to attend online at all, exclude hybrid and online options for students
    if code.split("-")[1] in ["async", "onl", "ringonl", "wechs", "hyb", "ringhyb2"]:
        effect = (code, -100)
        updated_questions["onlErlSt"]["antworten"]["kein"]["effects"].append(effect)

