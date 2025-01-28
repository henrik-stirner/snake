# Pflichtenheft

--- 

## Zielbestimmung

### Musskriterien
- Startfenster
- Einstellungsfenster
- Spielfeld, funktionsfähige Spielumgebung

### Wunschkriterien
- weitere Modi
- Zusatzfunktionen
  - Mauern
  - Power-ups
- Sounds
- Animationen

### Abgrenzungskriterien
- Levels
- Online-Multiplayer
- maschinelles Lernen

---

## Produkteinsatz

### Anwendungsbereiche
- Zeitvertreib (mit Freunden)
- Hardwaretests
- motorisches und kognitives Training (Reaktionszeit, Hand-Augen-Koordination)
- [Einfuehrung in die Programmierung: erstellen eigener Maps / Bots (Zusatzfunktion)]

### Zielgruppen
- Spielliebhaber
- Snake- / Retro-Fans

### Betriebsbedingungen
- Tastatur / Controller / ...
- Spieler ständig anwesend (im Spiel, sonst Spielende)

---

## Produktübersicht
- Snake (Spiel)
  - steuerbare Schlange
  - Aepfel -> Punkte
  - Einzel- und Mehrspielermodus
- Highscore-System
- Benutzeroberflaeche zur weiteren Bedienung
  - Startbildschirm
    - Modus-Auswahl, Namenseingabe
  - Einstellungen
  - (gesonderte) High-Score-Ansicht

---

## Produktfunktionen

### grundlegende Funktionen
- Spielstart durch Start Knopf
- Spielfeldkriterien:
  - besteht aus Feldern
    - groesse veraenderbar
    - verschiedene Zellzustaende
      - leer (normaler Hintergrund)
      - Apfel
      - Schlangenkopf
      - Schlangenglied 
- Apfelkriterien:
  - hat eine Position
  - kann gegessen werden (und erneut mit veraenderter Position erscheinen)
  - das essen von Aepfeln gibt Punkte
- Schlangenkriterien:
  - waechst durch Apfelkonsum
  - Richtung (aenderbar durch Pfeiltasten)
  - Lebensdauer der Schlangenglieder nimmt mit der Zeit ab
  - Schlangenglied muss Verschwinden, wenn Lebensdauer ablaeuft
- Spielende:
  - zusammenstoss des Schlangenkopfes, mit einer Wand oder einem Schlangenglied fuehrt zum Beenden der Spielrunde
  - Game Over + Highscoreliste (nach Ende einer Spielrunde)

### Wunschfunktionen
- Modi:
  - unendlicher Modus
    - kein Spielende durch Kollision(schlange verlauft ueber sich selbst und springt von einer Wand zur gegenueberliegenden)
  - gegen Computer
    - Verschiedene Algorithmen
  - Wettkampf (lokal)
    - wer als letzter lebt, gewinnt
    - wer weniger stirbt (in vorgegebener Zeit) gewinnt
    - wer in vorgegebener Zeit am meisten Punkte sammelt, gewinnt
- Zusatzfunktionen:
  - Spielfeld mit Mauern
  - Powerups:
    - schnelleres Spiel
    - mehr Aepfel
    - Spielfeld aendert sich
- Sounds
  - Spielstart
  - Schlange isst Apfel
  - Kollision / Schlangentod
  - Spielende
  - entsprechend zu den Zusatzfunktionen
    - Powerup eingesammelt
    - Zeit wird knapp
    - etc.
- Animationen

### Abgrenzungsfunktionen
- Levels
- Online-Multiplayer
- maschinelles Lernen

--- 

## Produktdaten
- Konfiguration
  - Fenstergroeße und -position
  - Einstellungen
    - Spielfeldgroesse
    - Modus
      - weitere modus-spezifische Einstellungen
    - (Sound)
  - Standard-Spielername
- Highscore-System
  - Erreichte Punktzahl (Score) bzw. Laenge der Schlange
  - Spielername
  - Spielfeldgroesse
  - Geschwindigkeit
  - Modus
  - ggf. Gegner
  - weitere modus-spezifische Metadaten

---

## Produktleistungen
- annehmbare Bildrate im Spielmodus
  - mindestens 60 FPS bei geeigneter Hardware (, beispielsweise: )
    - 8 GB RAM
    - 4 logische Prozessorkerne
    - (persistenter Speicher in Form einer SSD)
- verlustfreie Speicherung persistenten Daten
  - Einstellungen
  - Scores
- stabilität
  - möglichst wenige, am besten keine Abstuerze

---

## Qualitätsanforderungen
- Spielmechanik
  - flüssige Steuerung
  - fehlerfreie Kollisionserkennung
  - möglichst geringe Latenzzeit
- Spielspass
  - angemessener Schwierigkeitsgrad
  - Wiederholbarkeit

---

## Benutzungsoberfläche
- ansprechend
- übersichtlich
- selbsterklärend
- angemessene Farbgebung
  - aesthetisch
  - funktional
