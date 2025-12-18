# Entscheidungshilfe Online & Hybride Lehre
*ein Tool des Berliner Netzwerks Hybride Lehre*

## Impressum
Software-Programmierung: Natalia Spitha*
Fragenkatalog & Didaktik: Natalia Spitha & Judith Stelter**
Raumkonzepte: Philipp Kapser*

*Humboldt-Universität zu Berlin
**Berliner Hochschule für Technik

Entwickelt im Rahmen des berlinweiten Verbundprojekts "Netzwerk Hybride Lehre" (Land Berlin / QIO 2022-2025)

Der Quellcode ist unter der GNU General Public License Version 3.0 (GPL-3.0) lizenziert. Alle originalen Texte und Bilder stehen – sofern nicht anders angegeben – unter der Creative Commons Namensnennung – Weitergabe unter gleichen Bedingungen 4.0 International Lizenz (CC BY-SA 4.0).

## Zielgruppe
### Ziel und Zielgruppe des Tools

Der Entscheidungsbaum richtet sich an Lehrende (nicht nur HU-Lehrende), die eventuell eine Lehrveranstaltung (LV) in einem neuen Format als vorher unterrichten möchten (Use-Case 1) oder schon das Format kennen (Use-Case 2) und didaktische und technische Tipps für die Durchführung durchlesen möchten. Für Use-Case 1 hilft der Entscheidungsbaum den Lehrenden, je nach ihren Präferenzen und anderen Voraussetzungen ein passendes Lernszenario für sich zu finden (online, hybrid, vor Ort, oder abwechselnd). Für Use-Case 2 wählt die Lehrende Person das Lernszenario im Voraus und beantwortet ein paar zusätzliche Fragen (z.B. wie viel studentische Interaktion gewünscht ist). Bei beiden Use-Cases erhält die Lehrende Person am Ende didaktische und technische Tipps im Zusatz zu Informationen über das Lehr-Lernszenario.

### Ziel und Zielgruppe dieser Dokumentation
Diese Dokumentation dient dem Verständnis der "Backend"-Struktur des Tools, ohne das Programmierkenntnisse in JavaScript oder Python benötigt wird. Anhand dieser Dokumentation sollte jemand in der Lage sein, Texte in dem Entscheidungstool zu bearbeiten und Texte/Tipps zuzuordnen, sowie die Frage-Formulierungen anpassen. Diese Inhalte befinden sich hauptsächlich in ``.csv`` und ``.json``-Dateien, die bearbeitet werden können. Das hinzufügen von neuen Fragen, Antwortmöglichkeiten, Funktionen oder anderen Inhalten benötigt mindestens ein Grundverständnis von JavaScript, Python, HTML und CSS. 

## Vorschau

URL zur letzten Version: <https://bolognalab.github.io/entscheidungshilfe-lehre/app.html> oder <https://pages.cms.hu-berlin.de/netzwerk-hybride-lehre/entscheidungstool>

Direkt zu einem Beispiel-Ergebnis: <https://bolognalab.github.io/entscheidungshilfe-lehre/var_result.html>

Mit „Programm“ wird unten die HTML-Seite des Entscheidungsbaums gemeint, die auf Github gehostet ist.

## Struktur

### Ergebnisse des Entscheidungsbaums

#### Lehr- / Lernszenarien

Es werden grundsätzlich 33 verschiedene Lehr-/Lernszenarien als Ergebnisse des Entscheidungsbaums abgebildet (14 “Vorlesungen”, 15 “Seminare” und 4 “Praktika” und “Sonstige”). Für jedes Szenario sind viele unterschiedliche Kombinationen **der folgenden drei Variablen**, möglich, weshalb sich am Ende ganz viele (über 800) mögliche Ergebnisse aus dem Entscheidungsbaum ergeben könnten:

- **Umfang der synchronen Interaktion (Variabel ``syncInt``)**: wie viel Interaktion innerhalb der Sitzungen der LV stattfindet:
  - 0 = gering – nur gelegentliche Interaktivität (frontaler Unterricht)
  - 1 = mittlere - aktive Beteiligung der Studierende, allerdings keine intensive Gruppenarbeit
  - 2 = hohe - aktive Beteiligung und regelmäßige Gruppenarbeit
