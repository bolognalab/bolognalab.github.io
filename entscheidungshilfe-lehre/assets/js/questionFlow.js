    function start(){
        document.querySelector("#DIV_TEXT_welcome").classList.add("past")
        setTimeout(()=>{
            document.querySelector("#DIV_TEXT_welcome").style.display="none"
        }, 800)
        displayQuestion(questionOrder[nextQuestionIdx], from='upcoming')
    }

    function hideQuestion(qKey){
        // hiding question container when next question arrives
        let qToHide = document.getElementById("DIV_" + qKey)
        qToHide.classList.remove("upcoming")
        qToHide.classList.add("past")
        if (qKey.includes("TEXT_")){
            // remove buttonContainer, otherwise it will keep getting added!
            setTimeout(()=>{
                qToHide.querySelector(".buttonContainer").remove()
            }, 500)
        }
        // qToHide.style.display = "none"
    }
    function showHideContext(th){
        let a = th.parentElement
        if (a.classList.contains("open")){
            a.classList.remove("open")
            a.querySelector(".contextContent").style.height = "0px"
            a.querySelector(".contextContent").style.visibility="hidden"
        } else {
            a.classList.add("open")
            a.querySelector(".contextContent").style.height = a.querySelector(".contextContent").scrollHeight + "px"
            a.querySelector(".contextContent").style.visibility="visible"
        }
    }
    function displayQuestion(qKey, from="upcoming", addButtons=true, addTitle=false, excludekeys=[]){
        let q, qText, qDiv

        activeQ = qKey
        activeA = null

        if (qKey.includes("TEXT_")){
            // if the panel is just a text block, just display its content
            qDiv = document.getElementById("DIV_" + qKey)
            qDiv.style.display='block'

            // change indicator of parts 1-4
            if (qDiv.querySelector(".sectionTitle")){
                let blockTitle = qDiv.querySelector(".sectionTitle").innerHTML
                let sectionNo = blockTitle.split("Teil ")[1].split(":")[0]
                let blockTitleAdj = blockTitle.split(": ")[1]
                whichPart.innerHTML = blockTitleAdj + " (" + sectionNo + "/4)" 
            }
  
        }
        else {
            // if the panel contains a question, display the question, its answers, and any additional info
            q = questionInfo[qKey]
            qText = q.text
            qDiv = document.createElement("div"); qCont.append(qDiv)
            qDiv.setAttribute("id", "DIV_" + qKey)
            if (from != "start"){
                qDiv.classList.add("qDiv", from)
            } else {
                qDiv.classList.add("qDiv")
            }
            
            if (addTitle){
                // used for adjusting answer at result page; ignored usually
                let t = document.createElement("h3"); qDiv.append(t)
                t.classList.add("addedTitle")
                t.innerHTML = "Antwort ändern"
            }

            let qP = document.createElement("p"); qDiv.append(qP)
            qP.setAttribute("id", "Q_" + qKey); qP.classList.add("qText")
            qP.innerHTML = qText
            
            //adding context
            if (q.addInfo){
                if (qKey == "situations" ||  qKey == "leistungen" || qKey == "interactions"){
                    let context = document.createElement("div"); context.classList.add("context"); qDiv.append(context)
                    context.innerHTML = "<p>*<em>" + questionInfo[qKey]["addInfo"] + "</em></p>"
                } else {
                    let context = document.createElement("div"); context.classList.add("context"); qDiv.append(context)
                    let contextHeader = document.createElement("h5"); context.append(contextHeader)
                    contextHeader.innerHTML = "<img src='images/fwd3.svg' alt=''/><span>Warum fragen wir das?</span>"
                    let contextContent = document.createElement("div"); contextContent.innerHTML="<ul></ul>"; context.append(contextContent)
                    contextContent.classList.add("contextContent")
                    for (var i = 0; i < q.addInfo.length; i++){
                        let ul = contextContent.querySelector("ul")
                        let infoText = q.addInfo[i]
                        let info // will be either p or ul > li
                        // IMPORTANT: currently you can only a single list of statements + optionally a single paragraph statement above them
                        if (infoText.includes("{NO BULLET}")){
                            info = document.createElement('p'); info.innerHTML = infoText.split("{NO BULLET}")[1]; contextContent.insertBefore(info,ul)
                        } else {
                            info = document.createElement('li'); info.innerHTML = infoText; ul.append(info)
                        }
                        
                        // if there are any sources, find them on the list of sources and link them
                        // info.querySelectorAll("a").forEach((a)=>{
                        //     let target = a.getAttribute("href")
                        //     let source = document.querySelector(target)
                        //     let parent = source.parentNode
                        //     a.innerHTML = Array.prototype.indexOf.call(parent.children, source)+1
                        // })
                    }
                    contextHeader.setAttribute("onclick", "showHideContext(this)")
                    }

            }

            if (qKey == "situations" || qKey == "leistungen" || qKey == "interactions"){
                // make all answers 'no' by default - they will be changed if someone checks the box
                Object.keys(questionInfo[qKey]["antworten"]).forEach((a)=>{
                    answers[a] = "nein"
                })
                if (qKey=="leistungen"){
                    answers["keineLeistungen"] = "ja"
                }                
            }

            // add all answers to the question
            Object.entries(q.antworten).forEach((a, idx, array)=>{
                let aKey = a[0]
                let aText = a[1].text
                let aEffects = a[1].effects
                let aConditionalEffects= a[1].conditionalEffects

                let aDiv = document.createElement("div"); qDiv.append(aDiv)
                aDiv.setAttribute("id", "A_" + aKey)
                aDiv.classList.add("aDiv")
                let aRadio = document.createElement("input")

                // for checkbox question, create checkboxes, otherwise radio buttons
                if (qKey == "situations" || qKey == "leistungen" || qKey == "interactions"){
                    aRadio.setAttribute("type", "checkbox")  
                } else {
                    aRadio.setAttribute("type", "radio")
                }
                aRadio.setAttribute("name", "Q_" + qKey)
                aRadio.setAttribute("id", "Q_" + qKey + "_A_" + aKey)
                aRadio.setAttribute("value", aKey)
                aRadio.addEventListener("click", function(){  
                    selectAnswer(qKey, aKey, addButtons)
                })
                let aLabel = document.createElement("label")
                aLabel.setAttribute("for", "Q_" + qKey + "_A_" + aKey)
                aLabel.innerHTML = aText

                aDiv.append(aRadio, aLabel)

                // Exceptions: Answers to not display
                    // hide formats that are not ready yet
                if (aKey =="SO"){
                    aDiv.style.display = "none"
                }
                    // hide least interactive option for Seminars
                if (qKey == "intSync" && aKey == "0" && answers["artLV"]=="SE"){
                    aDiv.style.display = "none"
                }
                    // hide "geringe Raumkapazität" for Vorlesungen
                if (qKey == "situations" && aKey == "begrAnz" && answers["artLV"]!="SE"){
                    aDiv.style.display = "none"
                }    
                    // hide answers explicitly excluded
                if (excludekeys.includes(aKey)){
                    aDiv.style.display = "none"
                }

                // AT THE END OF THE LOOP: For checkbox questions, add "none of the above" as the last answer and highlight it
                if (qKey == "situations" || qKey == "leistungen"){ 
                    if (idx === array.length -1){
                        let aDiv = document.createElement("div"); qDiv.append(aDiv)
                        aDiv.setAttribute("id", "A_none")
                        aDiv.classList.add("aDiv","highlighted")
                        let aRadio = document.createElement("input")
                        aRadio.setAttribute("type", "checkbox")
                        
                        aRadio.setAttribute("name", "Q_" + qKey)
                        aRadio.setAttribute("id", "Q_" + qKey + "_A_none")
                        aRadio.setAttribute("value", "none")
                        aRadio.addEventListener("click", function(){  
                            selectAnswer(qKey, "none", addButtons)
                        })
                        let aLabel = document.createElement("label")
                        aLabel.setAttribute("for", "Q_" + qKey + "_A_none")
                        aLabel.innerHTML = qKey == "situations" ? "Keine der genannten Situationen" : "keine der vorgenannten Leistungen"

                        aDiv.append(aRadio, aLabel)
                    } 
                } 
            })
            

        }

        
        let buttonContainer = document.createElement("div")
        buttonContainer.classList.add("buttonContainer")
        qDiv.append(buttonContainer)
        if (qKey == "TEXT_welcome"){
            buttonContainer.style.display = "none"
        }
        if (addButtons){
            buttonContainer.append(pButton)
            buttonContainer.append(nButton)
            nButton.disabled = qKey=="situations" || qKey=="leistungen" || qKey.includes("TEXT_") && qKey != "TEXT_labore" ? false : true
            pButton.style.display = nextQuestionIdx == 0 || qKey == "TEXT_welcome" ? "none" : "inline"
            nButton.style.display = nextQuestionIdx == 0 ? "none" : qKey == "TEXT_labore" ? "none" : "inline"

            // progress bar: check where we are!
            let progress = questionOrder.indexOf(activeQ)
            for (i=0; i< questionOrder.length; i++){
                if (i<=progress){
                    document.querySelector("#prog_" + i).classList.add("full")
                } else {
                    document.querySelector("#prog_" + i).classList.remove("full")
                }

            }
            // // text on upper left corner
            whichPart.parentElement.removeChild(whichPart)
            qDiv.append(whichPart)
            if (!qKey.includes("TEXT_")){
                whichPart.classList.add("show")
            } else {
                whichPart.classList.remove("show")
            }

            // add either to the bottom or to the top right
            if (qKey.includes("TEXT_")){
                if (qKey == "TEXT_labore" || qKey == "TEXT_welcome"){
                    progressBar.style.opacity=0
                } else {
                    progressBar.style.opacity=1
                }
                
                // progressBar.classList.remove("discreet")
                buttonContainer.append(progressBar)
            } else {
                progressBar.style.opacity=1
                // progressBar.classList.add("discreet")
                // qDiv.append(progressBar)
                buttonContainer.append(progressBar)
            }
            

        }

        setTimeout(function(){
            qDiv.classList.remove("upcoming", "past")
        }, 100)
        
        nextQuestionIdx += 1
    }


    function selectAnswer(qKey, aKey, addButtons=true){
        if (qKey == "situations" || qKey == "leistungen" || qKey == "interactions"){
            let aDiv = document.querySelector("#DIV_" + qKey + " > #A_" + aKey)
            if (aDiv.classList.contains("highlighted") && aKey != "none"){
                aDiv.classList.remove("highlighted")
            } else {
                aDiv.classList.add("highlighted")
            }

        } else {
            // formatting
            document.querySelectorAll("#DIV_" + qKey + " > .aDiv").forEach(function(aDiv){
                aDiv.classList.remove("highlighted")
            })
            document.querySelector("#DIV_" + qKey + " > #A_" + aKey).classList.add("highlighted")
            
        }
        
        // store the answer temporarily (before hitting "next")
        if (qKey!= "situations" && qKey != "leistungen"){
            if (qKey == "interactions"){
                // special case: interactions
                let checked = document.querySelector("#Q_" + qKey + "_A_"+aKey).checked
                // case 1: the option was previously unselected and is being selected
                // case 2: the option was previously selected and is being deselected
                answers[aKey] = checked ? "ja" : "nein"
                // check if there are any options left selected, otherwise prevent deselection
                if (document.querySelectorAll("#DIV_" + qKey + " > .highlighted").length == 0){
                    document.querySelector("#Q_" + qKey + "_A_"+aKey).checked = true
                    setTimeout(()=>{
                        document.querySelector("#DIV_" + qKey + " > #A_" + aKey).classList.add("highlighted")
                    }, 100)
                    document.querySelector("#selectAtLeastOne").style.background = "rgba(117, 208, 131, 0.2)"
                    setTimeout(()=>{
                        document.querySelector("#selectAtLeastOne").style.background = "rgba(18, 161, 154, 0)"
                    }, 2100)
                    answers[aKey] = "ja"
                }
                // update "intSync" answer based on what is checked: 
                let gruppen = answers["gruppen"] == "ja"
                let plenum = answers["plenum"] == "ja"
                answers["intSync"] = gruppen ? "2" : plenum ? "1" : "0"
            } else {
                answers[qKey] = aKey 
            }
        } else {
            // special treatment for checkbox questions
            if (aKey != "none"){
                // normal behavior:
                let checked = document.querySelector("#Q_" + qKey + "_A_"+aKey).checked
                // case 1: the option was previously unselected and is being selected
                // case 2: the option was previously selected and is being deselected
                answers[aKey] = checked ? "ja" : "nein"
                // special case: selecting 'praxis' in the 'leistungen' question also activates 'LZiP'
                if (qKey == "leistungen"){
                    answers["LZiP"] = document.querySelector("#Q_leistungen_A_LZiP").checked ? "ja" : answers["praxis"] == "ja"? "ja" : "nein"
                }
                // check if there are any options left selected, otherwise highlight 'none of the above'
                if (document.querySelectorAll("#DIV_" + qKey + " > .highlighted").length == 0){
                    document.querySelector("#DIV_" + qKey + " > #A_none").classList.add("highlighted")
                    if (qKey=="leistungen"){
                        answers["keineLeistungen"] = "ja"
                    }
                } else {
                    // if other options are selected, deselect 'none of the above' option
                    document.querySelector("#DIV_" + qKey + " > #A_none").classList.remove("highlighted")
                    if (qKey=="leistungen"){
                        answers["keineLeistungen"] = "nein"
                    }
                }


            } else {
                // clicking on "none of the above" cancels everything else
                Object.keys(questionInfo[qKey]["antworten"]).forEach((a)=>{
                    document.querySelector("#DIV_" + qKey + " > #A_" + a).classList.remove("highlighted")
                    answers[a] = "nein"
                })
            }
            
        }
        
        if (addButtons){
            // check if there would be a next question if this answer is selected; if so, enable the "Next Button"
            let includeNextQuestion = false
            let dummyIdx = nextQuestionIdx
            if (dummyIdx >= questionOrder.length){
                document.querySelector("#DIV_" + activeQ + " > .buttonContainer").append(sButton)
                sButton.style.display="inline"
                progressBar.style.opacity=0
                }
            while (dummyIdx < questionOrder.length && includeNextQuestion == false){
                let nextQuestion = questionOrder[dummyIdx]
                
                includeNextQuestion = includeCheck(nextQuestion)
                if (includeNextQuestion){
                    if (sButton.style.display == "inline"){
                        document.body.appendChild(sButton)
                        sButton.style.display="none"
                    }
                    nButton.disabled = false
                    break
                } else {
                    dummyIdx += 1
                }
                // if we reach the end and don't find a valid question, display final submit button
                if (dummyIdx >= questionOrder.length){
                    document.querySelector("#DIV_" + activeQ + " > .buttonContainer").append(sButton)
                    sButton.style.display="inline"
                    progressBar.style.opacity=0
                }
            }            
        }


        activeA = aKey
    }

    function proceedFromQuestion(cq=null){
        let cKey = cq? cq : activeQ
        // check if there is another question left to display and, if yes, do so.
        let includeNextQuestion = false
        while (nextQuestionIdx < questionOrder.length && includeNextQuestion == false){
            let nextQuestion = questionOrder[nextQuestionIdx]
            includeNextQuestion = includeCheck(nextQuestion)
            if (includeNextQuestion){
                hideQuestion(cKey)
                displayQuestion(nextQuestion, from="upcoming")
                break
            } else {
                nextQuestionIdx += 1
            }
        }
    }
    function submitSingleAnswer(qq=null, aa=null, proceed=true, resetRecent=true, verbose=false){
        let qKey = qq? qq : activeQ
        let pKey = qKey
        let aKey = aa? aa : activeA

        if (resetRecent && verbose){
            recent = []
        }
        if (proceed){
            let allRadios = document.getElementById("DIV_" + qKey).querySelectorAll("input")
            for (let radio of allRadios){
                if (radio.id == "Q_" + qKey + "_A_" + aKey){
                    radio.classList.add("selected")   
                }
                radio.setAttribute("disabled", true)
            }
        }

        let effects = questionInfo[qKey]["antworten"][aKey]["effects"]
        let conditionalEffects = questionInfo[qKey]["antworten"][aKey]["conditionalEffects"]

        Object.entries(effects).forEach((entry)=>{
            if (Object.keys(activeScenarios).includes(entry[0])){ //  && entry[1] != "FUNC"){
                let scoreVal = +(activeScenarios[entry[0]])
                newScoreVal = scoreVal + entry[1]
                activeScenarios[entry[0]] = newScoreVal
                recent.push(entry[0])
                // console.log("APPLIED EFFECT,", entry[0], qKey)
            }
        })

        Object.entries(conditionalEffects).forEach((entry)=>{
            let sKey = entry[0]
            let sEffects = entry[1]
        
            Object.entries(sEffects).forEach((sEntry)=>{
                let conditions = sEntry[0]
                let score = sEntry[1]
                // separate conditions if more than one
                let met = andOrCheck(conditions)
                if (met){
                    let scoreVal = +(activeScenarios[entry[0]])
                    newScoreVal = scoreVal + score
                    activeScenarios[entry[0]] = newScoreVal
                    recent.push(sKey)
                    // console.log("APPLIED CONDITIONAL EFFECT,", entry[0], qKey)
                }
            })
            
        })
        if (verbose){
            setTimeout(()=>{
                listActiveScenarios(activeScenarios)
            }, 100)
        }

        if (proceed){
            proceedFromQuestion(pKey)
        }
    
    }
    function submitMultipleAnswers(answersToSubmit, parentQ, isVerbose=false, moveOn=true){
        Object.entries(answersToSubmit).forEach((aEntry, idx, array)=>{
            submitSingleAnswer(aEntry[0], aEntry[1], proceed=false, resetRecent=idx==0, verbose=isVerbose)
            if (idx === array.length -1){
                submitSingleAnswer(parentQ, array[idx-1][0], proceed=moveOn, resetRecent=false, verbose=isVerbose)
            } 
        })
    }

    function undoAnswer(verbose=false){
        // remove current question, unless it's just a text box
        let cQ = document.getElementById("DIV_" + activeQ)
        cQ.classList.add("upcoming")
        if (!activeQ.includes("TEXT_")){
            setTimeout(function(){
            cQ.remove()
        }, 500)
        } else {
            setTimeout(function(){
            cQ.querySelector(".buttonContainer").remove()
        }, 500)
        }

        
        // if user has already selected an answer for the current question and not submitted it:
        // remove the current answer from 'answers' before proceeding
        // note: this doesn't have any effect if the 'question' was just a textbox
        if (activeA){
            if (activeQ && activeQ != "situations"){
                delete answers[activeQ]
            }            
        }
        // for situationsQuestion: delete answer regardless
        if (activeQ == "situations"){
            Object.keys(situationsQuestion["antworten"]).forEach((key)=>{
                delete answers[key]
            })            
        }
        // for interactions question: delete intSync answer
        if (activeQ == "interactions"){
            Object.keys(interactionsQuestion["antworten"]).forEach((key)=>{
                delete answers[key]
            })            
            delete answers["intSync"]
        }

        // get information about the last answered question and change variable activeQ
        if (activeQ == "situations"){
            activeQ = questionOrder[questionOrder.indexOf("situations")-1]
        } else {
            if (Object.keys(situationsQuestion["antworten"]).includes(Object.keys(answers)[Object.keys(answers).length-1])){
                activeQ = "situations"
            } else {
                // note: this works whether we are returning to a textbox or an actual question
                let oneBefore = questionOrder[questionOrder.indexOf(activeQ)-1]
                // oneBefore = Object.keys(answers)[Object.keys(answers).length-1] //this wouldn't work for text boxes, since they don't give answers

                // cases where a previous question/block must be skipped
                if ( oneBefore == "TEXT_labore"){
                    // 1. text about labs coming soon
                    activeQ = "artLV"
                } else if (oneBefore == "anzahlVL" && !answers["anzahlVL"]) {
                    // 2. question anzahlVL if Seminar had been chosen
                    activeQ = "artLV"
                } else if (oneBefore == "anzahlSE" && !answers["anzahlSE"]) {
                    // 3. question anzahlSE if Vorlesung had been chosen
                    activeQ = "anzahlVL"
                } else if (oneBefore == "nieSync" && !answers["nieSync"]){
                    // 4. question nieSync if it should have been skipped
                    activeQ = "limZPSt"
                } else if (oneBefore == "niePr" && !answers["niePr"]){
                    // 5. question niePr if it should have been skipped
                    if (!answers["nieSync"]){
                        // 6. maybe both nieSync and niePr were skipped
                        activeQ = "limZPSt"
                    } else {
                        activeQ = "nieSync"
                    }
                } else if (oneBefore == "labsOnl" && !answers["labsOnl"]){
                    // 7. skip the lab questions if one goes back from the interactions question
                    activeQ = "artLV"
                } else if (oneBefore == "labsHyb" && !answers["labsHyb"]){
                    // 8. skip the labsHyb question if coming from the labsOnl block
                    activeQ = "labFormat"
                } else {
                    // default
                    activeQ = oneBefore
                }                
            }
        }
        
        nextQuestionIdx = questionOrder.indexOf(activeQ)

        activeA = null
        let lastAnswer = {}
        if (activeQ == "situations" || activeQ == "leistungen"){
            Object.keys(questionInfo[activeQ]["antworten"]).forEach((key)=>{
                lastAnswer[key] = answers[key]
            })    
        } else {
            if (activeQ == "interactions"){
                lastAnswer["intSync"] = answers["intSync"]
            } else {
                lastAnswer[activeQ] = answers[activeQ]  
            }
        }

        
        // delete the stored answers of the last answered question
        delete answers[activeQ]
        if (activeQ == "situations" || activeQ == "leistungen" || activeQ == "interactions"){
            Object.keys(questionInfo[activeQ]["antworten"]).forEach((key)=>{
                delete answers[key]
            })
            if (activeQ == "interactions"){
                delete answers["intSync"]
            }     
        }

        function undoAllEffects(qKey, aKey){
            console.log(qKey, aKey)
            recent = []
            // calculate score provided by last answer for each code (but this time subtract it!)
            let effects = questionInfo[qKey]["antworten"][aKey]["effects"]
            let conditionalEffects = questionInfo[qKey]["antworten"][aKey]["conditionalEffects"]

            Object.entries(effects).forEach((entry)=>{
                if (Object.keys(activeScenarios).includes(entry[0])){ // && entry[1] != "FUNC"){
                    let scoreVal = +(activeScenarios[entry[0]])
                    newScoreVal = scoreVal - entry[1]
                    activeScenarios[entry[0]] = newScoreVal
                    recent.push(entry[0])
                    // console.log("REVERSED EFFECT,", entry[0], qKey)
                }
            })

            Object.entries(conditionalEffects).forEach((entry)=>{
                let sKey = entry[0]
                let sEffects = entry[1]
                Object.entries(sEffects).forEach((sEntry)=>{
                    let conditions = sEntry[0]
                    let score = sEntry[1]
                    
                    // separate conditions if more than one
                    let met = andOrCheck(conditions)
                    if (met){
                        let scoreVal = +(activeScenarios[entry[0]])
                        newScoreVal = scoreVal - score
                        activeScenarios[entry[0]] = newScoreVal
                        recent.push(sKey)
                        // console.log("REVERSED CONDITIONAL EFFECT,", entry[0], qKey)
                    }
                })
            })
        }

        if (!activeQ.includes("TEXT_")){
            Object.entries(lastAnswer).forEach((response)=>{
            qKey = response[0]
            aKey = response[1]
            undoAllEffects(qKey, aKey)
        })
        }

        // let qKey = activeQ
        // let aKey = lastAnswer

        // remove previous question and display it again
        if (activeQ.includes("TEXT_")){
            document.getElementById("DIV_" + activeQ).style.display="none"
        }
        else {
            document.getElementById("DIV_" + activeQ).remove()
        }
        displayQuestion(activeQ, from="past")
        
        if (verbose){
            setTimeout(()=>{
                listActiveScenarios(activeScenarios)
            }, 100)
        }
    }

    function getResult(finalResults){
        // decide which scenarios to show!
        topResults = getTopScenarios(finalResults)
        let firstResult = topResults[0]
        window.open("var_result.html?shownScenario=" + firstResult + "&topTier=" + JSON.stringify(topResults), "_self")
    }

    // Auxiliary functions (specialized)
    function getTopScenarios(results){
        shownScenarios = []
        // determine top 3 scores (multiple scenarios can have the same score)
        let firstScore = Math.max(...Object.values(results))
        let topTier = Object.entries(results).filter(([k,v])=>v==firstScore).reduce((r, [k,v])=>[...r,k], []) // returns list of scenarios
        topTier = sortByAsyncInt(topTier)

        let secondScore = Math.max(...Object.values(Object.entries(results).filter(([k,v])=>v<firstScore).reduce((r, [k, v]) => ({ ...r, [k]: v }), {})))
        let secondTier = Object.entries(results).filter(([k,v])=>v==secondScore).reduce((r, [k,v])=>[...r,k], [])
        secondTier = sortByAsyncInt(secondTier)

        let thirdScore = Math.max(...Object.values(Object.entries(results).filter(([k,v])=>v<secondScore).reduce((r, [k, v]) => ({ ...r, [k]: v }), {})))
        let thirdTier = Object.entries(results).filter(([k,v])=>v==thirdScore).reduce((r, [k,v])=>[...r,k], [])
        thirdTier = sortByAsyncInt(thirdTier)
        
        let sc
        for (let i=0; i<(topTier.length + secondTier.length + thirdTier.length); i++){
            // first tier: include all non-duplicates
            if (i<topTier.length){
                let scenarioToAdd = topTier[i]
                sc = getSpecialCases(scenarioToAdd)
                // do not add scenarios with same format hyb, rem, ringonl, etc.
                if (notDuplicate(scenarioToAdd, shownScenarios)){
                    shownScenarios.push(scenarioToAdd+"@"+JSON.stringify(sc))
                }

            } else {
                // second tier: don't consider if score less than zero
                if (i < (topTier.length+secondTier.length) && secondScore>=0){
                    let j = i - topTier.length
                    let scenarioToAdd = secondTier[j]
                    sc = getSpecialCases(scenarioToAdd)
                    if (notDuplicate(scenarioToAdd, shownScenarios)){
                        shownScenarios.push(scenarioToAdd+"@"+JSON.stringify(sc))
                    }

                } else {
                    // third tier: don't consider if score less than zero
                    if (thirdScore>=0){
                        let k = i - topTier.length - secondTier.length
                        let scenarioToAdd = thirdTier[k]
                        sc = getSpecialCases(scenarioToAdd)
                        if (notDuplicate(scenarioToAdd, shownScenarios)){
                            shownScenarios.push(scenarioToAdd+"@"+JSON.stringify(sc))
                        }
                    }

                    }
                }
            if (shownScenarios.length >=maxShownAnswers){
                break
            }     
            
        }
        return shownScenarios
    }

    // get special cases from answers - called just before submitting the answer
    function getSpecialCases(scenario){
        // collects the special cases that should be added to a scenario based on what answers were provided
        let answersToCheck = all_scenarios[scenario]["special_cases"]
        let all_cases_rev = Object.fromEntries(Object.entries(all_special_cases).map(a => a.reverse()))
        let applicableCases = []
        let applicableIndices = []
        Object.entries(answersToCheck).forEach(([r,c], i, arr)=>{
            if (andOrCheck(r)){
                console.log("adding ", c)
                applicableCases.push(c)
                if (Object.values(all_special_cases).includes(c)){
                    applicableIndices.push(Math.floor(all_cases_rev[c]))
                }
            }
        })
        return applicableIndices
    }

    function sortByAsyncInt(arr){
        // Step 1: Group by prefix
        const grouped = {};

        arr.forEach(item => {
        const match = item.match(/^(.*?)-(\d+-\d+-\d+)$/);
        if (!match) return;

        const prefix = match[1];
        const digits = match[2];

        if (!grouped[prefix]) grouped[prefix] = [];
        grouped[prefix].push(digits);
        });

        // Step 2: Sort each group of digits
        Object.keys(grouped).forEach(prefix => {
        grouped[prefix].sort((b, a) => {
            const [a1, a2, a3] = a.split("-").map(Number);
            const [b1, b2, b3] = b.split("-").map(Number);

            if (a1 !== b1) return a1 - b1;
            if (a2 !== b2) return a2 - b2;
            return a3 - b3;
        });
        });

        // Step 3: Recombine into final array, keeping prefix order
        const final = [];
        Object.keys(grouped).forEach(prefix => {
        grouped[prefix].forEach(digits => {
            final.push(`${prefix}-${digits}`);
        });
        });
        return final
    }

    // logic
    function includeCheck(qKey){
        // checks if a question should be displayed
        // assumes that questions have been ordered correctly, otherwise results may be unexpected
        if (qKey == "TEXT_welcome" || qKey == "TEXT_group1"){
            let condition = true
        } else if (qKey == "TEXT_group2" || qKey == "TEXT_group3" || qKey == "TEXT_group4"){
            let condition = "artLV!=PR"
            return andOrCheck(condition)
        } else {
            let condition = questionInfo[qKey]["condition"]
            if (condition == true){
                return true
            } else {
                return andOrCheck(condition)
            }
        }        
    }

    function andOrCheck(conditionString) {
        const orGroups = conditionString.split("|");

        for (let group of orGroups) {
            const conditions = group.split("+");
            let allTrue = true;

            for (let condition of conditions) {
                let isNegation = condition.includes("!=");
                let [qKey, aKey] = isNegation
                    ? condition.split("!=")
                    : condition.split("=");
                if (isNegation) {
                    if (answers[qKey] === aKey) {
                        allTrue = false;
                        break;
                    }
                } else {
                    if (answers[qKey] !== aKey) {
                        allTrue = false;
                        break;
                    }
                }
            }

            if (allTrue) return true; // at least one OR group passed
        }

        return false; // none of the OR groups passed
    }

    function notDuplicate(newScenario, shownScenarios){
        sType = newScenario.split("-")[1]
        if (shownScenarios.map((str)=>str.split("-")[1]).includes(sType)){
            // if the type of scenario is the same, still include if there is asynchronous participation alternative for one scenario
            let matchingScenarios = shownScenarios.filter((str)=>str.split("-")[1] == sType)
            if (matchingScenarios.length > 1){
                // can't add same scenario a third time!
                return false
            }
            let matchingScenario = matchingScenarios[0]
            let asyncNew = newScenario.split("-")[3] // asynchronous participation mode of new scenario
            let asyncMatching = matchingScenario.split("-")[3] // asynchronous participation mode of matching scenario
            if ([asyncNew, asyncMatching].includes("3") && asyncNew != asyncMatching){
                return true
            } else {
                return false
            }
        } else {
            return true
        }
    }