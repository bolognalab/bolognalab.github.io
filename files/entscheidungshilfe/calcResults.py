import os
import json
from itertools import product
from collections import Counter
import numpy as np

os.chdir(os.path.dirname(__file__))

# previous entries to update
with open("../../entscheidungshilfe-lehre/data.json", mode='r', encoding='utf-8') as json_file:
    data = json.load(json_file)
    question_info = data['questions']
    scenario_list = list(data['scenarios'].keys())

dummyAnswers = {
    "artLV": "SE",
    "intSync": "2",
    "referat": "ja",
    "debate": "nein",
    "praxis": "nein",
    "privat": "nein",
    "LZiP": "nein",
    # # "keineLeistungen": "nein",
    "niveauSt": "freshmen",
    "limZPSt": "ja",
    "nieSync": "idk",
    "niePr": "ja",
    "regAbw": "abundzu",
    "onlBereit": "egal",
    "gruppenarb": "ja",
    "exkur": "nein",
    "intKoll": "nein",
    "begrAnz": "nein",
    "gaeste": "both"
}

question_answers = dict.fromkeys(dummyAnswers.keys())

# get answers
for qKey in list(question_answers.keys()):
    question_answers[qKey] = []
    for aKey in question_info[qKey]["antworten"].keys():
        question_answers[qKey].append(aKey)

questions = list(question_answers.keys())
answers = list(question_answers.values())
  


def getTopScore(answer_combo):
    topScenarios = {scenario_list[0]:0}
    for i, scenario in enumerate(scenario_list):
        scenario_score = getScore(scenario, answer_combo)
        if scenario_score > max(topScenarios.values()):
            # case 1: override top scenario
            topScenarios = {scenario: scenario_score}
        elif scenario_score == max(topScenarios.values()):
            # case 2: add scenario to top tier
            topScenarios[scenario] = scenario_score
        else:
            # case 3: do nothing
            pass
    return list(topScenarios.keys())

def getScore(scenario, answer_combo):
    score = 0
    for (qKey, aKey) in zip(questions, answer_combo):
        try:
            effect = question_info[qKey]["antworten"][aKey]["effects"][scenario]
        except KeyError:
            effect = 0
        score += effect
    return score

output_histogram = Counter()
for scenario in scenario_list:
    (art, lehrform, syncInt, asyncTN, asyncInt) = scenario.split("-")
    if art not in ["pr", "so"]:
        output_histogram[art + "-" + lehrform] = 0
    # else:
    #     scenario_list.remove(scenario)

i =  0
for combo in product(*answers):
    if i%1000 == 0:
        print(i)
    topTier = getTopScore(combo)
    for topScenario in topTier:
        (art, lehrform, syncInt, asyncTN, asyncInt) = topScenario.split("-")
        if (art not in ["pr", "so"]):
            output_histogram[art + "-" + lehrform] += 1
    i += 1
    # if i >= 100:
    #     break

# combine results into a histogram
import matplotlib.pyplot as plt

labels, counts = zip(*output_histogram.items())

plt.figure(figsize=(max(10, len(labels)//10), 8))
plt.bar(labels, counts)
plt.xticks(rotation='vertical', fontsize=6)
plt.xlabel("Output")
plt.ylabel("Frequency")
plt.title("Histogram of Computed Outputs")
plt.tight_layout()
plt.savefig("test.png", dpi=300)