- **Anteil der asynchronen Teilnahme (Variabel ``asyncTN``):** welchen Anteil bzw. welche Komponenten der LV online stattfinden:
  - 0 = exklusiv synchron
  - 1 = ergänzende Materialien für Nacharbeit
  - 2 = ergänzende Materialien für Vor- (Flipped Classroom) und Nacharbeit
  - 3 = asynchrone Teilnahme als möglicher Ersatz der synchr. Teilnahme
  - 4 = exklusiv asynchron
- **Umfang der asynchronen Interaktion (Variabel ``asyncInt``)**: wie viel studentische Interaktion außerhalb der Kurssitzungen gewünscht ist und inwieweit die Lehrperson diese Interaktion strukturieren möchte
  - 0 = minimal; keine Strukturierung der asynchronen Interaktion für Studierende und minimale Bereitstellung von Ressourcen dafür. Die asynchrone Interaktion besteht hauptsächlich in dem Konsum/Nachlesen von Materialien
  - 1 = Bereitstellung von Strukturen für Interaktion individueller Studierenden mit der Lehrperson oder mit Feedback-Tools
  - 2 = Bereitstellung von Strukturen für individuelles Feedback und für Peer-Interaktion 

Die drei Variablen beeinflussen, welche Tipps im Ergebnis angezeigt werden. Anmerkung: manche Kombinationen sind aus logischen Gründen nicht möglich (z.B. ``asyncTN = 0`` & ``asyncInt =2``).

