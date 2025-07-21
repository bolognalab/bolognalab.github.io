
import os
import sys
import csv
import json

os.chdir(os.path.dirname(__file__))

# previous entries to update
with open("fragen_source.json", mode='r', encoding='utf-8') as json_file:
    data = json.load(json_file)
    existing_questions = data['questions']

updated_json = {}
updated_scenarios = {}
list_of_scenarios = []

# indexing of special cases (only defined here)
special_cases =  {
        "0": "international",
        "1": "langfristGrupp",
        "2": "hybrideExkursion",
        "3": "onlineZuschaltungLP",
        "4": "gastOnline",
        "5": "gastVorOrtHyb",
        "6": "keineAufzeichnung", #nur für den Technik-Pfad
    }


#importing scenarios from csv
csv_file = 'szenarien.csv'
with open(csv_file, mode='r', encoding='utf-8-sig') as csv_file:
    csvfiledata = csv.DictReader(csv_file, delimiter=';')
    # print(csvfiledata)
    for r, row_data in enumerate(csvfiledata):
        # extract code to use as identifier 
        key = row_data.pop("code")
        shortkey = key

        # intervention: exclude combo syncInt=0, asyncTN=2
        if shortkey.split("-")[2] != "0" or shortkey.split("-")[3] != "2":
            list_of_scenarios.append(shortkey)
            # 'pop' has removed the 'code' from row_data, so now we are collecting the rest of the information
            subkeys = row_data.keys()
            subvalues = row_data.values()
            updated_scenarios[shortkey] = dict(zip(subkeys, subvalues))
            updated_scenarios[shortkey]["special_cases"] = {}

updated_questions = existing_questions.copy()

for key, val in existing_questions.items():
    answers = val['antworten']
    for akey, aname in answers.items():
        updated_questions[key]["antworten"][akey] = {
            "text": aname,
            "effects": {},
            "conditionalEffects": {}
        }

def setEffect(qKey, aKey, code, effect):
    try: 
        updated_questions[qKey]["antworten"][aKey]["effects"][code] += effect
    except KeyError: 
        updated_questions[qKey]["antworten"][aKey]["effects"][code] = effect

def setConditionalEffect(qKey, aKey,  code, condition, effect):
    try:
        updated_questions[qKey]["antworten"][aKey]["conditionalEffects"][code][condition] = effect
        # updated_questions[qKey]["antworten"][aKey]["effects"][code] = "FUNC"
    except KeyError:
        updated_questions[qKey]["antworten"][aKey]["conditionalEffects"][code] = {}
        updated_questions[qKey]["antworten"][aKey]["conditionalEffects"][code][condition] = effect
        # updated_questions[qKey]["antworten"][aKey]["effects"][code] = "FUNC"

def setSpecialCase(code, conditions, case):
    updated_scenarios[code]["special_cases"][conditions] = case

