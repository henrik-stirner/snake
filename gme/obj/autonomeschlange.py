from typing import *
from configparser import ConfigParser
import logging

import math
import random


# ----------
# config und logger
# ----------

config = ConfigParser()
config.read("./config.ini")

logger = logging.getLogger(__name__)

# ----------
# eigene imports
# ----------

from gme.obj.konsumgut import Konsumgut
from gme.obj.schlange import SchlangenKopf

# ----------


class AutonomerSchlangenKopf(SchlangenKopf):
    def __init__(self, spiel, x, y, richtung, laenge, farbe="darkblue", name="Computer", lebensdauer=None):
        super().__init__(name, spiel, x, y, richtung, laenge, farbe, lebensdauer)
    
    def abstand(self, obj): 
        return math.sqrt((obj.x - self.x)**2 + (obj.y - self.y)**2)
    
    def denken(self):
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
            ertragreiche_richtungen.append((1 if dx > 0 else -1, 0))
            # vertikal
            ertragreiche_richtungen.append((0, 1 if dy > 0 else -1))

        # ----------
        # Also... Wohin jetzt?
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

        # Ab hier sieht es schlecht aus..

    def aktualisieren(self):
        self.denken()
        super().aktualisieren()
