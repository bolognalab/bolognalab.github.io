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
        updated_scenarios[key]["special_cases"] = {}

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

def setSpecialCase(code, conditions, case):
    updated_scenarios[code]["special_cases"][conditions] = case

# MASS-POPULATE SOME EFFECTS
for code in list_of_scenarios:
    # artLV: exclude all options not matching the selected LV type
    if code.split('-')[0] not in ["vl", "so"]:
        updated_questions["artLV"]["antworten"]["VL"]["effects"][code] = -100
    if code.split('-')[0] not in ["se", "so"]:
        # allow Ringvorlesung format for seminar
        if code.split('-')[1] not in ["ringpraes", "ringonl", "ringhyb1", "ringhyb2"]:
            updated_questions["artLV"]["antworten"]["SE"]["effects"][code] = -100
    if code.split('-')[0] not in ["pr"]:
        updated_questions["artLV"]["antworten"]["PR"]["effects"][code] = -100
    if code.split('-')[0] != "so":
        updated_questions["artLV"]["antworten"]["SO"]["effects"][code] = -100

    #modulCombo: do nothing, but will affect previous answers

    # LZiP: if essential learning goals in person and there are no other LV in the module, exclude hybrid and online options.
    # if there are essential goals in person and there are other LV in the module, discourage those options and add note
    # if some nonessential learning goals in person, discourage online options and less so hybrid options
    if code.split("-")[1] in ["async", "onl", "ringonl"]:
        setConditionalEffect("LZiP", "2", code, "modulCombo=nein", -100)
        setConditionalEffect("LZiP", "2", code, "modulCombo=ja", -2)
        setConditionalEffect("LZiP", "1", code, "modulCombo=nein", -2)
        setConditionalEffect("LZiP", "1", code, "modulCombo=ja", -1)
        updated_questions["LZiP"]["antworten"]["0"]["effects"][code] = +1
    if code.split("-")[1] in ["hyb", "ringhyb2", "onlhybwechs", "hybrem"]:
        setConditionalEffect("LZiP", "2", code, "modulCombo=nein", -100)
        setConditionalEffect("LZiP", "2", code, "modulCombo=ja", -2)
        setConditionalEffect("LZiP", "1", code, "modulCombo=nein", -1)
        updated_questions["LZiP"]["antworten"]["0"]["effects"][code] = +1

    # LZsy: if important learning goals are exclusively attainable synchronously, exclude all options that are fully asynchronous or offer asynchronous alternatives
    if code.split("-")[3] == "3":
        updated_questions["LZsy"]["antworten"]["1"]["effects"][code] = -1
        updated_questions["LZsy"]["antworten"]["2"]["effects"][code] = -100
    if code.split("-")[3] == "4":
        updated_questions["LZsy"]["antworten"]["1"]["effects"][code] = -2
        updated_questions["LZsy"]["antworten"]["2"]["effects"][code] = -100 

    # niePr; if some students can never make it to class in-person, then exclude all options exclusively in-person for students
    if code.split("-")[1] in ["praes", "ringpraes", "rem", "ringhyb1", "grwechs", "praesonlwechs", "praeshybwechs", "onlpraeswechs"]:
        # do not exclude options with asynchronous participation alternative
        if code.split("-")[3] != "3":
            updated_questions["niePr"]["antworten"]["ja"]["effects"][code] = -100
        else:
            updated_questions["niePr"]["antworten"]["ja"]["effects"][code] = -2

    # nieSync; if some students cannot regularly make it to class synchronously, then exclude all options where material is exclusively shared synchronously
    if code.split("-")[3] == "0":
        updated_questions["nieSync"]["antworten"]["ja"]["effects"][code] = -100
    # also, discourage options where asynchronous work only complements (but cannot replace) synchronous participation
    if code.split("-")[3] == "1":
        updated_questions["nieSync"]["antworten"]["ja"]["effects"][code] = -2
    if code.split("-")[3] == "2":
        updated_questions["nieSync"]["antworten"]["ja"]["effects"][code] = -1
    # and encourage options with asynchronous participation alternatives, unless there are essential learning goals in person
    if code.split("-")[3] in ["3", "4"]: 
        setConditionalEffect("nieSync", "ja", code, "LZsy!=2", +1)

    # wohnLP: if the instructor lives far from the university, favor online and mostly-online options, unless there are essential learning goals in person!
    if code.split("-")[1] in ["onl", "ringonl", "onlhybwechs", "onlpraeswechs", "async"]: 
        setConditionalEffect("wohnLP", "nein", code, "LZiP!=2", +1)

    # regAbw: if instructor is occasionally absent from campus, encourage switching options with more in-person character
    if code.split("-")[1] in ["praesonlwechs", "praeshybwechs", "hyb", "ringhyb1", "ringhyb2", "hybrem"]: 
        # note: hybrid options also count, because the hybrid room can easily be moved fully online for individual classes
        updated_questions["regAbw"]["antworten"]["abundzu"]["effects"][code] = + 2
    # if regularly absent from campus, enccourage switching options with more online character and fully online options (for the instructor)
    if code.split("-")[1] in ["onlpraeswechs", "onl", "ringonl", "onlhybwechs"]:
        updated_questions["regAbw"]["antworten"]["oft"]["effects"][code] = + 2
    # also encourage async options
    if code.split("-")[3] == "4": 
        updated_questions["regAbw"]["antworten"]["oft"]["effects"][code] = + 2

    # onlBereit: if instructor doesn't want to teach online at all, exclude fully online and switching options
    if code.split("-")[1] in ["async", "onl", "ringonl", "onlhybwechs", "onlpraeswechs", "praesonlwechs"]:
        updated_questions["onlBereit"]["antworten"]["kein"]["effects"][code] = -100
    # if instructor wants to teach online only occasionally:
    # exclude fully online options
    if code.split("-")[1] in ["async", "onl", "ringonl"]:
        updated_questions["onlBereit"]["antworten"]["geleg"]["effects"][code] = -100
    #  discourage options with more than occasional online teaching
    if code.split("-")[1] in ["onlhybwechs", "onlpraeswechs"]:
        updated_questions["onlBereit"]["antworten"]["geleg"]["effects"][code] = -1
    # if instructor wants to teach online as much as possible, encourage options with a higher online portion
    if code.split("-")[1] in ["onlhybwechs", "onlpraeswechs"]:
        updated_questions["onlBereit"]["antworten"]["viel"]["effects"][code] = +2
    if code.split("-")[1] in ["onl", "ringonl"]:
        # do not favor fully online options if there are important learning goals in person
        setConditionalEffect("onlBereit", "viel", code, "LZiP=0", +2)
        setConditionalEffect("onlBereit", "viel", code, "LZiP=1", +1)

    # limZPSt: if most students have significant time-limitations:
    #  - discourage flipped-classroom options
    if code.split("-")[3] == "2":
        updated_questions["limZPSt"]["antworten"]["ja"]["effects"][code] = - 2
    #  -  encourage asynchronous alternative options
    if code.split("-")[3] in ["3", "4"]: 
        updated_questions["limZPSt"]["antworten"]["ja"]["effects"][code] = + 2
    # - lightly encourage online and hybrid options (async is already favored above)
    if code.split("-")[1] in ["hyb", "onl", "ringonl", "ringhyb2", "onlpraeswechs", "onlhybwechs", "hybrem"]:
        updated_questions["limZPSt"]["antworten"]["ja"]["effects"][code] = + 1
    # - lightly encourage synchronous only options
    if code.split("-")[3] == "0":
        # TODO: maybe: check for answer to question: are certain students unable to attend synchronously ever?
        updated_questions["limZPSt"]["antworten"]["ja"]["effects"][code] = + 1  

    # studGeraete: do nothing, but it will influence future answers

    # onlZugang: if not all students have access to stable internet (for conferencing), exclude all online-only or mandatorily partially online options
    if code.split("-")[1] in ["async", "onl", "ringonl", "grwechs", "praesonlwechs", "onlpraeswechs", "onlhybwechs"]:
        updated_questions["onlZugang"]["antworten"]["nein"]["effects"][code] = -100
        updated_questions["onlZugang"]["antworten"]["idk"]["effects"][code] = -2

    # aufzTech
    # if a clear recording of the room is not possible, exclude Remote Classroom
    if code.split("-")[1] in ["rem", "hybrem"]:
        updated_questions["aufzTech"]["antworten"]["nein"]["effects"][code] = -100

    # IntSync: 
    # options with no synchronous interaction and purely async options: exlude automatically if any interaction is wished
    if code.split("-")[2] == "0" or code.split("-")[3] == "4":
        updated_questions["IntSync"]["antworten"]["1"]["effects"][code] = -100
        updated_questions["IntSync"]["antworten"]["2"]["effects"][code] = -100
    # option with only St-LP interaction: exclude if St-St wanted AND St-St technically possible; otherwise discourage and suggest replacing sync interaction with async interaction.
    if code.split("-")[2] == "1":
        # always technically possible for pure-in-person and pure-online
        if code.split("-")[1] in ["praes", "ringpraes", "onl", "ringonl", "ringhyb1", "onlpraeswechs", "praesonlwechs"]:
            updated_questions["IntSync"]["antworten"]["2"]["effects"][code] = -100
        # for hybrid options with individual online students: technically possible with student devices
        if code.split("-")[1] in ["hyb", "ringhyb2", "rem", "hybrem", "onlhybwechs", "praeshybwechs"]:
            setConditionalEffect("IntSync", "2", code, "studGeraete=ja", -100)
    # if St-St interaction is wished but it's not technically possible, discourage options with synchronous St-St and instead favor those with synchronous St-LP and asynchronous St-St
    # xx-xxx-1-x-2
    if code.split("-")[2] == "2":
        # if St-St is desired and possible, favor it!
        if code.split("-")[1] in ["praes", "ringpraes", "onl", "ringonl", "ringhyb1", "onlpraeswechs", "praesonlwechs"]:
            updated_questions["IntSync"]["antworten"]["2"]["effects"][code] = +1
        # if St-St is desired and impossible, discourage it
        if code.split("-")[1] in ["hyb", "ringhyb2", "rem", "hybrem", "onlhybwechs", "praeshybwechs"]:
            # TODO: here add a note to differentiate between cross-group and intra-group interaction.
            setConditionalEffect("IntSync", "2", code, "studGeraete=nein", -100)

    # IntAsync: if desired asynchronous interaction is level 1 or 2, exclude options with less interaction 
    if code.split("-")[4] == "0":
        updated_questions["IntAsync"]["antworten"]["1"]["effects"][code] = -100
        updated_questions["IntAsync"]["antworten"]["2"]["effects"][code] = -100
    if code.split("-")[4] == "1":
        updated_questions["IntAsync"]["antworten"]["2"]["effects"][code] = -100

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
    if code.split("-")[1] in ["hyb", "ringhyb2", "onlhybwechs", "hybrem"]:
        setConditionalEffect("exkurMittel", "ja", code, "exkur=ja", -1)
    # favor options with fully-in-person excursion possibility if enough means
    if code.split("-")[1] in ["praes", "ringhyb1", "ringpraes", "onlpraeswechs"]:
        setConditionalEffect("exkurMittel", "ja", code, "exkur=ja", +2)
    # favor options with hybrid excursion option if not enough means to send everyone
    if code.split("-")[1] in ["hyb", "ringhyb2", "onlhybwechs", "praeshybwechs", "hybrem"]:
        setConditionalEffect("exkurMittel", "nein", code, "exkur=ja", +2)

    # begrAnz: gruppenwechsel is pointless if everyone can fit in the room
    if code.split("-")[1] == "grwechs":
        updated_questions["begrAnz"]["antworten"]["nein"]["effects"][code] = -100
        updated_questions["begrAnz"]["antworten"]["ja"]["effects"][code] = + 2

    #intKoll: only include remote, online, switching, and hybrid options
    if code.split("-")[1] not in ["onl", "onlhybwechs", "ringonl", "onlpraeswechs", "ringhyb2", "rem", "hyb", "hybrem"]:
        updated_questions["intKoll"]["antworten"]["ja"]["effects"][code] = -100  
    # add special case 'international'
    
    # SPECIAL CASES
    setSpecialCase(code, "intKoll=ja", "international")

    #for online, hybrid and async options, if there are other LV in the same module, add note that the other LV should have in-person elements
    if code.split("-")[1] in ["onl", "onlhybwechs", "ringonl", "ringhyb2", "hyb", "hybrem"]:
        setSpecialCase(code, "modulCombo=ja+LZiP=2", "alternativPraes")
        setSpecialCase(code, "modulCombo=ja+LZiP=1", "alternativPraes")



updated_json["questions"] = updated_questions
updated_json["scenarios"] = updated_scenarios

json_file = "data.json"
def updateJSON(json_data, json_file):
    with open(json_file, 'w') as json_file:
        json_file.write(json.dumps(json_data, indent=4))
        print("json file created or updated successfully")

updateJSON(updated_json, json_file)