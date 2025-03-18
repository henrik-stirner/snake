import logging

from tkinter import X, messagebox
from tkinter.ttk import *

# ----------
# logger
# ----------

logger = logging.getLogger(__name__)

# ----------
# eigene imports
# ----------

from win.element.entry import register, alphanumeric

from win.tl.base import Nebenfenster

# ----------


class NameEingabeFenster(Nebenfenster):
	"""
	Fenster zur Eingabe der Spielernamen.
	"""

	def __init__(self, spiel_fenster: object, spielerzahl: int = None) -> None:
		"""
		Initiiert das Fenster zur Eingabe der Spielernamen.

		:param spiel_fenster: zum Starten des Spiels über die entsprechende Schnittstelle (Funktion spiel_starten()
		:param spielerzahl: die Spielerzahl entscheidet darüber, wie viele Namen eingegebene werden müssen
		"""

		super().__init__(spiel_fenster)
		self.title("Namenseingabe")

		self.ALPHANUMERIC = register(self, alphanumeric)

		self.entries = []

		self.interface_generieren(spielerzahl)
		self.mainloop()

	def interface_generieren(self, spielerzahl: int = None) -> None:
		"""
		Generiert das Interface des Namenseingabefensters.

		:param spielerzahl:
		:return:
		"""

		super().interface_generieren()

		self.entry_frame = Frame(self.frame)
		self.entry_frame.pack(expand=True, pady=10)

		self.knopf_frame = Frame(self.frame)
		self.knopf_frame.pack(expand=True, fill=X, pady=10)

		standard_entry = self.entry_erstellen()
		standard_entry.insert(0, self.config["Spiel"]["nutzername"])

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

	def entry_erstellen(self) -> Entry:
		"""
		Erstellt ein Entry-Widget für die Eingabe eines Spielernamens.

		:return:
		"""

		spieler_entry = Entry(self.entry_frame, validate="all", validatecommand=self.ALPHANUMERIC)
		spieler_entry.pack(fill=X, pady=5)
		self.entries.append(spieler_entry)

		return spieler_entry

	def namen(self) -> list[str]:
		"""
		Gibt die eingegebenen Spielernamen zurück.

		:return:
		"""

		return [entry.get() for entry in self.entries]

	def eingabe(self) -> None:
		"""
		Eingabe der Spielernamen überprüfen und ggf. Spiel starten.

		:return:
		"""

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

		self.einstellungen_speichern()
		self.destroy()
		self.hauptfenster.spiel_starten(namen)

	def abbruch(self) -> None:
		"""
		Abbruch des Spielstarts.

		:return:
		"""

		pass

	def einstellungen_speichern(self) -> None:
		"""
		Speichert die Einstellungen in der Konfigurationsdatei.

		:return:
		"""

		# Nutzernamen speichern
		self.config.set("Spiel", "nutzername", str(self.entries[0].get()))
		with open("config.ini", "w") as configfile:
			self.config.write(configfile)

	def schliessen(self) -> None:
		"""
		Schließt das Fenster nicht.
		Es soll nicht geschlossen werden, da die Eingabe der Spielernamen zwingend erforderlich ist.

		Stattdessen soll das Spiel gestartet und
		dann über den vorgesehenen Weg kontrolliert geschlossen oder neu gestartet werden.

		:return:
		"""

		pass
