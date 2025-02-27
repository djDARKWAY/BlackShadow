import os
import sys
import subprocess

os.system('cls' if os.name == 'nt' else 'clear')
print("Verifiying dependencies...")
print("--------------------------------------")
def readRequirements():
    with open("requirements.txt", "r") as f:
        return f.read().splitlines()
def installPackage(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
def uninstallPackage(package):
    subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", package])

requiredPackages = readRequirements()
for package in requiredPackages:
    try:
        __import__(package)
    except ImportError:
        installPackage(package)

import curses
import threading
import itertools
import time
import re
from browsers import operaGX, chrome, edge, brave, vivaldi
from recon import systemInfo, hardwareInfo, networkInfo, securityInfo
from utils.ansiColors import BOLD_RED, BOLD_YELLOW, BOLD_GREEN, GRAY, RESET
from utils.logo import showLogo as showLogoUtils

# Logo
def showLogo(screen):
    logo = r"""
     ⠀⠀⠀⢀⣴⣿⣿⣿⣦
     ⠀⠀⣰⣿⡟⢻⣿⡟⢻⣧        ____  __           __   _____ __              __              
    ⠀⠀⣰⣿⣿⣇⣸⣿⣇⣸⣿       / __ )/ /___  _____/ /__/ ___// /_  ____  ____/ /_____      __
    ⠀⣴⣿⣿⣿⣿⠟⢻⣿⣿⣿      / __  / / __ \/ ___/ //_/\__ \/ __ \/ __ \/ __  / __ \ | /| / /
   ⣠⣾⣿⣿⣿⣿⣿⣤⣼⣿⣿⡇     / /_/ / / /_/ / /__/ , < ___/ / / / / /_/ / /_/ / /_/ / |/ |/ / 
   ⢿⡿⢿⣿⣿⣿⣿⣿⣿⣿⡿⠀    /_____/_/\__,__\___/_/|_|/____/_/ /_/\__,__\__,_/\____/|__/|__/  
   ⠀⠀⠀⠈⠿⠿⠋⠙⠿⠛⠁
    """
    screen.addstr(logo)
    screen.refresh()
# Menu and controls functions
def displayMenu(screen, options, currentOption, title):
    screen.clear()
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    showLogo(screen)
    titleStartY = 9
    titleStartX = 5
    screen.addstr(titleStartY, titleStartX, title, curses.color_pair(1) | curses.A_BOLD)
    menuStartY = 10
    for idx, (option, description) in enumerate(options):
        displayIdx = menuStartY + idx if idx < len(options) - 1 else menuStartY + idx + 1
        if idx == currentOption:
            screen.addstr(displayIdx, 5, f"› {description}", curses.A_REVERSE)
        else:
            screen.addstr(displayIdx, 5, f"  {description}")
    screen.refresh()
def handleInput(key, currentOption, options):
    if key == curses.KEY_UP:
        currentOption = (currentOption - 1) % len(options)
    elif key == curses.KEY_DOWN:
        currentOption = (currentOption + 1) % len(options)
    elif key in [curses.KEY_ENTER, 10, 13]:
        return options[currentOption][0], currentOption
    elif key == 27:
        return '0', currentOption
    return None, currentOption
def mainMenuControl():
    options = [
        ("1", "Web Forensics"),
        ("2", "System Overview"),
        ("3", "Network Insights"),
        ("4", "Security Audit"),
        ("0", "Exit")
    ]
    currentOption = 0
    selectedOption = None

    def menuLogic(screen):
        nonlocal selectedOption, currentOption
        while selectedOption is None:
            displayMenu(screen, options, currentOption, "MAIN MENU")
            key = screen.getch()
            selectedOption, currentOption = handleInput(key, currentOption, options)

    curses.wrapper(menuLogic)
    return selectedOption
# Sub Menus (intermediary between a menu and final options to activate a feature)
def subMenuBrowsers():
    options = [
        ("1", "Password Extraction"),
        ("2", "Tracking Data (Cookies)"),
        ("3", "Browsing History"),
        ("0", "Back")
    ]
    currentOption = 0
    selectedOption = None

    def menuLogic(screen):
        nonlocal selectedOption, currentOption
        while selectedOption is None:
            displayMenu(screen, options, currentOption, "WEB FORENSICS")
            key = screen.getch()
            selectedOption, currentOption = handleInput(key, currentOption, options)

    curses.wrapper(menuLogic)
    return selectedOption
def subMenuNetwork():
    options = [
        ("1", "Network Interfaces"),
        ("2", "Port Scanning"),
        ("3", "Wifi Credentials"),
        ("4", "Geolocation"),
        ("0", "Back")
    ]
    currentOption = 0
    selectedOption = None

    def menuLogic(screen):
        nonlocal selectedOption, currentOption
        while selectedOption is None:
            displayMenu(screen, options, currentOption, "NETWORK INSIGHTS")
            key = screen.getch()
            selectedOption, currentOption = handleInput(key, currentOption, options)

    curses.wrapper(menuLogic)
    return selectedOption
# Sub Options (submenu in which the option activates a feature)
def subOptionsBrowsers():
    options = [
        ("1", "Brave"),
        ("2", "Google Chrome"),
        ("3", "Microsoft Edge"),
        ("4", "Opera GX"),
        ("5", "Vivaldi"),
        ("0", "Back")
    ]
    currentOption = 0
    selectedOption = None

    def subMenuLogic(screen):
        nonlocal selectedOption, currentOption
        while selectedOption is None:
            displayMenu(screen, options, currentOption, "BROWSER SELECTION")
            key = screen.getch()
            selectedOption, currentOption = handleInput(key, currentOption, options)
    curses.wrapper(subMenuLogic)
    return selectedOption
def subOptionsSystemInformation():
    options = [
        ("1", "System Details"),
        ("2", "Hardware Specs"),
        ("3", "Screen Overview"),
        ("4", "Software Inventory"),
        ("5", "System Logs"),
        ("0", "Back")
    ]
    currentOption = 0
    selectedOption = None

    def menuLogic(screen):
        nonlocal selectedOption, currentOption
        while selectedOption is None:
            displayMenu(screen, options, currentOption, "SYSTEM OVERVIEW")
            key = screen.getch()
            selectedOption, currentOption = handleInput(key, currentOption, options)

    curses.wrapper(menuLogic)
    return selectedOption
def subOptionsPorts():
    options = [
        ("1", "ALL"),
        ("2", "ESTABLISHED"),
        ("3", "LISTEN"),
        ("4", "CLOSE_WAIT"),
        ("5", "TIME_WAIT"),
        ("6", "SYN"),
        ("7", "CLOSING"),
        ("8", "FIN_WAIT"),
        ("9", "NONE"),
        ("0", "Back")
    ]
    currentOption = 0
    selectedOption = None

    def subMenuLogic(screen):
        nonlocal selectedOption, currentOption
        while selectedOption is None:
            displayMenu(screen, options, currentOption, "PORTS")
            key = screen.getch()
            selectedOption, currentOption = handleInput(key, currentOption, options)

    curses.wrapper(subMenuLogic)
    if selectedOption == '0':
        return

    statesMapping = {
        '1': None,
        '2': ["ESTABLISHED"],
        '3': ["LISTEN"],
        '4': ["CLOSE_WAIT"],
        '5': ["TIME_WAIT"],
        '6': ["SYN"],
        '7': ["CLOSING"],
        '8': ["FIN_WAIT"],
        '9': ["NONE"]
    }

    filterStates = statesMapping.get(selectedOption)
    showOpenPortsDetails(filterStates)
def subOptionsSecurity():
    options = [
        ("1", "Firewall & Antivirus"),
        ("2", "User Profile"),
        ("0", "Back")
    ]
    currentOption = 0
    selectedOption = None

    def subMenuLogic(screen):
        nonlocal selectedOption, currentOption
        while selectedOption is None:
            displayMenu(screen, options, currentOption, "SECURITY AUDIT")
            key = screen.getch()
            selectedOption, currentOption = handleInput(key, currentOption, options)
    curses.wrapper(subMenuLogic)
    return selectedOption

# Main functions
def showSystemDetails():
    stopEvent = threading.Event()
    loaderThread = threading.Thread(target=loadingAnimation, args=(stopEvent,))
    loaderThread.start()

    systemData = systemInfo.getDateTime()
    bios = systemInfo.getBios()
    directX = systemInfo.getDirectXVersion()

    stopEvent.set()
    loaderThread.join()

    showLogoUtils()
    print(f"======================================")
    print(f"         ** SYSTEM DETAILS **         ")
    print(f"======================================")

    details = {
        "Username": systemInfo.getUsername(),
        "Computer name": systemInfo.getComputerName(),
        "OS version": systemInfo.getOsVersion(),
        "Architecture": systemInfo.getArchitecture(),
        "Domain": systemInfo.getDomain(),
        "Date & time": f"{systemData['currentDate']} {systemData['currentTime']}",
        "Timezone": systemData['timezone'],
        "DirectX version": directX,
        "Language": systemInfo.getLanguage(),
        "Manufacturer": bios['manufacturer'],
        "Version": bios['version'],
        "Release date": bios['releaseDate'],
        "Serial number": bios['serialNumber']
    }

    for key, value in details.items():
        print(f"{BOLD_GREEN}{key:<17}:{RESET} {value}")

    pauseAndClear()
def showHardwareDetails():
    stopEvent = threading.Event()
    loaderThread = threading.Thread(target=loadingAnimation, args=(stopEvent,))
    loaderThread.start()

    cpuInfo = hardwareInfo.getCpu()
    gpuInfo = hardwareInfo.getGpu()
    ramInfo = hardwareInfo.getRam()
    diskInfo = hardwareInfo.getDisks()
    motherboardInfo = hardwareInfo.getMotherboard()

    stopEvent.set()
    loaderThread.join()

    showLogoUtils()
    print(f"======================================")
    print(f"        ** HARDWARE DETAILS **        ")
    print(f"======================================")

    print(f"{BOLD_GREEN}►{GRAY} MOTHERBOARD:")
    details = {
        "Model": motherboardInfo['model'],
        "Manufacturer": motherboardInfo['manufacturer'],
        "Boot Mode": motherboardInfo['bootMode'],
        "Secure Boot": motherboardInfo['secureBoot']
    }
    for key, value in details.items():
        print(f"{BOLD_GREEN}{key:<17}:{RESET} {value}")

    print(f"\n{BOLD_GREEN}►{GRAY} CPU:")
    details = {
        "Model": cpuInfo['cpuModel'],
        "Cores/Threads": f"{cpuInfo['cores']}C/{cpuInfo['threads']}T",
        "Base Clock": f"{cpuInfo['baseClock']} GHz"
    }
    for key, value in details.items():
        print(f"{BOLD_GREEN}{key:<17}:{RESET} {value}")

    print(f"\n{BOLD_GREEN}►{GRAY} GPU:")
    for i, gpu in enumerate(gpuInfo, start=1):
        print(f"{BOLD_GREEN}GPU {i}:{RESET}")
        details = {
            "├ Model": gpu['gpuModel'],
            "├ VRAM": f"{gpu['memory']:.2f} MB",
            "└ Driver Version": gpu['driverVersion']
        }
        for key, value in details.items():
            print(f"{BOLD_GREEN}{key:<17}:{RESET} {value}")

    print(f"\n{BOLD_GREEN}►{GRAY} RAM:")
    for i, ram in enumerate(ramInfo[1:], start=1):
        connector = "└" if i == len(ramInfo[1:]) else "├"
        details = f"{ram['capacity']:.0f} GB - {ram['speed']} MHz - {ram['type']} | {ram['manufacturer']} {ram['ramModel']}"
        print(f"{BOLD_GREEN}{connector} #{i:<14}:{RESET} {details}")
    print(f"{BOLD_GREEN}Total RAM:{RESET} {ramInfo[0]['totalRam']:.2f} GB")

    print(f"\n{BOLD_GREEN}►{GRAY} DISKS:")
    for i, disk in enumerate(diskInfo, start=1):
        connector = "└" if i == len(diskInfo) else "├"
        details = f"{disk['total']:.2f} GB (Used: {disk['used']:.2f} GB - Free: {disk['free']:.2f} GB) [{disk['filesystem']}]"
        print(f"{BOLD_GREEN}{connector} #{i:<14}:{RESET} {details}")
    print(f"{BOLD_GREEN}Total Memory:{RESET} {sum(disk['total'] for disk in diskInfo):.2f} GB")
    
    pauseAndClear()
def showMonitorDetails():
    stopEvent = threading.Event()
    loaderThread = threading.Thread(target=loadingAnimation, args=(stopEvent,))
    loaderThread.start()

    monitorInfo = hardwareInfo.getMonitor()

    stopEvent.set()
    loaderThread.join()

    showLogoUtils()
    print(f"=======================================")
    print(f"         ** MONITOR DETAILS **         ")
    print(f"=======================================")

    if monitorInfo:
        for i, monitor in enumerate(monitorInfo, start=1):
            print(f"{BOLD_GREEN}► {GRAY}Monitor {i}:{RESET}")
            details = {
                "├ Identifier   ": monitor['displayIdentifier'],
                "├ Name         ": monitor['monitorName'],
                "├ Resolution   ": monitor['resolution'],
                "├ Refresh rate ": f"{monitor['refreshRate']} Hz",
                "└ Output       ": monitor['output']
            }
            for key, value in details.items():
                print(f"{BOLD_GREEN}{key:<17}:{RESET} {value}")
            
            if i != len(monitorInfo):
                print()
    else:
        print(f"{BOLD_RED}No monitors found.{RESET}")

    pauseAndClear()
def showInterfacesDetails():
    stopEvent = threading.Event()
    loaderThread = threading.Thread(target=loadingAnimation, args=(stopEvent,))
    loaderThread.start()

    networkData = networkInfo.getInterfaces()

    stopEvent.set()
    loaderThread.join()

    showLogoUtils()
    print(f"========================================")
    print(f"        ** INTERFACES DETAILS **        ")
    print(f"========================================")

    outputs = []
    for interface in networkData['interfaces']:
        outputs.append(f"{BOLD_GREEN}► {GRAY}Interface:{interface['interface']}")
        outputs.append(f"{BOLD_GREEN}├ IPv4    :{RESET} {interface['ipv4']}")
        outputs.append(f"{BOLD_GREEN}├ IPv6    :{RESET} {interface['ipv6']}")
        outputs.append(f"{BOLD_GREEN}└ Netmask :{RESET} {interface['netmask']}")
        outputs.append("")

    for line in outputs[:-1]:
        print(line)
    
    pauseAndClear()
def showOpenPortsDetails(filterStates=None):
    stopEvent = threading.Event()
    loaderThread = threading.Thread(target=loadingAnimation, args=(stopEvent,))
    loaderThread.start()

    portsData = networkInfo.getOpenPorts(filterStates=filterStates)

    stopEvent.set()
    loaderThread.join()

    showLogoUtils()
    print(f"====================================")
    print(f"          ** OPEN PORTS **          ")
    print(f"====================================")

    if not portsData:
        print(f"{BOLD_RED}No active network connections.{RESET}")
    else:
        for port in portsData:
            print(f"{BOLD_GREEN}► {GRAY}Address  :{RESET} {port['Local Address']} → {port['Remote Address']}")
            print(f"{BOLD_GREEN}├ Status   :{RESET} {port['Status']}")
            print(f"{BOLD_GREEN}├ PID      :{RESET} {port['PID']}")
            print(f"{BOLD_GREEN}└ Protocol :{RESET} {port['Protocol']}")
            if portsData.index(port) != len(portsData) - 1:
                print("")

    pauseAndClear()
def showInstalledSoftware():
        stopEvent = threading.Event()
        loaderThread = threading.Thread(target=loadingAnimation, args=(stopEvent,))
        loaderThread.start()

        softwareData = systemInfo.getSoftwares()

        stopEvent.set()
        loaderThread.join()

        showLogoUtils()
        print(f"======================================")
        print(f"       ** INSTALLED SOFTWARE **       ")
        print(f"======================================")

        if not softwareData:
            print(f"{BOLD_RED}No software found.{RESET}")
        else:
            for software in softwareData:
                print(f"{BOLD_GREEN}{software['name']}{GRAY} - {software['version']}{RESET}")


        pauseAndClear()
def showLogsDetails():
    stopEvent = threading.Event()
    loaderThread = threading.Thread(target=loadingAnimation, args=(stopEvent,))
    loaderThread.start()

    logsData = systemInfo.getSystemLogs()

    stopEvent.set()
    loaderThread.join()

    showLogoUtils()
    print(f"======================================")
    print(f"          ** SYSTEM LOGS **           ")
    print(f"======================================")

    if not logsData:
        print(f"{BOLD_RED}No logs found.{RESET}")
    else:
        for log in logsData:
            print(f"{BOLD_GREEN}► {GRAY}Time:{RESET} {log['time']}")
            print(f"{BOLD_GREEN}├ Source:{RESET} {log['source']}")
            print(f"{BOLD_GREEN}├ Event ID:{RESET} {log['event_id']}")
            print(f"{BOLD_GREEN}├ Message:{RESET} {log['message']}")
            print(f"{BOLD_GREEN}└ Category:{RESET} {log['category']}")
            print()

    pauseAndClear()
def showSecurityWsFirewall():
    stopEvent = threading.Event()
    loaderThread = threading.Thread(target=loadingAnimation, args=(stopEvent,))
    loaderThread.start()

    firewallStatus = securityInfo.getFirewall()
    wsStatus = securityInfo.getWindowsDefender()

    stopEvent.set()
    loaderThread.join()

    showLogoUtils()
    print(f"======================================")
    print(f"       ** SECURITY ANALYSIS **       ")
    print(f"======================================")

    if not firewallStatus:
        print(f"{BOLD_RED}Firewall status not found.{RESET}")
    else:
        print(f"{BOLD_GREEN}Firewall Status: {RESET}{firewallStatus}")

    if not wsStatus:
        print(f"{BOLD_RED}Antivirus status not found.{RESET}")
    else:
        for key, label in {
            "AntivirusEnabled": "Antivirus",
            "BehaviorMonitorEnabled": "├ Behavior Monitor",
            "DefenderSignaturesOutOfDate": "├ Defender Signatures Out of Date",
            "IsTamperProtected": "├ Tamper Protection",
            "RealTimeProtectionEnabled": "├ Real Time Protection",
            "AntivirusSignatureVersion": "├ Antivirus Signature Version",
            "AntispywareEnabled": "├ Antispyware Protection",
            "LastFullScanTime": "├ Last Full Scan",
            "LastQuickScanTime": "├ Last Quick Scan",
            "IoavProtectionEnabled": "├ Malware Protection",
            "SmartAppControlState": "├ Smart App Control",
            "TamperProtectionSource": "├ Tamper Protection Source",
            "TDTCapable": "└ Real Time Detection Mode"
        }.items():
            if key in wsStatus:
                print(f"{BOLD_GREEN}{label}:{RESET} {wsStatus[key]}{RESET if key == 'TDTCapable' else ''}")

    pauseAndClear()
def showUserDetails():
    def separateUppercase(text):
        return re.sub(r'([a-z])([A-Z])', r'\1 \2', text)

    stopEvent = threading.Event()
    loaderThread = threading.Thread(target=loadingAnimation, args=(stopEvent,))
    loaderThread.start()

    userData = securityInfo.getUsers()

    stopEvent.set()
    loaderThread.join()

    showLogoUtils()  
    print(f"=======================================")
    print(f"       ** ACTIVE USER ACCOUNTS **      ")
    print(f"=======================================")

    if isinstance(userData, list) and not userData:
        print("No active user accounts found.")
        pauseAndClear()
        return

    outputs = []
    for account in userData:
        userName = account.get('Name', 'N/A')
        userName = separateUppercase(userName)
        outputs.append(f"{BOLD_GREEN}► {GRAY}User Account:{RESET} {userName}")

        for idx, (key, value) in enumerate(account.items()):
            if key != 'Name':
                key = separateUppercase(key)
                connector = "└" if idx == len(account.items()) - 1 else "├"
                outputs.append(f"{BOLD_GREEN}{connector} {key:<30}:{RESET} {value}")
        
        outputs.append("")

    for line in outputs[:-1]:
        print(line)
    
    pauseAndClear()
def showWifiPasswords():
    stopEvent = threading.Event()
    loaderThread = threading.Thread(target=loadingAnimation, args=(stopEvent,))
    loaderThread.start()
    
    wifiData = networkInfo.getWifiPasswords()
    
    stopEvent.set()
    loaderThread.join()

    showLogoUtils()
    print(f"=======================================")
    print(f"          ** Wi-Fi NETWORKS **         ")
    print(f"=======================================")

    if "error" in wifiData:
        print(f"{BOLD_RED}Error: {wifiData['error']}{RESET}")
    elif not wifiData:
        print(f"{BOLD_RED}No stored Wi-Fi networks found.{RESET}")
    else:
        categories = {
            "Protected Wi-Fi": (BOLD_GREEN, []),
            "Free Wi-Fi": (BOLD_YELLOW, []),
            "Failed to retrieve": (BOLD_RED, [])
        }

        for wifi in wifiData:
            ssid, password = wifi["SSID"], wifi["Password"]
            key = "Free Wi-Fi" if password == "-" else "Failed to retrieve" if password in ["Failed", "Error"] else "Protected Wi-Fi"
            categories[key][1].append((ssid, password))

        for title, (color, networks) in categories.items():
            if networks:
                print(f"\n{color}{title}:{RESET}")
                for ssid, password in networks:
                    if title == "Protected Wi-Fi":
                        print(f"{color}SSID: {RESET}{ssid:<32}: {RESET}{password}{RESET}")
                    else:
                        print(f"{color}SSID: {RESET}{ssid}{RESET}")

    pauseAndClear()
def showGeoLocationDetails():
    stopEvent = threading.Event()
    loaderThread = threading.Thread(target=loadingAnimation, args=(stopEvent,))
    loaderThread.start()

    networkData = networkInfo.getGeoLocation()

    stopEvent.set()
    loaderThread.join()

    showLogoUtils()
    print(f"========================================")
    print(f"        ** GEOLOCATION DETAILS **       ")
    print(f"========================================")

    print(f"{BOLD_GREEN}Local:{RESET} {networkData['localIp']}")
    print(f"{BOLD_GREEN}IPv4:{RESET} {networkData['publicIpv4']}")
    print(f"{BOLD_GREEN}IPv6:{RESET} {networkData['publicIpv6']}\n")
    
    print(f"{BOLD_GREEN}{networkData['geoData']['isp']}")
    print(f"{BOLD_GREEN}Location    : {RESET}{networkData['geoData']['city']}, "
        f"{networkData['geoData']['region']}, {networkData['geoData']['country']}")
    print(f"{BOLD_GREEN}Coordinates : {RESET}{networkData['geoData']['lat']}, "
        f"{networkData['geoData']['lon']}")
    print(f"{BOLD_GREEN}Zip Code    : {RESET}{networkData['geoData']['zip']}")
    
    pauseAndClear()

# Secondary functions
def pauseAndClear():
    print(f"=====================================")
    input("Press Enter to continue...")
    os.system('cls' if os.name == 'nt' else 'clear')
def loadingAnimation(stopEvent):
    showLogoUtils()
    for char in itertools.cycle(["|", "/", "-", "\\"]):
        if stopEvent.is_set():
            break
        sys.stdout.write(f"\rLoading... {char}")
        sys.stdout.flush()
        time.sleep(0.1)
    time.sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')
def createDxDiagFile():
    stopEvent = threading.Event()
    loaderThread = threading.Thread(target=loadingAnimation, args=(stopEvent,))
    loaderThread.start()

    if not os.path.exists("utils/dxdiag/dxdiag_output.txt"):
        subprocess.run("dxdiag /t utils/dxdiag/dxdiag_output.txt", shell=True, check=True)
    else:
        os.remove("utils/dxdiag/dxdiag_output.txt")
        subprocess.run("dxdiag /t utils/dxdiag/dxdiag_output.txt", shell=True, check=True)

    stopEvent.set()
    loaderThread.join()

createDxDiagFile()
os.system('cls' if os.name == 'nt' else 'clear')

def main():
    while True:
        choice = mainMenuControl()
        
        # Web Forensics
        if choice == '1':
            subChoice = subMenuBrowsers()

            if subChoice == '1': # Passwords
                subOption = subOptionsBrowsers()
                browserFunctions = {
                    '1': brave.getPasswords,
                    '2': chrome.getPasswords,
                    '3': edge.getPasswords,
                    '4': operaGX.getPasswords,
                    '5': vivaldi.getPasswords
                }
                if subOption in browserFunctions:
                    browserFunctions[subOption]()

                elif subOption == '0': # Back
                    continue

                pauseAndClear()
            elif subChoice == '2': # Cookies
                subOption = subOptionsBrowsers()
                browserFunctions = {
                    '3': edge.getCookies,
                    '4': operaGX.getCookies
                }
                if subOption in browserFunctions:
                    browserFunctions[subOption]()

                elif subOption == '0':
                    continue
                
                pauseAndClear()
            elif subChoice == '3': # History
                subOption = subOptionsBrowsers()
                browserFunctions = {
                    '3': edge.getHistory,
                    '4': operaGX.getHistory
                }
                if subOption in browserFunctions:
                    browserFunctions[subOption]()
                    
                elif subOption == '0':
                    continue
                
                pauseAndClear()
            elif subChoice == '0': # Back
                continue
        
        # System Overview
        if choice == '2':
            subOption = subOptionsSystemInformation()
            
            Functions = {
                '1': showSystemDetails,
                '2': showHardwareDetails,
                '3': showMonitorDetails,
                '4': showInstalledSoftware,
                '5': showLogsDetails
            }
            if subOption in Functions:
                Functions[subOption]()

            elif subOption == '0': # Back
                continue

        # Network Insights
        if choice == '3':
            subOption = subMenuNetwork()
            
            systemFunctions = {
                '1': showInterfacesDetails,
                '2': subOptionsPorts,
                '3': showWifiPasswords,
                '4': showGeoLocationDetails
            }
            if subOption in systemFunctions:
                systemFunctions[subOption]()

            elif subOption == '0': # Back
                continue
        
        # Security Audits
        if choice == '4':
            subOption = subOptionsSecurity()
            
            Functions = {
                '1': showSecurityWsFirewall,
                '2': showUserDetails
            }
            if subOption in Functions:
                Functions[subOption]()

            elif subOption == '0': # Back
                continue
        
        # Exit
        elif choice == '0':
            if os.path.exists("utils/dxdiag/dxdiag_output.txt"):
                os.remove("utils/dxdiag/dxdiag_output.txt")
            os.system('cls' if os.name == 'nt' else 'clear')
            break

if __name__ == "__main__":
    main()