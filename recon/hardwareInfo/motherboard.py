import wmi
import winreg

def getSecureBootStatus():
    try:
        key_path = r"SYSTEM\CurrentControlSet\Control\SecureBoot\State"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
            secure_boot, _ = winreg.QueryValueEx(key, "UEFISecureBootEnabled")
            return "Enabled" if secure_boot == 1 else "Disabled"
    except FileNotFoundError:
        return "Secure Boot not supported"
    except Exception as e:
        return f"Unknown ({e})"
    
def getBootMode():
    try:
        key_path = r"SYSTEM\CurrentControlSet\Control\SecureBoot"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
            return "UEFI"
    except FileNotFoundError:
        return "Legacy (BIOS)"
    except Exception as e:
        return f"Unknown ({e})"

def getMotherboard():
    c = wmi.WMI()
    board = c.Win32_BaseBoard()[0]
    
    motherboard_info = {
        "manufacturer": board.Manufacturer.strip() if board.Manufacturer else "Unknown",
        "model": board.Product.strip() if board.Product else "Unknown",
        "secureBoot": getSecureBootStatus(),
        "bootMode": getBootMode(),
    }
    
    return motherboard_info