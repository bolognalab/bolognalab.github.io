import os
import sys
import csv
import json

os.chdir(os.path.dirname(__file__))

# previous entries to update
with open("fragen_source.json", mode='r', encoding='utf-8') as json_file:
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
    csvfiledata = csv.DictReader(csv_file, delimiter=';')
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
            "effects": {},
            "conditionalEffects": {}
        }
# print(updated_questions)
def setConditionalEffect(qKey, aKey,  code, condition, effect):
    try:
        updated_questions[qKey]["antworten"][aKey]["conditionalEffects"][code][condition] = effect
        updated_questions[qKey]["antworten"][aKey]["effects"][code] = "FUNC"
    except KeyError:
        updated_questions[qKey]["antworten"][aKey]["conditionalEffects"][code] = {}
        updated_questions[qKey]["antworten"][aKey]["conditionalEffects"][code][condition] = effect
        updated_questions[qKey]["antworten"][aKey]["effects"][code] = "FUNC"


# MASS-POPULATE SOME EFFECTS
for code in list_of_scenarios:
    # artLV: exclude all options not matching the selected LV type
    if code.split('-')[0] not in ["vl", "so"]:
        updated_questions["artLV"]["antworten"]["VL"]["effects"][code] = -100
    if code.split('-')[0] not in ["se", "so"]:
        updated_questions["artLV"]["antworten"]["SE"]["effects"][code] = -100
    if code.split('-')[0] not in ["pr"]:
        updated_questions["artLV"]["antworten"]["PR"]["effects"][code] = -100
    if code.split('-')[0] != "so":
        updated_questions["artLV"]["antworten"]["SO"]["effects"][code] = -100

    # LZiP: if essential learning goals in person, exclude hybrid and online options
    if code.split("-")[1] in ["async", "onl", "ringonl", "hyb", "ringhyb2", "onlhybwechs"]:
        updated_questions["LZiP"]["antworten"]["2"]["effects"][code] = -100
        updated_questions["LZiP"]["antworten"]["1"]["effects"][code] = -2
        updated_questions["LZiP"]["antworten"]["0"]["effects"][code] = +1

    # LZsy: if important learning goals are exclusively attainable synchronously, exclude all options that are fully asynchronous or offer asynchronous alternatives
    if code.split("-")[3] in ["3", "4"]:
        updated_questions["LZsy"]["antworten"]["2"]["effects"][code] = -100

    # IntSync: if desired synchronous interaction is level 1 or 2, exclude options with lower levels of interaction
    if code.split("-")[2] == "0":
        updated_questions["IntSync"]["antworten"]["1"]["effects"][code] = -100
        updated_questions["IntSync"]["antworten"]["2"]["effects"][code] = -100
    if code.split("-")[2] == "1":
        updated_questions["IntSync"]["antworten"]["2"]["effects"][code] = -100

    # IntAsync: if desired asynchronous interaction is level 1 or 2, exclude options with less interaction (if it's technically possible)
    # TODO: if St-St interaction is not technically feasible, discourage but not exclude those options
    if code.split("-")[4] == "0":
        updated_questions["IntAsync"]["antworten"]["1"]["effects"][code] = -100
        updated_questions["IntAsync"]["antworten"]["2"]["effects"][code] = -100
    if code.split("-")[4] == "1":
        updated_questions["IntAsync"]["antworten"]["2"]["effects"][code] = -100
    

    # niePr; if some students can never make it to class in-person, then exclude all options exclusively in-person for students
    if code.split("-")[1] in ["praes", "ringpr", "rem", "ringhyb1", "grwechs", "praesonlwechs", "praeshybwechs", "onlpraeswechs"]:
        # do not exclude options with asynchronous participation alternative
        if code.split("-")[3] != "3":
            updated_questions["niePr"]["antworten"]["ja"]["effects"][code] = -100

    # nieSync; if some students cannot regularly make it to class synchronously, then exclude all options where material is exclusively shared synchronously
    if code.split("-")[3] == "0":
        updated_questions["nieSync"]["antworten"]["ja"]["effects"][code] = -100
    # also, discourage options where asynchronous work only complements (but cannot replace) synchronous participation
    if code.split("-")[3] == "1":
        updated_questions["nieSync"]["antworten"]["ja"]["effects"][code] = -2
    if code.split("-")[3] == "2":
        updated_questions["nieSync"]["antworten"]["ja"]["effects"][code] = -1
    # and encourage options with asynchronous participation alternatives
    if code.split("-")[3] in ["3", "4"]: 
        updated_questions["nieSync"]["antworten"]["ja"]["effects"][code] = + 1

    # wohnLP: if the instructor lives far from the university, favor online and mostly-online options!
    if code.split("-")[1] in ["onl", "ringonl", "onlhybwechs", "onlpraeswechs", "async"]: 
        updated_questions["wohnLP"]["antworten"]["nein"]["effects"][code] = + 1

    # regAbw: if instructor is occasionally absent from campus, encourage switching options and, less so, primarily-online options
    if code.split("-")[1] in ["praesonlwechs", "praeshybwechs", "hyb", "ringhyb1", "ringhyb2"]: 
        # note: hybrid options also count, because the hybrid room can easily be moved fully online for individual classes
        updated_questions["regAbw"]["antworten"]["abundzu"]["effects"][code] = + 2
    if code.split("-")[1] in ["onlpraeswechs", "onl", "ringonl", "onlhybwechs"]:
        updated_questions["regAbw"]["antworten"]["abundzu"]["effects"][code] = + 1
    # if regularly absent from campus, enccourage fully online options (for the instructor)
    if code.split("-")[1] in ["onlpraeswechs", "onl", "ringonl", "onlhybwechs"]:
        updated_questions["regAbw"]["antworten"]["oft"]["effects"][code] = + 2
    # also encourage async options
    if code.split("-")[3] == "4": 
        updated_questions["regAbw"]["antworten"]["oft"]["effects"][code] = + 2

    # onlErlLP: if not allowed to teach online at all, exclude all online options
    if code.split("-")[1] in ["async", "onl", "ringonl", "onlhybwechs", "onlpraeswechs"]:
        updated_questions["onlErlLP"]["antworten"]["kein"]["effects"][code] = -100

    # onlErlSt: if students not allowed to attend online at all, exclude hybrid and online options for students
    if code.split("-")[1] in ["async", "onl", "ringonl", "grwechs", "hyb", "ringhyb2", "onlhybwechs", "onlpraeswechs", "praesonlwechs", "praeshybwechs"]:
        updated_questions["onlErlSt"]["antworten"]["kein"]["effects"][code] = -100

    # limZPSt: if most students have significant time-limitations:
    #  - discourage flipped-classroom options
    if code.split("-")[3] == "2":
        updated_questions["limZPSt"]["antworten"]["ja"]["effects"][code] = - 2
    #  -  encourage asynchronous alternative options
    if code.split("-")[3] in ["3", "4"]: 
        updated_questions["limZPSt"]["antworten"]["ja"]["effects"][code] = + 2
    # - lightly encourage online and hybrid options (async is already favored above)
    if code.split("-")[1] in ["hyb", "onl", "ringonl", "ringhyb2", "onlpraeswechs", "onlhybwechs"]:
        updated_questions["limZPSt"]["antworten"]["ja"]["effects"][code] = + 1
    # - lightly encourage synchronous only options
    if code.split("-")[3] == "0":
        # TODO: maybe: check for answer to question: are certain students unable to attend synchronously ever?
        updated_questions["limZPSt"]["antworten"]["ja"]["effects"][code] = + 1  

    # onlZugang: if not all students have access to stable internet (for conferencing), exclude all online-only or mandatorily partially online options
    if code.split("-")[1] in ["async", "onl", "ringonl", "grwechs", "praesonlwechs", "onlpraeswechs", "onlhybwechs"]:
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
    if code.split("-")[1] == "ringpraes":
        updated_questions["gaesteMittel"]["antworten"]["nein"]["effects"][code] = -100
        updated_questions["gaesteMittel"]["antworten"]["ja"]["effects"][code] = +1
    if code.split("-")[1] == "ringhyb2":
        updated_questions["gaesteMittel"]["antworten"]["ja"]["effects"][code] = +1

    #exkur: if there are excursions, exclude fully-online options
    if code.split("-")[1] in ["onl", "ringonl", "async"]:
        updated_questions["exkur"]["antworten"]["ja"]["effects"][code] = -100
    
    #exkurMittel depending on exkurs
    # disourage hybrid options (where some students would never participate in person) if there is enough means to send every student to the excursion
    if code.split("-")[1] in ["hyb", "ringhyb2", "onlhybwechs"]:
        setConditionalEffect("exkurMittel", "ja", code, "exkur=ja", -1)
    # favor options with fully-in-person excursion possibility if enough means
    if code.split("-")[1] in ["praes", "ringhyb1", "ringpraes", "onlpraeswechs"]:
        setConditionalEffect("exkurMittel", "ja", code, "exkur=ja", +2)
    # favor options with hybrid excursion option if not enough means to send everyone
    if code.split("-")[1] in ["hyb", "ringhyb2", "onlhybwechs", "praeshybwechs"]:
        setConditionalEffect("exkurMittel", "nein", code, "exkur=ja", +2)

    

    # begrAnz: gruppenwechsel is pointless if everyone can fit in the room
    if code.split("-")[1] == "grwechs":
        updated_questions["begrAnz"]["antworten"]["nein"]["effects"][code] = -100
        updated_questions["begrAnz"]["antworten"]["ja"]["effects"][code] = + 2

    #intKoll: exclude non-internet options if collaborative
    # if code.split("-")[1] not in ["onl", "onlhybwechs", "onlpraeswechs", "ringonl", "rem", "hyb", "ringhyb2"]


    # # LZiP: if no important learning goals exclusively in-person, discourage in-person only options
    # if "praes" in code.split("-")[1] and code.split("-")[3] in ["0", "1", "2"]:
    #     updated_questions["LZiP"]["antworten"]["0"]["effects"][code] = -2
    #     updated_questions["LZiP"]["antworten"]["1"]["effects"][code] = -1

    

    

updated_json["questions"] = updated_questions
updated_json["scenarios"] = updated_scenarios

json_file = "fragenSzenarienV2.json"
def updateJSON(json_data, json_file):
    with open(json_file, 'w') as json_file:
        json_file.write(json.dumps(json_data, indent=4))
        print("json file created or updated successfully")

updateJSON(updated_json, json_file)