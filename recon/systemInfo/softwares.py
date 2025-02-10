import winreg

def getSoftwares():
    registryPaths = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"), # 64-bit
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
    ]

    programs = []

    for hkey, path in registryPaths:
        try:
            registry = winreg.OpenKey(hkey, path)
            for i in range(winreg.QueryInfoKey(registry)[0]):
                try:
                    subkeyName = winreg.EnumKey(registry, i)
                    subkey = winreg.OpenKey(registry, subkeyName)

                    name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                    try:
                        version = winreg.QueryValueEx(subkey, "DisplayVersion")[0]
                    except FileNotFoundError:
                        version = "Unknown"

                    try:
                        installLocation = winreg.QueryValueEx(subkey, "InstallLocation")[0]
                    except FileNotFoundError:
                        installLocation = "Unknown"

                    programs.append({
                        "name": name,
                        "version": version,
                        "installLocation": installLocation
                    })

                except FileNotFoundError:
                    continue

            winreg.CloseKey(registry)
        except FileNotFoundError:
            continue

    programs = sorted(programs, key=lambda x: x['name'].lower())

    return programs
