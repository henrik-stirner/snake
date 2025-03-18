# ----------
# Helferfunktionen für die Validierung von Eingaben in Entry-Widgets
# ----------

def register(root: object, validatecommand: callable) -> tuple[callable, str, str]:
    """
    Registriert die Validierungsfunktionen für die Entry-Widgets.

    :param root: Fenster, in dem die Entry-Widgets sind
    :param validatecommand: Validierungsfunktionen
    :return: validatecommand wrapper
    """

    return root.register(validatecommand), '%d', '%S'


# siehe https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/entry-validation.html

def alphabetic(action_code: 0 | 1 | -1, change: str):
    return change.isalpha() if action_code in "01" else True


def numeric(action_code: 0 | 1 | -1, change: str):
    return change.isdigit() if action_code in "01" else True


def alphanumeric(action_code: 0 | 1 | -1, change: str):
    return change.isalnum() if action_code in "01" else True
