from configparser import ConfigParser
import logging

from tkinter import X, messagebox
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

from win.tl.base import Nebenfenster

# ----------


class NameEingabeFenster(Nebenfenster):
	def __init__(self, spiel_fenster, spielerzahl: int = None) -> None:
		super().__init__(spiel_fenster)
		self.title("Namenseingabe")

		self.entries = []

		self.interface_generieren(spielerzahl)
		self.mainloop()

	def interface_generieren(self, spielerzahl: int = None):
		super().interface_generieren()

		self.entry_frame = Frame(self.frame)
		self.entry_frame.pack(expand=True, pady=10)

		self.knopf_frame = Frame(self.frame)
		self.knopf_frame.pack(expand=True, fill=X, pady=10)

		standard_entry = self.entry_erstellen()
		standard_entry.insert(0, config["Spiel"]["nutzername"])

		if spielerzahl is not None:
			num_len = len(str(spielerzahl))
			for i in range(spielerzahl-1):
				spieler_entry = self.entry_erstellen()
				spieler_entry.insert(0, f"Spieler{str(i).zfill(num_len)}")
		else:
			# variable Spielerzahl
			self.hinzufuegen_knopf = Button(self.knopf_frame, style="Big.TButton", text="SPIELER HINZUFÜGEN", command=self.entry_erstellen)
			self.hinzufuegen_knopf.pack(fill=X)

		# Fortfahren-Knopf
		self.fertig_knopf = Button(self.knopf_frame, style="Big.TButton", text="FORTFAHREN", command=self.eingabe)
		self.fertig_knopf.pack(fill=X)

	def entry_erstellen(self):
		spieler_entry = Entry(self.entry_frame)
		spieler_entry.pack(fill=X, pady=5)
		self.entries.append(spieler_entry)

		return spieler_entry

	def namen(self):
		return [entry.get() for entry in self.entries]

	def eingabe(self):
		namen = []
		for entry in self.entries:
			if name := entry.get():
				if name in namen:
					messagebox.showerror("Doppelter Name", "Bitte tragen sie für jeden Spieler einen einzigartigen Namen ein.")
					return
				namen.append(name)
			else:
				messagebox.showerror("Leeres Eingabefeld", "Bitte tragen Sie für jeden Spieler einen alphanumerischen Namen ein.")
				return

		super().schliessen()
		self.hauptfenster.spiel_starten(namen)

	def abbruch(self):
		pass

	def einstellungen_speichern(self):
		# Nutzernamen speichern
		config.set("Spiel", "nutzername", str(self.entries[0].get()))
		with open("config.ini", "w") as configfile:
			config.write(configfile)

	def schliessen(self):
		pass