# MASS-POPULATE EFFECTS
for code in list_of_scenarios:
    (art, lehrform, syncInt, asyncTN, asyncInt) = code.split("-")
    # ------------------------
    # - artLV
    # ------------------------
    # artLV: exclude all options not matching the selected LV type
    if art not in ["vl", "so"]:
        setEffect("artLV", "VL", code, -100)
        # updated_questions["artLV"]["antworten"]["VL"]["effects"][code] = -100
    if art not in ["se", "so"]:
        setEffect("artLV", "SE", code, -100)
    if art not in ["pr"]:
        setEffect("artLV", "PR", code, -100)
    if art != "so":
        setEffect("artLV", "SO", code, -100)


    # ------------------------
    # - intSync
    # ------------------------
    # If max synchronous interaction includes small group work (intSync = 2)
    # exclude syncInt=0 or 1
    if syncInt in ["0", "1"]:
        setEffect("intSync", "2", code, -100)
    # favor syncInt=2
    else: 
        setEffect("intSync", "2", code, +1)
        # discourage options with asyncInt=3
        if asyncTN == "3":
            setEffect("intSync", "2", code, -2)
        # exclude fully asynchronous options
        if asyncTN == "4":
            setEffect("intSync", "2", code, -100)

    # If max synchronous interaction is just in plenum (intSync = 1)
    # - exlude syncInt=0 or 2
    if syncInt in ["0", "2"] and lehrform != "async":
        setEffect("intSync", "1", code, -100)
    #favor syncInt=1 :
    else:
        setEffect("intSync", "1", code, +1)
        # - discourage options with asynchronous participation alternative
        if asyncTN == "3":
            setEffect("intSync", "1", code, -1)
        # - discourage fully asynchornous options
        elif asyncTN == "4":
            setEffect("intSync", "1", code, -3)

    # If teaching style ist mostly didactic
    # exclude syncInt=2, favor syncInt=1
    if syncInt == "2":
        setEffect("intSync", "0", code, -100)
    # - promote answers with little asynchronous interaction  
    if syncInt == "0":
        setEffect("intSync", "0", code, +1)
        updated_questions["intSync"]["antworten"]["0"]["effects"][code] = + 1
    
    # ------------------------
    # - leistungen: 
    # ------------------------
    #          referat
    # ------------------------ 
    # exclude/discourage asyncTN=0,3 or 4
    if asyncTN in ["0", "3", "4"]:
        setEffect("referat", "ja", code, -100)
    if asyncTN == "3":
        setEffect("referat", "ja", code, -3)
    # favor asyncTN = 2 (preparing for the presentation)
    if asyncTN == "2":
        setEffect("referat", "ja", code, +1)
    # ------------------------
    #          debate
    # ------------------------ 
    # exclude/discourage asyncTN=0,3 or 4
    if asyncTN in ["0", "4"]:
        setEffect("debate", "ja", code, -100)
    if asyncTN == "3":
        setEffect("debate", "ja", code, -3)
    # favor asyncTN = 2 (preparing for the debate)
    if asyncTN == "2":
        setEffect("debate", "ja", code, +1)
    # ------------------------
    #          praxis
    # ------------------------ 
    # exclude asyncTN=3 or 4
    if asyncTN in ["3", "4"]:
        setEffect("praxis", "ja", code, -100)
    # exclude options without mandatory in-person components
    if lehrform in ["async", "onl", "ringonl", "hyb", "ringhyb2", "onlhybwechs", "hybrem", "grwechshyb"]:
        setEffect("praxis", "ja", code, -100)
    # ------------------------
    #          privat
    # ------------------------ 
    # exclude asyncTN=3 or 4
    if asyncTN in ["3", "4"]:
        setEffect("privat", "ja", code, -100)
    # discourage options with online broadcasting and no mandatory in-person components (risk of sensitive data being recorded)
    if lehrform in ["async", "onl", "ringonl", "hyb", "ringhyb2", "ringhyb1", "onlhybwechs", "hybrem", "grwechs", "grwechshyb"]:
        setEffect("privat", "ja", code, -2)
    # ------------------------
    #          LZiP
    # ------------------------ 
    # exclude asyncTN=3 or 4
    if asyncTN in ["3", "4"]:
        setEffect("LZiP", "ja", code, -100)
    # exclude options without mandatory in-person components
    if lehrform in ["async", "onl", "ringonl", "hyb", "ringhyb2", "onlhybwechs", "hybrem", "grwechshyb"]:
        setEffect("LZiP", "ja", code, -100)
    # ------------------------
    #          keineLeistungen
    #         -----------------
    # if no option is selected, favor options with asynchronous alternative
    if asyncTN in ["3", "4"]:
        setEffect("keineLeistungen", "ja", code, +1)

    # ------------------------
    # - niveauSt
    # ------------------------
    # niveauSt = freshmen
    # discourage scenarios with asynchronous alternatives
    if asyncTN =="4":
        setEffect("niveauSt", "freshmen", code, -2)
    if asyncTN == "3":
        setEffect("niveauSt", "freshmen", code, -1)
    # favor asyncNT=1 and, following that, asyncTN=2 (flipped classroom may be overwhelming as a first-experience)
    if asyncTN == "2":
        setEffect("niveauSt", "freshmen", code, +1)
    if asyncTN == "1":
        setEffect("niveauSt", "freshmen", code, +1.5)
    # discourage fully online scenarios
    if lehrform in ["onl", "ringonl", "onlhybwechs"]:
        setEffect("niveauSt", "freshmen", code, -1)
    # promote in-person scenarios
    if lehrform in ["praes", "rem", "ringpraes", "ringhyb1", "grwechs"]:
        setEffect("niveauSt", "freshmen", code, +1.5)
    # encourage incentivising asynchronous interaction
    if asyncInt == "2":
        setEffect("niveauSt", "freshmen", code, +1)
    # discourage lack of structure whatsoever
    if asyncInt == "0":
        setEffect("niveauSt", "freshmen", code, -1)
    
    # niveauSt = upper (upper Bachelor)
    # favor asyncTN=2>1
    if asyncTN == "2":
        setEffect("niveauSt", "upper", code, +1)
    # discourage asyncTN=0
    if asyncTN == "0":
        setEffect("niveauSt", "upper", code, -1)
    # discourage asyncInt=0
    if asyncInt == "0":
        setEffect("niveauSt", "upper", code, -1)

    # niveauSt = grad (post-Bachelor)
    if asyncTN in ["2", "3" , "4"]:
        setEffect("niveauSt", "grad", code, +1)
    if asyncInt == "1":
        setEffect("niveauSt", "grad", code, +1)


    # ------------------------
    # - limZPSt
    # ------------------------
    # limZPSt=ja: if most students have significant time-limitations:
    #  - discourage flipped-classroom options
    if asyncTN == "2":
        setEffect("limZPSt" , "ja", code, -2)
    #  -  encourage asynchronous alternative options
    if asyncTN in ["3", "4"]: 
        setEffect("limZPSt" , "ja", code, +2)
    # - lightly encourage online and hybrid options (async is already favored above)
    if lehrform in ["hyb", "onl", "ringonl", "ringhyb2", "onlhybwechs", "hybrem", "onlpraeswechs", "hybpraeswechs", "grwechshyb"]:
        setEffect("limZPSt" , "ja", code, +1)
    # - lightly encourage synchronous only options
    if asyncTN == "0":
        setEffect("limZPSt" , "ja", code, +1)
    # avoid incentives to work asynchronously, since most people may miss out
    if syncInt == "2":
        setEffect("limZPSt" , "ja", code, -1)
    
    # limZPSt=idk (I don't know): same effects as "yes" but weaker
        #  - discourage flipped-classroom options
    if asyncTN == "2":
        setEffect("limZPSt" , "ja", code, -1)
    #  -  encourage asynchronous alternative options
    if asyncTN in ["3", "4"]: 
        setEffect("limZPSt" , "ja", code, +1)
    # - lightly encourage online and hybrid options (async is already favored above), controling for LZiP
    if lehrform in ["hyb", "onl", "ringonl", "ringhyb2", "onlhybwechs", "hybrem", "onlpraeswechs", "hybpraeswechs", "grwechshyb"]:
        setEffect("limZPSt" , "ja", code, +0.5)
    # - lightly encourage synchronous only options
    if asyncTN == "0":
        setEffect("limZPSt" , "ja", code, +0.5)
    # avoid incentives to work asynchronously, since most people may miss out
    if syncInt == "2":
        setEffect("limZPSt" , "ja", code, -0.5)

    # limZPSt=nein: if everyone can make it to class synchronously and no one has restricted time plan, no need for high degree of asynchronous materials as a replacement
    if asyncTN in ["3, 4"]:
        setEffect("limZPSt" , "nein", code, +1)
    # if everyone has sufficient time, encourage flipped classroom options, since students can prepare for class and use the time more effectively
    if asyncTN == "2":
        setEffect("limZPSt" , "nein", code, +1.5)
    # also encourage adding incentives to work asynchronously, since most people can take advantage of them
    if syncInt == "2":
        setEffect("limZPSt" , "nein", code, +1)

    # ------------------------
    # - nieSync
    # ------------------------
    # nieSync=ja; if some students cannot regularly make it to class synchronously, then exclude all options where material is exclusively shared synchronously
    if asyncTN == "0":
        setEffect("nieSync", "ja", code, -100)
    # also, discourage options where asynchronous work only complements (but cannot replace) synchronous participation
    if asyncTN == "1":
        setEffect("nieSync", "ja", code, -2.5)
    if asyncTN == "2":
        setEffect("nieSync", "ja", code, -1.5)
    # and encourage asynchronous participation alternatives
    if asyncTN in ["3", "4"]:
        setEffect("nieSync", "ja", code, +1)
    # slightly encourage incentivizing asynchronous interaction (to include the people who can't attend)
    if asyncInt == "2":
        setEffect("nieSync", "ja", code, +0.5)

    # nieSync=idk; if "I don't know" is selected, same effects as "yes" but weaker
    if asyncTN == "0":
        setEffect("nieSync", "idk", code, -2)
    # also, discourage options where asynchronous work only complements (but cannot replace) synchronous participation
    if asyncTN == "1":
        setEffect("nieSync", "idk", code, -0.75)
    if asyncTN == "2":
        setEffect("nieSync", "idk", code, -0.5)
    # and encourage asynchronous participation alternatives
    if asyncTN in ["3", "4"]:
        setEffect("nieSync", "idk", code, +0.25)
    # slightly encourage incentivizing asynchronous interaction (to include the people who can't attend)
    if asyncInt == "2":
        setEffect("nieSync", "idk", code, +0.5)
    # TODO: falls LZsy = 2 und nieSync=ja, es muss eine Anmerkung über dieses Dilemma im Ergebnis angezeigt werden


    # ------------------------
    # - niePr
    # ------------------------
    # if some students can never make it to class in-person, then exclude all options exclusively in-person for students
    if lehrform in ["praes", "ringpraes", "rem", "ringhyb1", "grwechs", "praesonlwechs", "praeshybwechs", "onlpraeswechs", "hybpraeswechs"]:
        # do not exclude options with asynchronous participation alternative
        # exception: if LZiP=ja or praxis=ja, then do not exclude the options with "wechs" - otherwise there is no solution left!
        if asyncTN != "3":
            if lehrform == "hybpraeswechs": 
                setConditionalEffect("niePr" , "ja", code, "LZiP=ja", -1)
                setConditionalEffect("niePr" , "ja", code, "LZiP=nein", -100)
            elif lehrform == "onlpraeswechs":
                setConditionalEffect("niePr", "ja", code, "LZiP=ja", -2)
                setConditionalEffect("niePr", "ja", code, "LZiP=nein", -100)
            else:
                setEffect("niePr" , "ja", code, -100)
        else:
            if lehrform == "hybpraeswechs":
                setConditionalEffect("niePr", "ja", code, "LZiP=ja", -0.5)
                setConditionalEffect("niePr", "ja", code, "LZiP=nein", -2)
            elif lehrform == "onlpraeswechs":
                setConditionalEffect("niePr", "ja", code, "LZiP=ja", -1)
                setConditionalEffect("niePr", "ja", code, "LZiP=nein", -2)
            else: 
                setEffect("niePr" , "ja", code, -2)
    # encourage online and hybrid
    if lehrform in ["onl", "ringonl", "ringhyb2", "hybrem", "onlhybwechs", "hybpraeswechs", "onlpraeswechs", "grwechshyb"]:
        setEffect("niePr" , "ja", code, +1)
    # slightly encourage incentivizing asynchronous interaction (to include the people who can't attend)
    if asyncInt == "2":
        setEffect("nieSync", "ja", code, +0.5)

    # if "I don't know" is selected, similar effect but weaker
    if lehrform in ["praes", "ringpraes", "rem", "ringhyb1", "grwechs", "praesonlwechs", "praeshybwechs", "onlpraeswechs", "hybpraeswechs"]:
        # do not exclude options with asynchronous participation alternative
        if asyncTN != "3":
            setEffect("niePr" , "idk", code, -2)
        else:
            setEffect("niePr" , "idk", code, -0.5)
     # encourage online and hybrid
    if lehrform in ["onl", "ringonl", "ringhyb2", "hybrem", "onlhybwechs", "hybpraeswechs", "onlpraeswechs", "grwechshyb"]:
        setEffect("niePr" , "ja", code, +0.5)
    # slightly encourage incentivizing asynchronous interaction (to include the people who can't attend)
    if asyncInt == "2":
        setEffect("nieSync", "ja", code, +0.5)

    # if answer is no, encouarge in-person options
    if lehrform in ["praes", "ringpraes", "rem", "ringhyb1", "grwechs", "praesonlwechs", "praeshybwechs", "onlpraeswechs", "hybpraeswechs"]:
        setEffect("niePr" , "nein", code, +0.5)


    
    # DEPRECATED # wohnLP: if the instructor lives far from the university, favor online and mostly-online options, unless there are essential learning goals in person!
    # if lehrform in ["onl", "ringonl", "onlhybwechs", "onlpraeswechs", "async"]: 
    #     setConditionalEffect("wohnLP", "nein", code, "LZiP!=2", +1)

    # ------------------------
    # - regAbw
    # ------------------------
    # if instructor is occasionally absent from campus, encourage switching options with more in-person character
    if lehrform in ["praesonlwechs", "praeshybwechs", "hyb", "ringhyb1", "ringhyb2", "hybrem", "hybpraeswechs", "grwechshyb"]: 
        # note: hybrid options also count, because the hybrid room can easily be moved fully online for individual classes
        setEffect("regAbw" , "abundzu", code, 2)
        #TODO: for praeshybwechs, hyb, ringhyb2, hybrem, hybpraeswechs add note about instructor needing to tune in online to an in-person room

    # discourage options where instructor would ALWAYS have to be in person
    if lehrform in ["praes", "ringpraes", "rem", "grwechs"]:
        setEffect("regAbw" , "abundzu", code, -1)

    # if they are regularly absent from campus, enccourage switching options with more online character and fully online options (for the instructor)
    if lehrform in ["onlpraeswechs", "onl", "ringonl", "onlhybwechs"]:
        setEffect("regAbw" , "oft", code, 2)
    # also encourage async options
    if asyncTN == "4": 
        setEffect("regAbw" , "oft", code, 2)
    
    # define special case if the instructor would be tuning in hybridly when they are away
    if lehrform in ["praeshybwechs", "hyb", "ringhyb1", "ringhyb2", "hybrem", "hybpraeswechs", "grwechshyb"]:
        setSpecialCase(code, "regAbw=abundzu", "onlineZuschaltungLP")
        setSpecialCase(code, "regAbw=oft", "onlineZuschaltungLP")


    # ------------------------
    # - onlBereit
    # ------------------------
    # onlBereit: if instructor doesn't want to teach online at all, exclude fully online and switching options
    if lehrform in ["async", "onl", "ringonl", "onlhybwechs", "onlpraeswechs", "praesonlwechs"]:
        setEffect("onlBereit" , "kein", code, -100)
    # if instructor wants to teach online only occasionally:
    # exclude fully online options
    if lehrform in ["async", "onl", "ringonl"]:
        setEffect("onlBereit" , "geleg", code, -100)
    #  discourage options with more than occasional online teaching
    if lehrform in ["onlhybwechs", "onlpraeswechs"]:
        setEffect("onlBereit" , "geleg", code, -1)
    # if instructor wants to teach online as much as possible, encourage options with a higher online portion
    if lehrform in ["onlhybwechs", "onlpraeswechs", "onl", "ringonl"]:
        setEffect("onlBereit" , "viel", code, 2)


    # ------------------------
    # - situations: 
    # ------------------------
    #          gruppenarb
    # ------------------------
    setSpecialCase(code, "gruppenarb=ja", "langfristGrupp")    

    # ------------------------
    #          exkur
    # ------------------------
    if lehrform in ["rem", "hybrem", "hyb", "ringhyb2", "grwechs", "onlhybwechs", "hybpraeswechs", "praeshybwechs", "grwechshyb"]:
        setSpecialCase(code, "exkur=ja", "hybrideExkursion")
    if lehrform in ["onl", "ringonl", "async"]:
        setEffect("exkur", "ja", code, -100)

    # ------------------------
    #          intKoll
    # ------------------------   
    setSpecialCase(code, "intKoll=ja", "international")
    #intKoll: only include remote, online, switching, and hybrid options
    if lehrform not in ["onl", "onlhybwechs", "ringonl", "onlpraeswechs", "ringhyb2", "rem", "hyb", "hybrem", "hybpraeswechs", "grwechshyb"]:
        if asyncTN in ["3", "4"]:
            setEffect("intKoll", "ja", code, -2)
        else: 
            setEffect("intKoll", "ja", code, -100)
    # if not a collaborative course, exclude remote classroom options
    if lehrform in ["hybrem", "rem"]:
        setEffect("intKoll", "nein", code, -100)

    # ------------------------
    #          begrAnz
    # ------------------------ 
    # begrAnz: gruppenwechsel is pointless if everyone can fit in the room
    if lehrform in ["grwechs", "grwechshyb"]:
        setEffect("begrAnz", "nein", code, -100)
        setEffect("begrAnz", "ja", code, +2)
   

    # ------------------------
    # - gaeste
    # ------------------------
    # note: there is currently no special case/ tips for having guests in-person in a non-hybrid environment
    # CASE 1: if no guests are invited: don't display 'ring' formats
    if "ring" in lehrform:
        setEffect("gaeste", "nein", code, -100)
    
    # CASE 2: if guests are only invited in-person:
    # - exclude simple formats without guests (they have corresponding "ring" formats) and 'ringhyb1' (where guest would be online):
    if lehrform in ["praes", "onl", "hyb", "ringhyb1"]:
        setEffect("gaeste", "vorOrt", code, -100)
    # - exclude purely-online formats
    if lehrform in ["ringonl", "async"]:
        setEffect("gaeste", "vorOrt", code, -100)
    # - set special case for guests in-person for all viable formats
    setSpecialCase(code, "gaeste=vorOrt", "gastVorOrtHyb")

    # CASE 3: if guests are only invited online:
    # - exclude simple formats without guests (they have corresponding 'ring' formats)
    if lehrform in ["praes", "onl", "hyb", "ringpraes"]:
        setEffect("gaeste", "virtuell", code, -100)
    # - exclude formats without synchronous online components:
    if lehrform in ["ringpraes", "async"]:
        setEffect("gaeste", "virtuell", code, -100)
    # - set special case for guests online for all viable formats
    setSpecialCase(code, "gaeste=virtuell", "gastOnline")

    # CASE 4: if guests are sometimes online, sometimes in-person:
    # - exclude all simple formats without guests (they have corresponding 'ring' formats)
    if lehrform in ["praes", "onl", "hyb"]:
        setEffect("gaeste", "both", code, -100)
    # - exclude purely in-person and purely online formats:
    if lehrform in ["ringpraes", "ringonl", "async"]:
        setEffect("gaeste", "both", code, -100)
    # - set special cases for both guests online and guests in-person for all viable formats
    setSpecialCase(code, "gaeste=both", "gastVorOrtHyb")   
    setSpecialCase(code, "gaeste=both", "gastOnline")
   


