import os
import sys
import subprocess
'''
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
'''
import curses
from browsers import operaGX, chrome, edge, brave, vivaldi
from recon import systemInfo, hardwareInfo

from utils.ansiColors import BOLD_RED, BOLD_GREEN, RESET

os.system('cls' if os.name == 'nt' else 'clear')

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
    titleStartY = 10
    titleStartX = 5
    screen.addstr(titleStartY, titleStartX, title, curses.color_pair(1) | curses.A_BOLD)
    menuStartY = 11
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
        ("1", "Browser Tools"),
        ("2", "System Information"),
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
        ("1", "Passwords"),
        ("2", "Cookies"),
        ("0", "Back")
    ]
    currentOption = 0
    selectedOption = None

    def menuLogic(screen):
        nonlocal selectedOption, currentOption
        while selectedOption is None:
            displayMenu(screen, options, currentOption, "TOOLS")
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
        ("2", "Hardware Information"),
        ("3", "Screen Information"),
        ("0", "Back")
    ]
    currentOption = 0
    selectedOption = None

    def menuLogic(screen):
        nonlocal selectedOption, currentOption
        while selectedOption is None:
            displayMenu(screen, options, currentOption, "SYSTEM INFORMATION")
            key = screen.getch()
            selectedOption, currentOption = handleInput(key, currentOption, options)

    curses.wrapper(menuLogic)
    return selectedOption
# Main functions
def showSystemDetails():
    systemData = systemInfo.getDateTime()
    bios = systemInfo.getBios()

    print(f"=====================================")
    print(f"         ** SYSTEM DETAILS **        ")
    print(f"=====================================")

    details = {
        "Username": systemInfo.getUsername(),
        "Computer name": systemInfo.getComputerName(),
        "OS version": systemInfo.getOsVersion(),
        "Architecture": systemInfo.getArchitecture(),
        "Domain": systemInfo.getDomain(),
        "Date & time": f"{systemData['currentDate']} {systemData['currentTime']}",
        "Timezone": systemData['timezone'],
        "DirectX version": systemInfo.getDirectXVersion(),
        "Language": systemInfo.getLanguage(),
        "Manufacturer": bios['manufacturer'],
        "Version": bios['version'],
        "Release date": bios['releaseDate'],
        "Serial number": bios['serialNumber']
    }

    for key, value in details.items():
        print(f"{BOLD_GREEN}{key:<20}:{RESET} {value}")
    print(f"=====================================")
def showHardwareDetails():
    cpuInfo = hardwareInfo.getCpu()
    gpuInfo = hardwareInfo.getGpu()
    ramInfo = hardwareInfo.getRam()
    diskInfo = hardwareInfo.getDisks()
    motherboardInfo = hardwareInfo.getMotherboard()

    print(f"=====================================")
    print(f"        ** HARDWARE DETAILS **       ")
    print(f"=====================================")

    print(f"            ** MOTHERBOARD **")
    details = {
        "Model": motherboardInfo['model'],
        "Manufacturer": motherboardInfo['manufacturer'],
        "Boot Mode": motherboardInfo['bootMode'],
        "Secure Boot": motherboardInfo['secureBoot']
    }
    for key, value in details.items():
        print(f"{BOLD_GREEN}{key:<20}:{RESET} {value}")

    print(f"\n                ** CPU **")
    details = {
        "Model": cpuInfo['cpuModel'],
        "Cores/Threads": f"{cpuInfo['cores']}C/{cpuInfo['threads']}T",
        "Base Clock": f"{cpuInfo['baseClock']} GHz"
    }
    for key, value in details.items():
        print(f"{BOLD_GREEN}{key:<20}:{RESET} {value}")

    print(f"\n                ** GPU **")
    for i, gpu in enumerate(gpuInfo, start=1):
        print(f"{BOLD_GREEN}GPU {i}:{RESET}")
        details = {
            "├ Model": gpu['gpuModel'],
            "├ VRAM": f"{gpu['memory']:.2f} MB",
            "└ Driver Version": gpu['driverVersion']
        }
        for key, value in details.items():
            print(f"{BOLD_GREEN}{key:<20}:{RESET} {value}")

    print(f"\n                ** RAM **")
    print(f"{BOLD_GREEN}Total RAM:{RESET} {ramInfo[0]['totalRam']:.2f} GB")
    for i, ram in enumerate(ramInfo[1:], start=1):
        connector = "└" if i == len(ramInfo[1:]) else "├"
        details = f"{ram['capacity']:.0f} GB - {ram['speed']} MHz - {ram['type']} | {ram['manufacturer']} {ram['ramModel']}"
        print(f"{BOLD_GREEN}{connector} RAM {i:<14}:{RESET} {details}")

    print(f"\n               ** DISKS **")
    print(f"{BOLD_GREEN}Total Memory:{RESET} {sum(disk['total'] for disk in diskInfo):.2f} GB")
    for i, disk in enumerate(diskInfo, start=1):
        connector = "└" if i == len(diskInfo) else "├"
        details = f"{disk['total']:.2f} GB (Used: {disk['used']:.2f} GB - Free: {disk['free']:.2f} GB) [{disk['filesystem']}]"
        print(f"{BOLD_GREEN}{connector} Disk {i:<13}:{RESET} {details}")
def showMonitorDetails():
    monitorInfo = hardwareInfo.getMonitor()

    print(f"=====================================")
    print(f"         ** MONITOR DETAILS **       ")
    print(f"=====================================")

    if monitorInfo:
        for i, monitor in enumerate(monitorInfo, start=1):
            print(f"{BOLD_GREEN}Monitor {i}:{RESET}")
            details = {
                "├ Identifier   ": monitor['displayIdentifier'],
                "├ Name         ": monitor['monitorName'],
                "├ Resolution   ": monitor['resolution'],
                "├ Refresh rate ": f"{monitor['refreshRate']} Hz",
                "└ Output       ": monitor['output']
            }
            for key, value in details.items():
                print(f"{BOLD_GREEN}{key:<20}:{RESET} {value}")
    else:
        print(f"{BOLD_RED}No monitors found.{RESET}")
    print(f"=====================================")

# Secondary functions
def pauseAndClear():
    input("Press Enter to continue...")
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    while True:
        choice = mainMenuControl()
        
        # Browser Tools
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
                }
                if subOption in browserFunctions:
                    browserFunctions[subOption]()

                elif subOption == '0':
                    continue
                
                pauseAndClear()
            
            elif subChoice == '0': # Back
                continue
        
        # System Information
        if choice == '2':
            subOption = subOptionsSystemInformation()
            
            systemFunctions = {
                '1': showSystemDetails,
                '2': showHardwareDetails,
                '3': showMonitorDetails
            }
            if subOption in systemFunctions:
                systemFunctions[subOption]()

            elif subOption == '0': # Back
                continue
            
            pauseAndClear()

        # Exit
        elif choice == '0':
            os.system('cls' if os.name == 'nt' else 'clear')
            break

if __name__ == "__main__":
    main()