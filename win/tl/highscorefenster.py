from configparser import ConfigParser
import logging

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


class HighscoreFenster(Nebenfenster):
    def __init__(self, launcher_fenster) -> None:
        super().__init__(launcher_fenster)
        self.title("Highscores")
    
        self.interface_generieren()
        self.mainloop()

    def _daten_laden(self):
        pass
