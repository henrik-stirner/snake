# Benutzerhandbuch
Lesen sie vor Benutzung das gesamte Handbuch aufmerksam durch!
---

## 1 Starten des Programms 
Um das Programm zu starten führen sie das Skript `main.py` mit ihrem Pythoninterpreter aus. <br>
Achten sie dabei darauf, dass die folgenden Bibliotheken auf ihrem Gerät Instaliert sind!
- **tkinter** <br>

Anschliessend sollte sich  das Launchfnster öffnen.
## 2 Einstellungen
Um auf die Einstellung zugreifen zu können, drücken sie auf das Einstellungs Symbol, oben rechts im Lancherfenster.<br>

Unter Fenstereinstellung können sie Größe und Position des Fensters anpassen in dem sie die folgenden Werte festlegen **!!!Achtung nur positive Ganzzahlen verwenden!!!**:<br>
- w: legt die Breite des Fensters in Pixeln fest
- h: legt die Höhe des Fensters in Pixeln fest
- x: legt den Abstand der oberen linken Ecke des Fensters zum linken Bildschirmrand in Pixeln fest
- y: legt den Abstand der oberen linken Ecke des Fensters zum oberen Bildschirmrand in Pixeln fest<br>

Unter Spieleinstellungen finden sie die folgenden Spielanpassungen:
- mode: legt den Spielmodus wie folgt fest **!!!andere Eingaben sind nicht zulässig!!!**:
  - 0 entspricht dem klassischem Modus
  - 1 entspricht dem Mehrspieler Modus
  - 2 entspricht dem Wandlos Modus
  - 3 entspricht dem Modus gegen den Computer Modus
- w: legt die Spilfeldbreite in Feldern Fest
- h: legt die Spielfeldhöhe in Feldern Fest
- delay: legt die Zeit in ms fest in der die Schlange sich ein Feld weiter Bewegt
- nutzername: legt den Namen fest unter dem der score bzw. highscore gespeichert bzw. angezeigt wird **!!!erfordert alphanumerische Eingabe!!!**<br>

Die Steuerung kann wie folgt für jeden Spieler unabhängig geändert werden:
- 1. Buchstabe/Ziffer für Bewegungsrichtung Aufwärts
- 2. Buchstabe/Ziffer für Bewegungsrichtung Links
- 3. Buchstabe/Ziffer für Bewegungsrichtung Abwärts
- 4. Buchstabe/Ziffer für Bewegungsrichtung Rechts
## 2 Einen Spielmodus Auswählen
Um einen Modus auszuwählen, öffnen sie mit ihrem courser das Dropdownmenü, welches sich in der Mitte des Lancherfensters befindet. Wählen sie jetzt, mit dem courser einen der verfügbaren Modi aus.<br>
Sollten sie keinen Modus ausgewählt haben, ist der klassische Modus standartmäßig ausgewählt. Sollten sie bereits gespielt haben ist standartmäßig der zuletzt ausgewählte Modus ausgewählt, auch wenn sie das Programm zwischenzeitig beendet haben.
## 3 Eine Spielrunde starten
Um jetzt eine Spielrunde zu starten drücken sie  mit ihrem courser auf Start oder betätigen sie `Enter`. Sollten sie noch keinen Namen <br>
**!!! ACHTUNG nach drücken der Entertaste startet das Spiel sofort !!!**
## 4 Steuerung im Spiel
Die Richtung der Schlange lässt sich im Klassichem Spiel mit mit den Tasten `W` ; `A` ; `S` ; `D` ändern. Im Mehrspielerspiel lässt sich die Richtung der zweiten Schlange mit den Tasten `I` ; `J` ; `K` ; `L` ändern.<br>
- `W`/`I` für Bewegungsrichtung Aufwärts
- `A`/`J` für Bewegungsrichtung Links
- `S`/`K` für Bewegungsrichtung Abwärts
- `D`/`L` für Bewegungsrichtung Rechts

Die Tastenbelegung der Steuerung kann in den Einstellungen geändert werden.
Um das Spiel zu pausieren betätigen sie `esc`. Um das Spiel anschliesend fortzusetzen betätigen sie `Enter`.
## 5 Punkte erzielen
Um Punkte zu erzielen, navigieren sie die Schlange zum rot gekenzeichnetem Feld.<br>
Für jedes Ereichen des Feldes erhalten sie im klassischem Spiel jeweils einen Punkt. Versuchen sie so viele Punkte wie möglich zu erzielen, um einen Platz auf dem leaderbord zu erhalten.
## 6 Der Mehrspieler Modus
Der Erste Spieler Steuert die links startende Schlange, während der zweite Spieler die Rechts startende Schlange 
Ziel im Mehrspielermodus, ist nicht mehr Punkte als der Gegener zu erzielen, sondern länger zu übeleben.
## 7 Das Spiel Beenden
Nach Ende einer Spielrunde öffnet sich das Auswertungsfenster.
Drücken sie mit ihrem courser auf Zurück oder betätigen sie `Enter` um wieder zum Launchfenster zu gelangen.<br>
Drücken sie Beenden um das Programm zu schliesen.
Um das Spiel vorzeitig zu beenden und zum Launchfenster zurück zu kehren drücken sie im Pausefenster `esc`.<br>
Falls sie Spiel- oder Auswertungsfenster manuell schliessen, beenden sie auch das Program
## 8 Beenden des Programmes
Betätigen sie im Launchfenster `esc` um das Programm zu beenden. Alternativ können sie auch das Launchfenster manuell schliessen.