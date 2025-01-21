import platform

def getOsVersion():
    return f"{platform.system()} {platform.release()} (Build {platform.version()})"
