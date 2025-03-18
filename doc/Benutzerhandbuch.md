# Benutzerhandbuch

Lesen Sie vor dem ersten Programmstart das gesamte Benutzerhandbuch aufmerksam durch!

---

## 0 Allgemeines
Mit "drücken" bzw. "klicken" ist im allgemeinen eine Betätigung der Haupttaste der Computermaus gemeint.

Zum Großteil kann das Interface auch mit der Tastatur bedient werden.
`Enter` ist stets positive oder voranschreitend konnotiert. Typische Aktionen sind z. B. Starten oder Fortfahren.
`Escape` ist stets mit einem Abbruch oder Schließen des Fensters verbunden.
Ausnahme ist lediglich das Nameeingabefenster, dessen Schließen praktischerweise nicht möglich ist (s.u.).
Des weiteren sind das Einstellungs- und Highscorefenster nur durch betätigung der entsprechenden Knöpfe
mit der Computermaus erreichbar.

## 1 Starten des Programms 
Um das Programm zu starten, führen Sie das Skript `main.py` mit Ihrem Python3-Interpreter aus.
(Auf einigen Systemen ist dies direkt per Doppelklick möglich, wenn die Dateiendung ".py" entsprechend assoziiert wurde.)
Achten Sie dabei darauf, dass die folgenden Bibliotheken auf Ihrem Gerät installiert sind!

- **tkinter** <br>

Es handelt sich um einen Standardbibliothek, 
die bei standardmäßiger Installation von Python automatisch mitinstalliert wird.

Anschließend sollte sich das Launcherfenster öffnen.

## 2 Einstellungen
Um auf die Einstellungen zugreifen zu können, drücken Sie auf das Zahnradsymbol oben rechts im Launcherfenster.

Unter Fenstereinstellung können Sie die Größe und Position des Fensters anpassen, 
indem Sie die folgenden Werte festlegen. **!!!Achtung: nur positive Ganzzahlen verwenden!!!**
- w: legt die Breite des Fensters in Pixeln fest
- h: legt die Höhe des Fensters in Pixeln fest
- x: legt den Abstand der oberen linken Ecke des Fensters zum linken Bildschirmrand in Pixeln fest
- y: legt den Abstand der oberen linken Ecke des Fensters zum oberen Bildschirmrand in Pixeln fest

Unter Spieleinstellungen finden Sie die folgenden Spielanpassungen:
- mode: legt den Spielmodus wie folgt fest. <br>
  **!!!Achtung: andere Eingaben, als die folgenden, sind nicht zulässig!!!**
  - 0 entspricht dem klassischem Modus
  - 1 entspricht dem "Mehrspieler"-Modus
  - 2 entspricht dem "Wandlos"-Modus
  - 3 entspricht dem "Gegen Computer"-Modus
  - 4 entspricht dem "Simulation"-Modus
- w: legt die Spilfeldbreite in Feldern Fest
- h: legt die Spielfeldhöhe in Feldern Fest
- delay: legt die Zeit in ms fest, in der die Schlange sich ein Feld weiterbewegt
  - nutzername: legt den Namen fest unter dem der Score bzw. Highscore gespeichert bzw. angezeigt wird <br>
  **Achtung: !!!erfordert alphanumerische Eingabe!!!**

Die Steuerung kann wie folgt für jeden Spieler unabhängig geändert werden:
- 1. Buchstabe / Ziffer für Bewegungsrichtung Aufwärts
- 2. Buchstabe / Ziffer für Bewegungsrichtung Links
- 3. Buchstabe / Ziffer für Bewegungsrichtung Abwärts
- 4. Buchstabe / Ziffer für Bewegungsrichtung Rechts

## 3 Einen Spielmodus Auswählen
Um einen Modus auszuwählen, öffnen Sie das ensprechende Dropdownmenü,
welches sich in der Mitte des Launcherfensters befindet, mit einem Linksklick. 
Wählen Sie jetzt einen der verfügbaren Modi aus.

Sollten Sie keinen Modus ausgewählt haben, ist der klassische Modus standartmäßig ausgewählt. 
Sollten Sie bereits gespielt haben, dann ist standartmäßig der zuletzt ausgewählte Modus ausgewählt, 
auch wenn Sie das Programm zwischenzeitig beendet haben.

