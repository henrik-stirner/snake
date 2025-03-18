from typing import *
from configparser import ConfigParser
import logging

from tkinter import *
from tkinter.ttk import *


# ----------
# logger
# ----------

logger = logging.getLogger(__name__)

# ----------
# eigene imports
# ----------

# ...

# ----------


class Nebenfenster(Toplevel):
	"""
	Grundklasse für Nebenfenster
	"""

	def __init__(self, hauptfenster) -> None:
		"""
		Initialisierung des Nebenfensters.
		Der Stil des Hauptfensters wird übernommen.

		:param hauptfenster:
		:return:
		"""

		super().__init__(hauptfenster)

		self.hauptfenster = hauptfenster

		self.stil = self.hauptfenster.stil
		stil_name = self.hauptfenster.stil.theme_use()
		self.stil.theme_use(stil_name)

		self.focus_force()

		self.config = ConfigParser()
		self.config.read("./config.ini")
		self.geometry(
			f"{self.config["Fenster"]["w"]}x{self.config["Fenster"]["h"]}+{self.config["Fenster"]["x"]}+{self.config["Fenster"]["y"]}"
		)

		self.protocol("WM_DELETE_WINDOW", self.schliessen)
		self.bind('<Key>', lambda event: self.taste(event))
		self.bind('<Return>', lambda args: self.eingabe())

	def interface_generieren(self) -> None:
		"""
		Generiert das Interface.
		Standardmäßig hat jedes Fenster einen leeren Frame,
		denn die Hintergrundfarbe des Fensters selbst kann nicht per Stylesheet konfiguriert werden.

		:return:
		"""

		self.background = Frame(self)
		self.background.place(x=0, y=0, relwidth=1.0, relheight=1.0)

		self.frame = Frame(self)
		self.frame.pack(expand=True, fill=X)

	def taste(self, event: Event) -> None:
		"""
		Verarbeitung von Tastatureingaben.

		:param event: Tkinter <Key> Event
		:return:
		"""

		taste = event.char

		if taste == "\x1b":  # Escape
			self.abbruch()

	def eingabe(self) -> None:
		"""
		Entertaste standardmäßig unbelegt.
		Zu überschreiben.

		:return:
		"""

		pass

	def abbruch(self) -> None:
		"""
		Escape-Taste standardmäßig für:
		Schließen des Fensters.

		:return:
		"""

		self.schliessen()

	def einstellungen_speichern(self) -> None:
		"""
		Speichert die Einstellungen in der Konfigurationsdatei.
		Zu überschreiben.

		:return:
		"""

		pass

	def schliessen(self) -> None:
		"""
		Schließt dieses Fenster.

		:return:
		"""

		self.einstellungen_speichern()
		self.destroy()
