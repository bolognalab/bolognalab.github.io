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

updated_json = {}
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

updated_questions = existing_questions.copy()

for key, val in existing_questions.items():
    answers = val['antworten']
    for akey, aname in answers.items():
        updated_questions[key]["antworten"][akey] = {
            "text": aname,
            "effects": {}
        }
# print(updated_questions)

# MASS-POPULATE SOME EFFECTS
for code in list_of_scenarios:
    # ABSOLUTE RULES (complete exclusion)
    # question artLV excludes all options not matching the selected LV type
    if code.split('-')[0] not in ["vl", "so"]:
        updated_questions["artLV"]["antworten"]["VL"]["effects"][code] = -100
    if code.split('-')[0] not in ["se", "so"]:
        updated_questions["artLV"]["antworten"]["SE"]["effects"][code] = -100
    if code.split('-')[0] not in ["pr"]:
        updated_questions["artLV"]["antworten"]["PR"]["effects"][code] = -100

    # LZiP: if essential learning goals in person, exclude hybrid and online options
    if code.split("-")[1] in ["async", "onl", "ringonl", "hyb", "ringhyb2"]:
        updated_questions["LZiP"]["antworten"]["2"]["effects"][code] = -100

    # LZsy: if important learning goals are exclusively attainable synchronously, exclude all options that are fully asynchronous or offer asynchronous alternatives
    if code.split("-")[3] in ["3", "4"]:
        updated_questions["LZsy"]["antworten"]["2"]["effects"][code] = -100

    # IntSync: if synchronous interaction is wished at different levels, exclude options with lower levels of interaction
    if code.split("-")[2] == "0":
        updated_questions["IntSync"]["antworten"]["1"]["effects"][code] = -100
        updated_questions["IntSync"]["antworten"]["2"]["effects"][code] = -100
    if code.split("-")[2] == "1":
        updated_questions["IntSync"]["antworten"]["2"]["effects"][code] = -100

    # IntAsync: if asynchronous interaction is wished at different levels, exclude options with less interaction
    if code.split("-")[4] == "0":
        updated_questions["IntAsync"]["antworten"]["1"]["effects"][code] = -100
        updated_questions["IntAsync"]["antworten"]["2"]["effects"][code] = -100
    if code.split("-")[4] == "1":
        updated_questions["IntAsync"]["antworten"]["2"]["effects"][code] = -100

    # niePr; if some students can never make it to class in-person, then exclude all options exclusively in-person for students
    if code.split("-")[1] in ["praes", "ringpr", "rem", "ringhyb1", "grwechs"]:
        # do not exclude options with asynchronous participation alternative
        if code.split("-")[3] != "3":
            effect = (code, -100)
            updated_questions["niePr"]["antworten"]["ja"]["effects"][code] = -100

    # if not allowed to teach online at all, exclude all online options
    if code.split("-")[1] in ["async", "onl", "ringonl"]:
        updated_questions["onlErlLP"]["antworten"]["kein"]["effects"][code] = -100

    # if students not allowed to attend online at all, exclude hybrid and online options for students
    if code.split("-")[1] in ["async", "onl", "ringonl", "grwechs", "hyb", "ringhyb2"]:
        updated_questions["onlErlSt"]["antworten"]["kein"]["effects"][code] = -100

    # onlZugang: if not all students have access to stable internet (for conferencing), exclude all online-only or mandatorily partially online options
    if code.split("-")[1] in ["async", "onl", "ringonl", "grwechs"]:
        updated_questions["onlZugang"]["antworten"]["nein"]["effects"][code] = -100

    # aufzTech: if a clear recording of the room is not possible, exclude Remote Classroom
    if code.split("-")[1] == "rem":
        updated_questions["aufzTech"]["antworten"]["nein"]["effects"][code] = -100

    # gaeste: if having regular guest speakers, only display Ringvorlesung formats
    if "ring" not in code.split("-")[1]:
        updated_questions["gaeste"]["antworten"]["2"]["effects"][code] = -100
    # and obviously don't display Ringvorlesung formats if no guests!
    if "ring" in code.split("-")[1]:
        updated_questions["gaeste"]["antworten"]["0"]["effects"][code] = -100
        updated_questions["gaeste"]["antworten"]["1"]["effects"][code] = -100
    
    # gaesteMittel: no in-person Ringvorlesung if no means to invite
    if code.split("-")[1] == "ringpr":
        updated_questions["gaesteMittel"]["antworten"]["nein"]["effects"][code] = -100

    # NON-ABSOLUTE RULES
    # LZiP: if no important learning goals exclusively in-person, discourage in-person only options
    if "praes" in code.split("-")[1] and code.split("3") in ["0", "1", "2"]:
        updated_questions["LZiP"]["antworten"]["0"]["effects"][code] = -2
        updated_questions["LZiP"]["antworten"]["1"]["effects"][code] = -1

    

updated_json["questions"] = updated_questions
updated_json["scenarios"] = updated_scenarios

json_file = "fragenSzenarienV2.json"
def updateJSON(json_data, json_file):
    with open(json_file, 'w') as json_file:
        json_file.write(json.dumps(json_data, indent=4))
        print("json file created or updated successfully")

updateJSON(updated_json, json_file)