## 4 Eine Spielrunde starten
Um jetzt eine Spielrunde zu starten, drücken Sie auf Start oder betätigen Sie `Enter`. 
Sollten Sie noch keinen Nutzernamen gespeichert haben, öffnet sich vor dem Spielen ein Eingabefenster, 
in dem der Nutzername festzulegen ist. Drücken Sie in diesem Fenster nach festlegung des Namens auf Fortfahren, 
um die Spielrunde zu starten.

**!!!Achtung: wenn bereits ein Nutzername gespeichert ist, 
startet das Spiel nach drücken der Entertaste oder des Startknopfes sofort!!!**

## 5 Steuerung im Spiel
Die Richtung der Schlange lässt sich im klassischen Spiel standardmäßig mit mit den Tasten `W` ; `A` ; `S` und `D` ändern. 
Im Mehrspielerspiel lässt sich die Richtung der zweiten Schlange standardmäßig mit den Tasten `I` ; `J` ; `K` und `L` ändern.
- `W` / `I` für Bewegungsrichtung Aufwärts
- `A` / `J` für Bewegungsrichtung Links
- `S` / `K` für Bewegungsrichtung Abwärts
- `D` / `L` für Bewegungsrichtung Rechts

Die Tastenbelegung der Steuerung kann in den Einstellungen geändert werden.
Um das Spiel zu pausieren, betätigen Sie `Escape`. 
Um das Spiel anschließend fortzusetzen, betätigen sie `Enter`.

## 6 Punkte erzielen
Um Punkte zu erzielen, navigieren Sie die Schlange zum rot gekenzeichnetem Feld ("Apfel").<br>
Für jedes Ereichen des Feldes erhalten Sie im klassischem Spiel jeweils einen Punkt. 
Versuchen Sie, so viele Punkte wie möglich zu erzielen, um einen möglichst hohen Platz auf dem Leaderbord zu erhalten.

Um auf eine vollständige, scrollbare Highscoreliste zuzugreifen, 
drücken Sie auf das Pokalsymbol oben links im Launcherfenster.

## 7 Spielende
Das Spiel endet, sobald mindestens eine der involvierten Schlangen stirbt.
Das ist der Fall, wenn der Schlangenkopf auf ein Schlangenglied seinen eigenen Körpers, 
auf ein Schlagnenglied eines fremden Schlangenkörpers, oder auf eine Wand (Spielfeldgrenze) trifft.

Eine Ausnahme ist der "Wandlos"-Modus, in welchem das Spielfeld auffällige Eigenschaften aufweist: 
Es handelt sich um die Emulation einer toroidalen Raumstruktur, 
denn gegenüberliegende Spielfeldgrenzen sind miteinander verbunden.
D. h. Sie Ihre Schlange stirbt nicht, wenn sie in eine Spielfeldbegrenzung fährt, 
sondern kommt auf der gegenüberliegenden Seite wieder heraus.

## 8 Der Mehrspieler Modus
Nach dem Starten einer Runde muss zunächst im vorgesehenen Eingabefeld des Nameeingabefensters jeweils 
der Name der Benutzer eingetragen werden. Der Name des Hauptnutzers ist bereits voreingetragen. 
Zudem sind anonymisierte Spielernamen der Form "SpielerX", wobei X der Index des Spielers ist, 
für weitere Spieler voreingetragen. Drücken Sie auf fortfahren, um mit dem Spiel zu beginnen, 
wenn Sie die Spielernamen im Rahmen ihrer Ansprüche angepasst haben.
Der Erste Spieler Steuert die links startende Schlange, der zweite Spieler steuert die rechts startende Schlange.
Ziel im Mehrspielermodus ist nicht, mehr Punkte als der Gegener zu erzielen, sondern länger zu übeleben.

## 9 Das Spiel Beenden
Nach dem Ende einer Spielrunde öffnet sich das Auswertungsfenster.
Drücken sie auf Zurück oder betätigen sie `Enter`, um wieder zum Launcherfenster zu gelangen.
Um das Spiel vorzeitig zu beenden, und zum Launchfenster zurückzukehren, drücken sie im Pausefenster Beenden oder `Escape`. 
Falls Sie das Spielfenster manuell schliessen, wird das Spiel ebenso beendet.

## 10 Beenden des Programmes
Betätigen sie im Launchfenster `Escape` um das Programm zu beenden. 
Alternativ können Sie das Launchfenster auch manuell schließen.

Drücken sie im Auswertungsfenster Beenden, um das Programm vorzeitig zu schließen.
