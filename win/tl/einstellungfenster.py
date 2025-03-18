import logging

from tkinter import BOTH, E, W
from tkinter.ttk import *

# ----------
# logger
# ----------

logger = logging.getLogger(__name__)

# ----------
# eigene imports
# ----------

from win.element.frame import VerticalScrolledFrame
from win.tl.base import Nebenfenster

# ----------


class EinstellungFenster(Nebenfenster):
    """
    Fenster für die Einstellungen des Programms
    """

    def __init__(self, launcher_fenster: object) -> None:
        """
        Initialisierung des Fensters.

        :param launcher_fenster: zum Wiederanzeigen beim Schließen dieses Fensters
        """

        super().__init__(launcher_fenster)
        self.title("Einstellungen")

        self.entries = []

        self.interface_generieren()
        self.mainloop()

    def interface_generieren(self) -> None:
        """
        Generiert das Interface des Fensters.

        :return:
        """

        super().interface_generieren()
        self.frame.pack(expand=True, fill=BOTH)

        # Info-Label
        self.info_label = Label(self.frame, text="EINSTELLUNGEN")
        self.info_label.pack(pady=20)

        # Ranking
        self.einstellungen_frame = VerticalScrolledFrame(self.frame)
        self.einstellungen_frame.interior.grid_columnconfigure(tuple(range(2)), weight=1)
        self.einstellungen_frame.pack(pady=10, expand=True, fill=BOTH)

        i = 1
        for kategorie in self.config.keys():
            ueberschrift_label = Label(self.einstellungen_frame.interior, text=kategorie)
            ueberschrift_label.grid(row=i, column=0, columnspan=2, pady=20)

            info_frame = Frame(self.einstellungen_frame.interior)
            info_frame.grid(row=i+1, column=0, sticky="nse")

            einstellung_frame = Frame(self.einstellungen_frame.interior)
            einstellung_frame.grid(row=i+1, column=1, sticky="w")

            for bezeichner, parameter in self.config[kategorie].items():
                info_label = Label(info_frame, text=bezeichner, anchor=E)
                info_label.pack(anchor=E, expand=True)
                einstellung_entry = Entry(einstellung_frame)
                einstellung_entry.insert(0, parameter)
                einstellung_entry.pack(pady=5, expand=True, anchor=W)

                self.entries.append(einstellung_entry)

            i += 2

    def einstellungen_speichern(self) -> None:
        """
        Speichert die Einstellungen in der config.ini-Datei.

        :return:
        """

        i = 0
        for kategorie in self.config.keys():
            for bezeichner in self.config[kategorie].keys():
                self.config.set(kategorie, bezeichner, str(self.entries[i].get()))
                i += 1

        with open("config.ini", "w") as configfile:
            self.config.write(configfile)
