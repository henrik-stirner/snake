from typing import *
from configparser import ConfigParser
import logging


# ----------
# logger
# ----------

logger = logging.getLogger(__name__)

# ----------
# eigene imports
# ----------

from gme.base import Spiel

from gme.obj.schlange import SchlangenKopf
from gme.obj.konsumgut import Apfel

# ----------


class WandlosSpiel(Spiel):
    """
    Ein Spiel, bei dem die Schlange durch die Wände teleportiert wird.
    Der Spielfeldrand ist ungefährlich, aber eine Kollision mit dem eigenen Körper ist möglich.
    """

    def __init__(self, spiel_fenster: object, spieler_name: str) -> None:
        """
        Initialisiert das Spiel.

        :param spiel_fenster: SpielFenster, in dem das Spiel stattfindet. Umfasst die entsprechenden Schnittstellen für die Darstellung und Eingabe.
        :param spieler_name:
        """

        super().__init__(spiel_fenster)
        self.erlaubte_eingaben += self.config["Steuerung"]["spieler_0"]
        self.richtung_eingaben = {
            self.erlaubte_eingaben[0]: (0, -1),     # w → oben
            self.erlaubte_eingaben[1]: (-1, 0),     # a → links
            self.erlaubte_eingaben[2]: (0, 1),      # s → unten
            self.erlaubte_eingaben[3]: (1, 0)       # d → rechts
        }

        self.schlange = SchlangenKopf(spieler_name, self, (self.spiel_fenster.w - 1) // 2, (self.spiel_fenster.h - 1) // 2, (0, -1), 2, wand_teleport=True)
        self.apfel = Apfel(self, *self.zufaellige_freie_kachel())

        self.spielobjekte += [self.schlange, self.apfel]

    def aktualisieren(self) -> None:
        """
        Aktualisiert das Spiel.
        :return:
        """

        for spielobjekt in self.spielobjekte:
            if spielobjekt.tot and isinstance(spielobjekt, SchlangenKopf):
                self.spiel_beenden()

        super().aktualisieren()

    def eingabe_verarbeiten(self, eingabe: str) -> None:
        """
        Verarbeitet die Eingabe des Spielers.

        :param eingabe: Tastenbezeichner, i. d. R. Buchstabe
        :return:
        """

        neue_richtung = self.richtung_eingaben[eingabe]
        self.schlange.drehen(neue_richtung)
