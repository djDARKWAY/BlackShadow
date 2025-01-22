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

from utils.ansiColors import RED, RESET

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
# Sub Menus ("subMenu" is an intermediary between a menu and final options to activate a feature)
def subMenuBrowsers():
    options = [
        ("1", "Passwords"),
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
# Sub Options ("subOption" is a submenu in which the option activates a feature)
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
    print(f"Username: {systemInfo.getUsername()}")
    print(f"Computer Name: {systemInfo.getComputerName()}")
    print(f"OS Version: {systemInfo.getOsVersion()}")
    print(f"Architecture: {systemInfo.getArchitecture()}")
    print(f"Domain: {systemInfo.getDomain()}\n")
def showHardwareDetails():
    # CPU Information
    cpuInfo = hardwareInfo.getCpu()
    print("CPU:")
    print(f"► {cpuInfo['cpuModel']}")
    print(f"  └ Cores: {cpuInfo['cores']} ({cpuInfo['threads']} threads)")

    # GPU Information
    gpuInfo = hardwareInfo.getGpu()
    print("\nGPU:")
    for gpu in gpuInfo:
        print(f"► {gpu['gpuModel']}")
        print(f"  ├ VRAM: {gpu['memory']:.2f} MB")
        print(f"  └ Driver version: {gpu['driverVersion']}")

    # RAM Information
    ramInfo = hardwareInfo.getRam()
    print("\nRAM:")
    print(f"► Total RAM: {ramInfo[0]['totalRam']:.2f} GB")
    for i, ram in enumerate(ramInfo[1:], start=1):
        connector = "└" if i == len(ramInfo) - 1 else "├"
        print(f"  {connector} RAM {i}: {ram['capacity']:.0f} GB - {ram['speed']}MHz {ram['type']} | {ram['manufacturer']} {ram['ramModel']}")

    # Disk Information
    diskInfo = hardwareInfo.getDisks()
    print("\nDisks:")
    print(f"► Total Memory: {sum(disk['total'] for disk in diskInfo)} GB")
    for i, disk in enumerate(diskInfo, start=1):
        connector = "└" if i == len(diskInfo) else "├"
        print(f"  {connector} [{disk['filesystem']}] {disk['mountPoint']} - Total: {disk['total']} GB (Used: {disk['used']} GB | Free: {disk['free']} GB)")
def showMonitorDetails():
    monitorInfo = hardwareInfo.getMonitor()
    print("\Monitors:")
    for i, monitor in enumerate(monitorInfo, start=1):
        print(f"► Monitor {i}")
        print(f"  ├ {monitor['displayIdentifier']} - {monitor['monitorName']}")
        print(f"  └ Resolution: {monitor['resolution']}x{monitor['resolutionHeight']}")

# Secondary functions
def pauseAndClear():
    input("---------------------------\nPress Enter to continue...")
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