Jedes mögliche Ergebnis wird im Programm mit einem Code \[xx-yy...y-#-#-#\] beschrieben (z.B. vl-praes-2-1-2), der diese Parameter berücksichtigt:

| Parameter<br>\[``kurznotation``\] | Art der LV | Format | Synchrone Interaktion  <br>\[``syncInt``\] | Asynchrone Teilnahme<br><br>\[``asyncTN``\] | Asynchrone Interaktion  <br>\[``asyncInt``\] |
| --- | --- | --- | --- | --- | --- |
| Bsp: | Vorlesung | in Präsenz | hohe synchrone Interaktion | ergänzende Nacharbeit | St-LP und St-St |
| Code: | ``vl`` | ``praes`` | ``2``| ``1`` | ``2`` |

Die aktuelle Liste der Lernszenarien (alle Kombinationen) befindet sich in der Datei [**szenarien.csv**](https://github.com/bolognalab/bolognalab.github.io/blob/main/entscheidungshilfe-lehre/szenarien.csv/).

#### Ergebnisseiten direkt testen:
Um eine Ergebnisseite direkt anzuzeigen (z.B. um zu überprüfen, ob sie ordnungsgemäß funktioniert), kann die URL der Ergebnisseite mit der Code eines Szenarios ergänzt werden, z.B.:
```
...entscheidungshilfe-lehre/var_result.html?shownScenario=se-hyb-2-2-2
```

Es ist auch möglich, die Anzeige der **Sonderbedingungen** (s.u.) auszulösen, indem Sie die entsprechenden Nummern wie folgt in eckige Klammern setzen. Zum Beispiel entspricht die nummer 0 die Sondernbedingung zur Internationalen Kollaboration:
```
...entscheidungshilfe-lehre/var_result.html?shownScenario=se-hyb-2-2-2@[0]
```
Die Nummer, die jeder Sondernbedingung zugeordnet sind, können in der Datei ``setQuestionsAndRules.py`` gesehen werden. Mehrere Sonderbedingungen können zur URL mit Kommas hinzugefügt werden, z.B. ``@[0,5]``.

Nicht zuletzt können auch "Weitere Ergebnisse" gezeigt werden, indem ein "Top Tier" zur URL hinzugefügt werden, z.B.:

```
...entscheidungshilfe-lehre/var_result.html?shownScenario=se-hyb-2-2-2@[0]&topTier=["se-hyb-2-1-2@[0]", "se-hyb-2-2-2@[0]", "se-hybrem-2-1-2@[0]"]
```

#### Blöcke

Jedes angezeigte Ergebnis des Entscheidungsbaums wird in mindestens **5 Blöcken** aufgeteilt (s. Abbildung), jeder mit einem kleinen Text und Inhalten wie Tipps. Die Blöcke sind folgende:  

- **Titel**  
    Der Titel des Lernszenarios wird wie von der Datei **texts_tips_matrix.xlsx** (im Programm ist das eine CSV-Datei, text_tips_matrix.csv) aufgerufen. Anmerkung: der Titel ändert sich in der Regel nicht, wenn die Variablen für synchrone Interaktion (_syncInt_), asynchrone Teilnahme (_syncTN_) oder asynchrone Interaktion (_asyncInt_) sich ändern – es hängt nur von der Art der LV und dem „Format“ ab, mit _einer Ausnahme:_ wenn die Variable für asynchrone Teilnahme den Wert von 3 hat („asynchrone Teilnahme als möglicher Ersatz der synchronen Teilnahme“), dann erscheint als Untertitel der Text „mit asynchroner Teilnahme-Alternative“, damit es für die Lehrperson deutlicher wird.  

- **Block 1 - Übersicht:**  
    Hier steht ein Beschreibungstext des Lehr-Lernszenarios und idealerweise auch ein schönes, repräsentatives Bild dazu. 

- **Block 2 – Medientechnische Voraussetzungen**
    Hier werden in Textform wichtige Raum- und Medientechnikvoraussetzungen kurz beschrieben, die mithilfe von Bildern und 3D-Raummodellen abgebildet werden. Zusätzlich können für bestimmte Fälle Links zu interessanten Beispiele oder neue, inspirierende Raumkonzepte angegeben werden. In manchen Fällen (z.B. Labore hat dieser Block einen anderen Titel.)

- **Block 3 – Tipps für die synchrone Interaktion**  
    Hier steht ein kleiner Text, der den Umfang der synchronen Interaktion (je nach den Angaben der Lehrenden) grob erklärt. Nebenbei erscheinen Tipps für die synchrone Interaktion. Die Inhalte dieses Blocks hängen hauptsächlich von dem Parameter „Synchrone Interaktion“ des Ergebnisses (erste der drei Zahlen im Code).  

- **Block 4 – Tipps für die Kursplanung**
    Hier wird ein Überblick der asynchronen Teilnahme und Interaktion gegeben zusammen mit Tipps für die Strukturierung der asynchronen Kurskomponenten. Die Inhalte dieses Blocks hängen sowohl von dem Parameter „Asynchrone Teilnahme“ und dem Parameter „Asynchrone Interaktion“ ab (zweite und dritte Zahl im Code).  


- **Block 5 – Weitere Ergebnisse**  
    Hier werden alternative Szenarien gezeigt, falls sie auch je nach den Angaben der Nutzer\*innen relevant sind. Der Text dazu ist immer gleich „Folgende Lehr-/Lernszenarien könnten auch für Sie passend sein:“


#### Texte und ihre Zuordnung

Die Texte für Blöcke 1-4 (in HTML-Format, inkl. Tags) sowie die Information zur modularen Zuordnung der Tipps befinden sich in der Quelldatei [texts_tips_matrix.csv](https://github.com/bolognalab/bolognalab.github.io/blob/main/entscheidungshilfe-lehre/texts_tips_matrix.csv) und werden automatisch je nach den Parametern des Ergebnisses abgerufen und angezeigt. In der Quelldatei enthalten die ersten zwei Spalten der Tabelle das allgemeine Format des Szenarios und die anderen Spalten (bis zur Spalte "raum_syncInt-2") die Texte bzw. Links, die in jedem Block passen. Weil der angezeigte Text von den Werten der Parameter ``syncInt``, ``asyncTN`` und ``asyncInt`` abhängt, gibt es für jedes allgemeine Format verschiedene Alternativen, die angezeigt werden, wenn eine bestimmte Variable einen bestimmten Wert hat, z.B.:

Tabelle 1 - Struktur der Datei "texts_tips_matrix" (für Texte) mit einem Beispiel

| A   | B   | C   | D   | _..._ | I   | _..._ |
| --- | --- | --- | --- | --- | --- | --- |
| **wert** | **Name** | **text_overview** | **text_syncInt-0** | **_…_** | **text_asyncTN-2** | **_…_** |
| de-default | Standardszenario  <br>(Im Standardszenario sind Texte gespeichert, die in allen Szenarien verwendet werden können) | Dieser Text sollte nie angezeigt werden, solange alle Szenarien unten einen Überblicktext haben! | Wenn syncInt=0, wird dieser Text in Block 2 angezeigt. Wenn in dieser Spalte für ein bestimmtes Szenario ein anderer Text steht, wird der szenariospezifische Text diesen Text überschreiben. | …   | Wenn asyncTN=2, wird dieser Text in Block 3 angezeigt. Wenn in dieser Spalte für ein bestimmtes Szenario ein anderer Text steht, wird der szenariospezifische Text diesen Text überschreiben. | …   |
| vl-rem | Standort-übergreifende Kollaborative Vorlesung (Partnerkurse) | Dieser Text wird für alle Ergebnisse mit „vl-rem-#-#-#“ in Block 1 erscheinen. | \-  | …   | Dieser Text wird den oberen Text überschreiben. | …   |
| …   | …   | …   | …   | …   | …   | …   |


Im Quellcode werden unterschiedliche Teile der Datei "texts_tips_matrix" unterschiedlich behandelt, weshalb die Information in der CSV-Datei nicht immer ohne Kontext gut zu verstehen ist. Manchmal werden z.B. bei den mit dem medientechnischen Block bezogenen Spalten Formulierungen in spitzen Klammern verwendet; die spezielle Funktionen des Programms "aktivieren", e.g. 
* *\<\<COMING SOON\>\>* = hier muss ein bestimmter Text angezeigt werden, der sagt, dass Information folgt
* *\<\<FULLIMG\>\>* = hier muss ein Bild anstatt von einem Sketchfab Link angezeigt werden, oder 
* *\<\<DIGITAL\>\>* = hier handelt es sich um ein Online-Konzept (ohne medientechnischen Block)

Wenn man also den Inhalt der Texte korrigieren oder ergänzen möchte, würde man die Quelldatei [texts_tips_matrix.csv](https://github.com/bolognalab/bolognalab.github.io/blob/main/entscheidungshilfe-lehre/texts_tips_matrix.csv) bearbeiten und **IMMER am Ende lokal testen**, dass alles richtig angezeigt wird. 


#### Tipps und ihre Zuordnung

Für jedes Lehr-/Lernszenario erscheinen im Ergebnis eine bestimmte Reihe von didaktischen Tipps. Die Tipps sind in zwei Blöcken kategorisiert, einer „für die synchrone Interaktion“ und einer „für die asynchrone Teilnahme.“ Unter bestimmten „Spezialfällen“ (s. unten) können auch zusätzliche Blöcke mit Tipps erscheinen.

Der Inhalt jedes Tipps wird in einer Datei Namens [tips_source.json](https://github.com/bolognalab/bolognalab.github.io/blob/main/entscheidungshilfe-lehre/tips_source.json) gespeichert. Die folgende Abbildung erklärt (hoffentlich!) den Aufbau dieser Datei. Wenn man diese Datei ändern möchte, könnte lokal die HTML-Datei [files/entscheidungshilfe/tippsDisplay.html]((https://github.com/bolognalab/bolognalab.github.io/blob/main/files/entscheidungshilfe/tippsDisplay.html)) als Vorschau benutzt werden, die die Inhalte der json-Datei veranschaulicht. **Das ersetzt nicht die Notwendigkeit, nach jeder Bearbeitung der tips_source.json-Datei die Ergebnisseiten ausführlich zu testen!** :) 


![](dokumentation/img_tipStructure.png)
*Abbildung 2. Aufbau der Datei tips_source.json*

Die Information, welcher Tipp zu welchem Lehr-/Lernszenario unter welchen Bedingungen passt, wird durch die Datei [texts_tips_matrix.csv](https://github.com/bolognalab/bolognalab.github.io/blob/main/entscheidungshilfe-lehre/texts_tips_matrix.csv) festgelegt (wo auch die Texte sich befinden). Da werden unter verschiedene Spalten die Codes der Tips (z.B. „privateEcke“) aufgelistet, die erscheinen sollen.

Tabelle 2. Struktur der Datei "texts_tips_matrix" (für Tipps)

| A   | ... | O   | P   | _..._ | U   | _..._ |
| --- | --- | --- | --- | --- | --- | --- |
| **wert** | **…** | **tips_general** | **tips_syncInt-0** | **_…_** | **tips_asyncTN-2** | **_…_** |
| de-default | ... | (nicht genutzt) | [TippCodes, die bei allen Ergebnissen erscheinen, wo syncInt=0] | ... | [TippCodes, die bei allen Ergebnissen erscheinen, wo asyncTN=0] | ... |
| ... | ... | ... | ... | ... | ... | ... |
| vl-rem | …   | \[Tippcodes von Tipps, die _immer_ bei diesem Lehrformat erscheinen sollen\] | \[Tippcodes, die bei diesem Lehrformat erscheinen sollen, wenn syncInt=0\] | …   | \[Tippcodes, die bei diesem Lehrformat erscheinen sollen, wenn asyncTN=2\] | …   |
| …   | …   | …   | …   | …   | …   | …   |

Es ist wichtig für das Programm, dass die Tippcodes in einer Zelle der Tabelle mit Komma und einzelnem Leerzeichen getrennt sind, und _genau_ die Codes in der Datei **tips_source.json** anpassen, z.B.

privateEcke, warteZeitHyb, darstellungsformen

Hier werden ebenfalls spitze Klammern verwendet (*\<\<excludeDefault>>*), wenn man z.B. die von der *default*-Reihe zugeordneten Tipps ausnahmsweise deaktivieren will. 

#### Medientechnische Voraussetzungen
Die Organisation der Informationen zu Medientechnik in Dateien unterscheidet sich zwischen Labor- und anderen Formaten. Im Moment werden verschiedenen vor-Ort- und hybriden Szenarien Text und URL-Links für Raumkonzepte (die auf Sketchfab hochgeladen wurden) zugeordnet. Die Zuordnung wird in der Datei [texts_tips_matrix.csv](https://github.com/bolognalab/bolognalab.github.io/blob/main/entscheidungshilfe-lehre/texts_tips_matrix.csv) definiert.

#### Spezialfalle (Special Cases)
Zwischen Blöcken 4 (Tipps für die asynchrone Teilnahme) und 5 (Weitere Ergebnisse) können ggf. zusätzliche Tipps/Texte für bestimmte Sonderfallen angezeigt werden. Hier wird qualitativ beschrieben, was bei den verschiedenen Spezialfällen passieren sollte.

<table><tbody><tr><th><p><strong>Fall</strong></p></th><th><p><strong>Implementiert?</strong></p></th></tr><tr><td><p><strong>Internationale Kollaboration (hybride Exkursion)</strong></p><ul><li>Ein Zusätzlicher Block „Tipps für internationale Kollaboration“ soll erscheinen</li><li>In dem Block „Tipps für internationale Kollaboration“ werden Tipps hinzugefügt, die in der Datei <strong>tips_source.json</strong> mit „type“: „international“ bezeichnet werden.<ul><li>Mehrsprachigkeit: Für Videoaufzeichnungen wo möglich Live-Untertitelung nutzen (-&gt; viele VC Systeme können das, ob die Funktion nutzbar/aktiviert ist, muss mit IT Services geklärt werden). Englisch i.d.R. gut, Deutsch geht so, Wechsel zwischen zwei Sprachen schwierig.</li><li>Übersetzungen: Live Übersetzung sind meistens noch ein zusätzlicher, kostenpflichtiger Service oder datenschutzrechtlich problematisch. Dokumente können asynchron zur Sinnerfassung inzwischen gut mit DeepL übersetzt werden (https://www.deepl.com/de/translator)</li><li>Dokumentation: Die meisten VC Plattformen können inzwischen automatisch Transkripte von Videokonferenzen generieren. Das funktioniert mit Englisch ganz gut, mit anderen Sprachen mäßig. Achtung: Die Software kann nur Beiträge der Online-Teilnehmer:innen namentlich zuordnen; bei Aufnahmen aus dem analogen Raum fällt im Nachhinein die Unterscheidung zwischen verschiedenen Sprecher:innen/Beiträgen schwer. Als wörtliche Mitschrift sind die Skripte sehr umfangreich und aufwendig in der Überarbeitung.</li></ul></li></ul></td><td><p>Ja</p></td></tr><tr><td><p><strong>Hybride Exkursion (hybrideExkursion)</strong></p><ul><li>Ein Zusätzlicher Block „Tipps für Hybride Exkursionen“ soll erscheinen</li><li>Tipps werden für den Fall geschrieben; Quelle; <a href="https://www.e-teaching.org/praxis/hybride-lernraeume/stellvertreterexkursion">https://www.e-teaching.org/praxis/hybride-lernraeume/stellvertreterexkursion</a></li></ul></td><td><p>Ja</p></td></tr><tr><td><p><strong>Online-Zuschaltung Lehrperson<br></strong>(Die Lehrperson ist online zugeschaltet, während Studierende mit einer moderierenden Person im Lehrraum sind)</p><ul><li>Zusätzliche Tipps werden im Block für die synchrone Teilnahme hinzugefügt.<ul><li>Technik-Check vor der LV</li><li>Studierende als Moderator:innen vor Ort</li></ul></li></ul></td><td><p>Ja</p></td></tr></tbody></table>

<a id="contentSrcs"></a>
#### Abbildung: Beispiel Szenario und Quellen verschiedener Inhalte

Für das abgebildete Szenario **se-rem-1-1-0:**


### Fragen und Entscheidungen

#### Inhalte der Fragen

Die Fragen und Antworten können in der Datei [fragen_source.json](https://github.com/bolognalab/bolognalab.github.io/blob/main/entscheidungshilfe-lehre/fragen_source.json). Eine Frage wird durch das folgende beschrieben (s. Abbildung):

- Einen für die Nutzer\*innen unsichtbaren **Fragecode** (z.B. „onlBereit“)
- Eine Bedingung (**_condition_**) dafür, wann die Frage erscheint (je nachdem, wie frühere Fragen beantwortet wurden) – _true_ heißt, die Frage erscheint immer
- Den **text** der Frage
- Eine Reihe von **antworten**. Jede Antwort hat einen für die Nutzer\*innen unsichtbaren **Antwortcode** (z.B. „kein“, „geleg“) und einen Text. Die Texte für die Frage und Antworten unterstützen Formatierung durch HTML, z.B. &lt;b&gt;&lt;/b&gt; für bold.
- Eventuell einen Satz als zusätzliche Information (**addInfo**), welche die Frage länger erklärt.
*TODO: Dieses "addInfo" Element wird weiterentwickelt, weil inzwischen festgestellt wurde, dass für die sinnvolle Beantwortung der Fragen mehr Kontext notwendig ist.*

![](dokumentation/img_questionComponents.png)
*Abbildung 4. Eine Beispiel-Frage in der Datei fragen_source.md und ihre Abbildung im Entscheidungsbaum-App*

Anmerkung 1: die _Reihenfolge_ der Fragen wird nicht durch diese Datei bestimmt, sondern sie wird durch eine andere Datei ([app.html](https://github.com/bolognalab/bolognalab.github.io/blob/main/entscheidungshilfe-lehre/app.html)) definiert. Dort gibt es die Javascript-Variable ``questionOrder``, welche die Codes der verwendeten Fragen in der gewünschten Reihenfolge auflistet.

**Anmerkung 2 (Wichtig!): manche Fragen in der Datei [fragen_source.json](https://github.com/bolognalab/bolognalab.github.io/blob/main/entscheidungshilfe-lehre/fragen_source.json) sind nicht mehr im Entscheidungstool implementiert!!!** Diese Datei dient auch als Archiv für ältere Fragen. Die aktuellste Auswahl der Fragen wird (wie die Reihenfolge) in der Datei [app.html](https://github.com/bolognalab/bolognalab.github.io/blob/main/entscheidungshilfe-lehre/app.html) definiert.

#### Beantwortung der Fragen – Punktvergabe (Scores)

Wenn ein\*e Nutzer\*in sich am Anfang des Entscheidungsbaums befindet, erstellt das Programm im Hintergrund eine Liste mit allen möglichen Ergebnissen (über 700), denen jeweils eine Startpunktzahl (**„Score“**) von 0 zugewiesen wird. Während der/die Nutzer\*in die Fragen beantwortet, werden einige Ergebnisse begünstigt (ihr Score steigt), andere benachteiligt (ihr Score sinkt), einige werden sofort ausgeschlossen (ihr Score sinkt auf -100) und andere bleiben unverändert. Am Ende der Beantwortung wird das Ergebnis mit dem höchsten Score angezeigt und bis 4 weitere Szenarien („top Tier“) als „weitere Ergebnisse“ vorgeschlagen. Ob und wie viele alternative Szenarien gezeigt werden hängt davon ab, wie stark ihre Scores voneinander abweichen.

Die Regeln, die festlegen, wie sich die Art der Beantwortung der einzelnen Fragen auf dem Score der verschiedenen Ergebnisse auswirkt, werden in der Datei [setQuestionsRules.py](https://github.com/bolognalab/bolognalab.github.io/blob/main/entscheidungshilfe-lehre/setQuestionsRules.py) geschrieben. Wenn dieses Python-Skript aufgeführt wird, dann werden alle Regeln als "Effekte" einer Antwortmöglichkeit auf die Punktzahl eines Szenarios in der Datei [data.json](https://github.com/bolognalab/bolognalab.github.io/blob/main/entscheidungshilfe-lehre/data.json) gespeichert. In der Python-Datei ist auch die Logik hinter der Regeln in englischer Sprache kurz durch Kommentare erklärt.

Zusätzlich können auf der Seite <https://bolognalab.github.io/entscheidungshilfe-lehre/app-flow.html> die Regeln in Praxis getestet werden, indem man die Fragen beantwortet und gleich den Einfluss auf die Scores der Ergebnisse sehen kann (Abbildung 5). Auf dieser Seite gibt es auch eine Filter-Funktion, wenn man bestimmte Szenarien verfolgen möchte. Um den Namen eines Szenarios zu sehen, könnte man mit den Mauszeiger für ein paar Sekunden auf dem Code des Szenarios lassen - so erscheint der Titel des Szenarios als Tooltip.

**Achtung:  nachdem die Dateiene scenarien.csv or fragen_source.json geändert werden muss noch das Skript setQuestionsAndRules.py ausgeführt werden, damit die Änderungen im Tool sichtbar sind!**

![](dokumentation/img_flowScreenshot.png)
*Abbildung 5. Screenshot aus der Seite app-flow.html. Die mit gelb markierten Szenarien sind die, die durch die letzte Frage beeinflusst wurden.*

#### Fragen zur Entwicklung?
Wenn Sie Fragen zum Quellcode haben (der in dieser Dokumentation nicht im Fokus liegt) oder bei der Weiterentwicklung des Tools auf Probleme stoßen, zögern Sie nicht, Natalia zu kontaktieren (auch wenn sie nicht mehr formell im Netzwerk Hybride Lehre beschäftigt ist)! Sie hilft Ihnen gerne weiter, soweit sie kann. Ihre aktuellen Kontaktdaten finden Sie auf <https://naspitha.github.io/>.