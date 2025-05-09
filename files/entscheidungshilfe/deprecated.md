Begründung der Entscheidung mit Wörtern (formerly at var_result.html)
```html
            <div id="matchQuality" style="display:none; border-bottom: 0px" class="tip">
                <h5 onclick="showHideTip(this)">
                    <img src="images/fwd3.svg" alt="">
                    <span>Wie geeignet ist dieses Lehrszenario für mich?</span>
                </h5>
                <div class="tipContent">
                    <div id="vorteile" style="display: none">
                        <p>Hier sind einige Gründe, warum dieses Szenario gut für Sie ist:</p>
                        <ul class="reasonList"></ul>
                    </div>
                    <div id="nachteile" style="display: none">
                        <p>Hier sind einige Aspekte des Szenarios, die vielleicht nicht direkt mit Ihren Erwartungen übereinstimmen:</p>
                        <ul class="reasonList"></ul>
                    </div>
                </div>

            </div>
```
```js

$.get("regeln_formulierungen.csv", function(CSVdata){
    rule_data =  $.csv.toObjects(CSVdata, {separator:';'});
    // explainMatch(shownScenario, answers, rule_data)  
})

function explainMatch(scenario, answers=dummyAnswers, rules=[]){
    Object.entries(answers).forEach(function(item){
        let qCode = item[0]
        let aCode = item[1]
        let effectsForThisCombination = rule_data.filter((k)=>k.questionCode==qCode && k.answerCode==aCode)
        for (let effect of effectsForThisCombination){

            if (!isScenarioAffected(shownScenario, effect)){
                // only include effects that affect the displayed scenario!
                continue;
            }
            if (effect.scoreChange == "-100" || effect.scoreChange == "-"){
                // ignore effects that would have excluded this scenario and "noEffect"
                continue;
            } 
            if (effect.relevantVariable1 == "2" || effect.relevantVariable1 =="4"){
                // ignore effects that just define syncInt and asyncInt
                continue;
            }
            let sentence = document.createElement("li")
            let subsentence = effect.reasonSummary.replace("Szenario XYZ", "dieses Szenario")
            sentence.innerHTML = effect.answerSummary + " " + subsentence //+  " <b>(rule ID: " + effect.globalId + ")</b>"

            // if the effect is positive, add it to the first list (Vorteile)
            if (+effect.scoreChange > 0){
                document.querySelector("#vorteile .reasonList").append(sentence)
                document.querySelector("#matchQuality").style.display = "block"
                document.querySelector("#vorteile").style.display = "block"
            } else {
                // if the effect is negative, add it to the second list (Nachteile)
                document.querySelector("#nachteile .reasonList").append(sentence)
                document.querySelector("#matchQuality").style.display = "block"
                document.querySelector("#nachteile").style.display = "block"
            }            
        }
    })
    console.log("hallo")
}
// auxiliary functions for reading rules
function isScenarioInRange(scenarioCode, variable, range){
    // console.log(scenarioCode, variable, range)
    let scenarioVariable = scenarioCode.split("-")[variable]
    // turning the contents of the csv file into a list of strings
    let rangeList = $.csv.toArray(range).map(str => str.trim())
    return rangeList.includes(scenarioVariable)

}
function isScenarioAffected(scenarioCode, effect){
    // console.log(effect)
    let variable1 = effect.relevantVariable1, variable2 = effect.relevantVariable2
    let inRange1 = effect.includedRange1, inRange2 = effect.includedRange2
    let exRange1 = effect.excludedRange1, exRange2 = effect.excludedRange2
    // console.log(variable1, variable2, inRange1, inRange2, exRange1, exRange2)

    let match1 = variable1 == "-" ? true : isScenarioInRange(scenarioCode, variable1, inRange1)
    let match2 = variable1 != "-" && exRange1 == "-" ? false : !isScenarioInRange(scenarioCode, variable1, exRange1)
    let match3 = variable2 == "-" ? true : isScenarioInRange(scenarioCode, variable2, inRange2)
    let match4 = variable2 != "-" && exRange2 == "-" ? false : !isScenarioInRange(scenarioCode, variable2, exRange2)

    // console.log(match1, match2, match3, match4)
    return (match1 || match2) && (match3 || match4)

}
```