import json
import locale

def getLanguage():
    try:
        with open("utils/json/languages.json", "r", encoding="utf-8") as file:
            languages = json.load(file)
    except FileNotFoundError:
        return "Language file not found."
    except json.JSONDecodeError:
        return "Error decoding the language file."

    language, _ = locale.getdefaultlocale()

    if language in languages:
        return languages[language][0]
    else:
        return "Unknown Language"
