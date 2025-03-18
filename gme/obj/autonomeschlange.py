from typing import *
import logging

import math
import random


# ----------
# logger
# ----------

logger = logging.getLogger(__name__)

# ----------
# eigene imports
# ----------

from gme.obj.konsumgut import Konsumgut
from gme.obj.schlange import SchlangenKopf

# ----------


class AutonomerSchlangenKopf(SchlangenKopf):
    """
    computergesteuerter Schlangenkopf, der von sich aus eine sinnvolle Bewegungsrichtung ermittelt
    """

    def __init__(self, spiel: object, x: int, y: int, richtung: tuple[int, int], laenge: int = 0, farbe: str = "darkblue", name: str = "Computer", lebensdauer: int = None) -> None:
        """
        Initialisiert ein neuen AutonomenSchlangenkopf.

        :param spiel: Spiel, in dem das Objekt existieren soll
        :param x: x-Koordinate
        :param y: y-Koordinate
        :param richtung: 2d-Richtungsvektor, in welche sich das Objekt bewegen soll [z.B. (1, 0) für rechts]
        :param laenge: Länge der Schlange
        :param farbe: Farbe des Objekts. Standard: "darkblue". Vorzugsweise eine dunkle Farbe (Glieder standardmäßig heller, z.B. "blue").
        :param name: Name des Objekts. Standard: "Computer" Normalerweise (SchlangenKopf): Spielername
        :param lebensdauer: Lebensdauer des Objekts in Zyklen (Aktualisierungen des Spielfelds). Standard: None (unendlich)
        """

        super().__init__(name, spiel, x, y, richtung, laenge, farbe, lebensdauer)
    
    def abstand(self, obj: object) -> float:
        """
        Berechnet den Abstand zu einem anderen Objekt.

        :param obj: Anderes SpielObjekt
        :return: Abstand
        """

        return math.sqrt((obj.x - self.x)**2 + (obj.y - self.y)**2)
    
    def denken(self) -> None:
        """
        Es wird eine günstige Richtung für den nächsten Zug ermittelt und gesetzt.
        Tödliche Richtungen werden vermieden; Ziel ist das Erreichen von Konsumgütern.

        :return:
        """

        # ----------
        # Nicht sterben!
        # ----------

        verbotene_richtungen = [(-self.richtung[0], -self.richtung[1])]  # 180-Grad-Wende nie vorteilhaft

        # ----------

        links = (self.richtung[1], self.richtung[0])
        rechts = (-links[0], -links[1])

        # vorne, links, rechts: Koordinaten potentieller naechster Felder
        if not self.spiel.kachel_begehbar(self.x + self.richtung[0], self.y + self.richtung[1]):
            verbotene_richtungen.append(self.richtung)
        if not self.spiel.kachel_begehbar(self.x + links[0], self.y + links[1]):
            verbotene_richtungen.append(links)
        if not self.spiel.kachel_begehbar(self.x + rechts[0], self.y + rechts[1]):
            verbotene_richtungen.append(rechts)

        # ----------
        # Konsumverhalten: Konsum maximieren
        # ----------

        ertragreiche_richtungen = []

        # ----------

        moegliche_ziele = [obj for obj in self.spiel.spielobjekte if (isinstance(obj, Konsumgut) and not obj.konsumiert)]

        if moegliche_ziele:
            # ziel ist das naechste Objekt
            ziel = moegliche_ziele[0]
            for obj in moegliche_ziele[1:]:
                if self.abstand(obj) < self.abstand(ziel):
                    ziel = obj

            # Entfernung -> Richtung
            dx, dy = ziel.x - self.x, ziel.y - self.y
            # horizontal
            if dx > 0:
                ertragreiche_richtungen.append((1 if dx > 0 else -1, 0))
            # vertikal
            if dy > 0:
                ertragreiche_richtungen.append((0, 1 if dy > 0 else -1))

        # ----------
        # Zusammenführen der Informationen (und setzen der Richtung)
        # ----------

        guenstige_richtungen = [richtung for richtung in ertragreiche_richtungen if not richtung in verbotene_richtungen]
        if guenstige_richtungen:
            self.richtung = random.choice(guenstige_richtungen)
            return

        # Kein Essen in Aussicht. Ueberleben.
        verbleibende_richtungen = [richtung for richtung in self.erlaubte_richtungen if not richtung in verbotene_richtungen]
        if verbleibende_richtungen:
            self.richtung = random.choice(verbleibende_richtungen)
            return

        # Ab hier sieht es schlecht aus für den Schlangenkopf.

    def aktualisieren(self) -> None:
        """
        Der Schlangenkopf ermittelt eine sinnvolle Bewegungsrichtung.

        :return:
        """

        self.denken()
        super().aktualisieren()
