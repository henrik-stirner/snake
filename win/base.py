from typing import *
from configparser import ConfigParser
import logging

from tkinter import *
from tkinter.ttk import *


# ----------
# config und logger
# ----------

config = ConfigParser()
config.read("./config.ini")

logger = logging.getLogger(__name__)

# ----------
# eigene imports
# ----------

# ...

# ----------


class Hauptfenster(Tk):
	def __init__(self) -> None:
		super().__init__()

		self.tk.call("source", "./thema.tcl")

		self.stil = Style()
		self.stil.theme_use("dunkel")

		self.focus_force()
		self.geometry(
			f"{config["Window"]["w"]}x{config["Window"]["h"]}+{config["Window"]["x"]}+{config["Window"]["y"]}"
		)

		self.protocol("WM_DELETE_WINDOW", self.schliessen)
		self.bind('<Key>', lambda event: self.taste(event))
		self.bind('<Return>', lambda args: self.eingabe())

	def interface_generieren(self):
		self.background = Frame(self)
		self.background.place(x=0, y=0, relwidth=1.0, relheight=1.0)

		self.frame = Frame(self)
		self.frame.pack(expand=True, fill=X)

	def taste(self, event):
		taste = event.char

		if taste == "\x1b":  # Escape
			self.abbruch()

	def eingabe(self):
		pass

	def abbruch(self):
		self.schliessen()

	def einstellungen_speichern(self):
		pass

	def schliessen(self):
		self.einstellungen_speichern()
		self.destroy()


class Nebenfenster(Toplevel):
	def __init__(self, hauptfenster) -> None:
		super().__init__(hauptfenster)

		self.hauptfenster = hauptfenster

		self.stil = self.hauptfenster.stil
		stil_name = self.hauptfenster.stil.theme_use()
		self.stil.theme_use(stil_name)

		self.focus_force()
		self.geometry(
			f"{config["Window"]["w"]}x{config["Window"]["h"]}+{config["Window"]["x"]}+{config["Window"]["y"]}"
		)

		self.protocol("WM_DELETE_WINDOW", self.schliessen)
		self.bind('<Key>', lambda event: self.taste(event))
		self.bind('<Return>', lambda args: self.eingabe())

	def interface_generieren(self):
		self.background = Frame(self)
		self.background.place(x=0, y=0, relwidth=1.0, relheight=1.0)

		self.frame = Frame(self)
		self.frame.pack(expand=True, fill=X)

	def taste(self, event):
		taste = event.char

		if taste == "\x1b":  # Escape
			self.abbruch()

	def eingabe(self):
		pass

	def abbruch(self):
		self.schliessen()

	def einstellungen_speichern(self):
		pass

	def schliessen(self):
		self.einstellungen_speichern()
		self.destroy()
		self.hauptfenster.deiconify()
