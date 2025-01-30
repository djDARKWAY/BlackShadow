import winreg

def getSoftwares():
    uninstallKey = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
    
    try:
        registry = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, uninstallKey)
    except FileNotFoundError:
        return {}

    programs = []
    
    for i in range(0, winreg.QueryInfoKey(registry)[0]):
        try:
            subkeyName = winreg.EnumKey(registry, i)
            subkey = winreg.OpenKey(registry, subkeyName)
            
            name = winreg.QueryValueEx(subkey, "DisplayName")[0]
            try:
                version = winreg.QueryValueEx(subkey, "DisplayVersion")[0]
            except FileNotFoundError:
                version = "Unknown"

            programs.append({
                "name": name,
                "version": version
            })
        except FileNotFoundError:
            continue

    winreg.CloseKey(registry)
    
    programs = sorted(programs, key=lambda x: x['name'].lower())
    return {program['name']: program['version'] for program in programs}
