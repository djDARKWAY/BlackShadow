import wmi
import winreg

def getSecureBootStatus():
    try:
        keyPath = r"SYSTEM\CurrentControlSet\Control\SecureBoot\State"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, keyPath) as key:
            secureBoot, _ = winreg.QueryValueEx(key, "UEFISecureBootEnabled")
            return "Enabled" if secureBoot == 1 else "Disabled"
    except FileNotFoundError:
        return "Secure Boot not supported"
    except Exception as e:
        return f"Unknown ({e})"
    
def getBootMode():
    try:
        keyPath = r"SYSTEM\CurrentControlSet\Control\SecureBoot"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, keyPath) as key:
            return "UEFI"
    except FileNotFoundError:
        return "Legacy (BIOS)"
    except Exception as e:
        return f"Unknown ({e})"

def getMotherboard():
    c = wmi.WMI()
    board = c.Win32_BaseBoard()[0]
    
    motherboardInfo = {
        "manufacturer": board.Manufacturer.strip() if board.Manufacturer else "Unknown",
        "model": board.Product.strip() if board.Product else "Unknown",
        "secureBoot": getSecureBootStatus(),
        "bootMode": getBootMode(),
    }
    
    return motherboardInfo
