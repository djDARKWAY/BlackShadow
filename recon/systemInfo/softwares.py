import winreg

def getSoftwares():
    registry_paths = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),  # 64-bit
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),  # 32-bit (64-bit Windows)
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),  # Actual user
    ]

    programs = []

    for hkey, path in registry_paths:
        try:
            registry = winreg.OpenKey(hkey, path)
            for i in range(winreg.QueryInfoKey(registry)[0]):
                try:
                    subkey_name = winreg.EnumKey(registry, i)
                    subkey = winreg.OpenKey(registry, subkey_name)

                    name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                    try:
                        version = winreg.QueryValueEx(subkey, "DisplayVersion")[0]
                    except FileNotFoundError:
                        version = "Unknown"

                    try:
                        install_location = winreg.QueryValueEx(subkey, "InstallLocation")[0]
                    except FileNotFoundError:
                        install_location = "Unknown"

                    programs.append({
                        "name": name,
                        "version": version,
                        "install_location": install_location
                    })

                except FileNotFoundError:
                    continue

            winreg.CloseKey(registry)
        except FileNotFoundError:
            continue

    programs = sorted(programs, key=lambda x: x['name'].lower())

    return programs

