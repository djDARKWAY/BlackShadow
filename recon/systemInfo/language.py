import locale

def getLanguage():
    language, _ = locale.getdefaultlocale()
    return language
