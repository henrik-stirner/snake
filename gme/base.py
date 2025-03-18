from typing import *
from configparser import ConfigParser
import logging

from random import randint


# ----------
# logger
# ----------

logger = logging.getLogger(__name__)

# ----------
# eigene imports
# ----------

from gme.obj.schlange import Konsumgut
from gme.obj.schlange import SchlangenKopf

# ----------


class Spiel:
    """
    Das Spiel. Ich hab daran gedacht.
    """

    def __init__(self, spiel_fenster: object) -> None:
        """
        Initialisiert ein Spiel.

        :param spiel_fenster: SpielFenster, in dem das Spiel stattfindet. Umfasst die entsprechenden Schnittstellen für die Darstellung und Eingabe.
        """

        self.config = ConfigParser()
        self.config.read("./config.ini")

        self.delay = self.config["Spiel"]["delay"]

        self.erlaubte_eingaben = ""
        self.spielobjekte = []

        self.spiel_fenster = spiel_fenster

    def aktualisieren(self) -> None:
        """
        Aktualisiert das Spiel, indem alle Spielobjekte aktualisiert und neu gezeichnet werden.

        :return:
        """

        for spielobjekt in self.spielobjekte:
            if spielobjekt.tot and not isinstance(spielobjekt, SchlangenKopf):
                self.spielobjekte.remove(spielobjekt)

        if self.spiel_fenster.eingaben:
            eingabe = self.spiel_fenster.eingaben.pop(0)
            self.eingabe_verarbeiten(eingabe)

        for spielobjekt in self.spielobjekte:
            spielobjekt.aktualisieren()
        self.spielobjekte.sort(key=lambda obj: obj.z_index)
        for spielobjekt in self.spielobjekte:
            spielobjekt.malen()

    def eingabe_verarbeiten(self, eingabe: str) -> None:
        """
        Verarbeitet eine Eingabe. Diese Methode soll von Unterklassen überschrieben werden.

        :param eingabe: Tastenbezeichner, i. d. R. Buchstabe
        :return:
        """

        pass

    def zufaellige_kachel(self) -> tuple[int, int]:
        """
        Gibt Koordinaten einer zufälligen Kachel zurück.

        :return: K(x|y)
        """

        x = randint(0, self.spiel_fenster.w-1)
        y = randint(0, self.spiel_fenster.h-1)

        return x, y

    def kachel_frei(self, x: int, y: int) -> bool:
        """
        Überprüft, ob die Kachel bei den Koordinaten x und y frei ist.

        :param x: x-Koordinate
        :param y: y-Koordinate
        :return:
        """

        for spielobjekt in self.spielobjekte:
            if x == spielobjekt.x and y == spielobjekt.y:
                return False

        return True

    def objekte_auf_kachel(self, x: int, y: int) -> list[object]:
        """
        Gibt eine Liste von Spielobjekten zurück, die sich auf der Kachel bei den Koordinaten x und y befinden

        :param x: x-Koordinate
        :param y: y-Koordinate
        :return:
        """

        objekte = []

        for spielobjekt in self.spielobjekte:
            if x == spielobjekt.x and y == spielobjekt.y:
                objekte.append(spielobjekt)

        return objekte

    def instanz_auf_kachel(self, x: int, y: int, typ: Type) -> bool:
        """
        Überprüft, ob sich ein Objekt des Typs typ auf der Kachel bei den Koordinaten x und y befindet.

        :param x: x-Koordinate
        :param y: y-Koordinate
        :param typ: Klasse bzw. Objekt des Typs Typ o. Metaklasse etc.
        :return:
        """

        return any([isinstance(obj, typ) for obj in self.objekte_auf_kachel(x, y)])

    def kachel_begehbar(self, x: int, y: int) -> bool:
        """
        Überprüft, ob die Kachel bei den Koordinaten x und y begehbar (frei von Objekten) ist.

        :param x: x-Koordinate
        :param y: y-Koordinate
        :return:
        """

        if not ((0 <= x <= self.spiel_fenster.w - 1) and (0 <= y <= self.spiel_fenster.h - 1)):
            # nicht auf Spielfeld
            return False

        if not all([isinstance(obj, Konsumgut) for obj in self.objekte_auf_kachel(x, y)]):
            return False

        return True

    def alle_kacheln_belegt(self) -> bool:
        """
        Prüft, ob es noch mindestens eine freie Kachel auf dem Spielfeld gibt.

        :return:
        """

        for x in self.spiel_fenster.w:
            for y in self.spiel_fenster.h:
                if self.kachel_fre(x, y):
                    return False

        return True

    def zufaellige_freie_kachel(self) -> tuple[int, int] | tuple[None, None]:
        """
        Gibt die Koordinaten einer zufälligen freien Kachel zurück, falls es noch eine gibt.

        :return:
        """

        x, y = self.zufaellige_kachel()

        versuch = 1
        while not self.kachel_frei(x, y):
            if versuch == 10:
                if self.alle_kacheln_belegt():  # nur Pech? aufwendiger Test...
                    return None, None

                # andernfalls versuch += 1 also == 11, d.h. es wird kein zweites Mal geprüft

            x, y = self.zufaellige_kachel()
            versuch += 1


        return x, y

    def spiel_beenden(self):
        self.spiel_fenster.schliessen()