updated_json["questions"] = updated_questions
updated_json["scenarios"] = updated_scenarios
updated_json["special"] = special_cases

json_file = "data.json"
def updateJSON(json_data, json_file):
    with open(json_file, 'w') as json_file:
        json_file.write(json.dumps(json_data, indent=4))
        print("json file created or updated successfully")

updateJSON(updated_json, json_file)
# print(updated_questions["artLV"]["antworten"]["SE"]["effects"]["vl-hybpraeswechs-2-2-1"])


 # Deprecated: onlZugang: if not all students have access to stable internet (for conferencing), exclude all online-only or mandatorily partially online options
    # options with higher online portion
    # if lehrform in ["onl", "ringonl", "onlpraeswechs", "onlhybwechs"]:
    #     # if there is access to asynchronous participation alternative
    #     if asyncTN in ["3", "4"]:
    #         updated_questions["onlZugang"]["antworten"]["nein"]["effects"][code] = -3
    #         updated_questions["onlZugang"]["antworten"]["idk"]["effects"][code] = -2
    #     # if there is NO access to asynchronous participation alternative
    #     else:
    #         updated_questions["onlZugang"]["antworten"]["nein"]["effects"][code] = -100
    #         updated_questions["onlZugang"]["antworten"]["idk"]["effects"][code] = -3
    # # options with smaller online portion
    # if lehrform in ["grwechs", "praesonlwechs"]:
    #     # if there is access to asynchronous participation alternative
    #     if asyncTN in ["3", "4"]:
    #         updated_questions["onlZugang"]["antworten"]["nein"]["effects"][code] = -2
    #         updated_questions["onlZugang"]["antworten"]["idk"]["effects"][code] = -1
    #     # if there is NO access to asynchronous participation alternative
    #     else:
    #         updated_questions["onlZugang"]["antworten"]["nein"]["effects"][code] = -100
    #         updated_questions["onlZugang"]["antworten"]["idk"]["effects"][code] = -2
    # #TODO: if LZsy=0, reduce the negative effect if asyncTN=3 or 4

    # Deprecated: IntAsync: if desired asynchronous interaction is level 1 or 2, exclude options with less interaction.
    # in addition, slightly favor  each interaction level 0,1 or 2 according to what answer was given.
    # if code.split("-")[4] == "0":
    #     updated_questions["IntAsync"]["antworten"]["0"]["effects"][code] = +1
    #     updated_questions["IntAsync"]["antworten"]["1"]["effects"][code] = -100
    #     updated_questions["IntAsync"]["antworten"]["2"]["effects"][code] = -100
    # if code.split("-")[4] == "1":
    #     updated_questions["IntAsync"]["antworten"]["1"]["effects"][code] = +1
    #     updated_questions["IntAsync"]["antworten"]["2"]["effects"][code] = -100
    # if code.split("-")[4] == "2":
    #     updated_questions["IntAsync"]["antworten"]["0"]["effects"][code] = -100
    #     updated_questions["IntAsync"]["antworten"]["2"]["effects"][code] = +1

   # Deprecated: exkurMittel depending on exkurs
    # disourage hybrid options (where some students would never participate in person) if there is enough means to send every student to the excursion
    # if lehrform in ["hyb", "onlhybwechs", "hybrem", "ringhyb2"]:
    #     setConditionalEffect("exkurMittel", "ja", code, "exkur=ja", -1)
    # # favor options with fully-in-person excursion possibility if enough means
    # if lehrform in ["praes", "onlpraeswechs", "ringhyb1", "ringpraes", "hybpraeswechs"]:
    #     setConditionalEffect("exkurMittel", "ja", code, "exkur=ja", +2)
    #     # exlude options where the excursion would definitely have to happen in Person, if not everyone can make it.
    #     if lehrform in ["praes", "ringpraes"]:
    #        setConditionalEffect("exkurMittel", "nein", code, "exkur=ja", -100) 
    # # favor options with hybrid excursion option if not enough means to send everyone
    # if lehrform in ["hyb", "onlhybwechs", "praeshybwechs", "hybrem", "ringhyb2", "hybpraeswechs"]:
    #     setConditionalEffect("exkurMittel", "nein", code, "exkur=ja", +2)

    # deprecated: gaesteMittel: no in-person Ringvorlesung if no means to invite
    # if lehrform == "ringpraes":
    #     updated_questions["gaesteMittel"]["antworten"]["nein"]["effects"][code] = -100
    #     updated_questions["gaesteMittel"]["antworten"]["ja"]["effects"][code] = +1
    # if lehrform == "ringhyb2":
    #     updated_questions["gaesteMittel"]["antworten"]["ja"]["effects"][code] = +1
    # if lehrform in ["ringonl", "ringhyb1", "ringhyb2"]:
    #     updated_questions["gaesteMittel"]["antworten"]["nein"]["effects"][code] = +1

    #Deprecated: modulCombo: do nothing, but will affect previous answers

    # LZiP: if essential learning goals in person and there are no other LV in the module, exclude hybrid and online options.
    # if there are essential goals in person, discourage those options and add note
    # if some nonessential learning goals in person, discourage online options and less so hybrid options
    # if lehrform in ["async", "onl", "ringonl"]:
    #     updated_questions["LZiP"]["antworten"]["2"]["effects"][code] = -100
    #     updated_questions["LZiP"]["antworten"]["1"]["effects"][code] = -2
    #     # setConditionalEffect("LZiP", "2", code, "modulCombo=nein", -100)
    #     # setConditionalEffect("LZiP", "1", code, "modulCombo=nein", -2)
    #     # setConditionalEffect("LZiP", "2", code, "modulCombo=ja", -2)
    #     # setConditionalEffect("LZiP", "1", code, "modulCombo=ja", -1)
    #     updated_questions["LZiP"]["antworten"]["0"]["effects"][code] = +1
    # if lehrform in ["hyb", "ringhyb2", "onlhybwechs", "hybrem"]:
    #     updated_questions["LZiP"]["antworten"]["2"]["effects"][code] = -3
    #     updated_questions["LZiP"]["antworten"]["1"]["effects"][code] = -1
    #     # setConditionalEffect("LZiP", "2", code, "modulCombo=nein", -100)
    #     # setConditionalEffect("LZiP", "1", code, "modulCombo=nein", -1)
    #     # setConditionalEffect("LZiP", "2", code, "modulCombo=ja", -2)
    #     # updated_questions["LZiP"]["antworten"]["0"]["effects"][code] = +1
    #     # setSpecialCase(code, "LZiP=2", "voraussetztenGelPraes")

    # #for online, hybrid and async options, if there are other LV in the same module, add note that the other LV should have in-person elements
    # if lehrform in ["onl", "onlhybwechs", "ringonl", "ringhyb2", "hyb", "hybrem"]:
    #     setSpecialCase(code, "modulCombo=ja+LZiP=2", "alternativPraes")
    #     setSpecialCase(code, "modulCombo=ja+LZiP=1", "alternativPraes")
    
    #TODO: add special case for hybrid excursion
    # if lehrform in ["onlhybwechs", "praeshybwechs", "hyb", "ringhyb2"]:
    #     setSpecialCase(code, "exkur=ja", "hybrideExkursion")

    # TODO: prüfen: was soll passieren, wenn onlZugang=nein und intKoll=ja? Dann würden alle Szenarien ausgeschlossen! Es muss eine Ausnahme erstellt werden.
