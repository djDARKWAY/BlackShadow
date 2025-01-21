import os
import sys
import subprocess
import curses
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
from browsers.operaGX import getPasswords as getPasswordsOperaGX
from browsers.chrome import getPasswords as getPasswordsChrome
from browsers.edge import getPasswords as getPasswordsEdge
from browsers.brave import getPasswords as getPasswordsBrave
from browsers.vivaldi import getPasswords as getPasswordsVivaldi
from utils.ansiColors import RED, RESET

os.system('cls' if os.name == 'nt' else 'clear')

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

# Menu functions and logic
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
        ("1", "Browser tools"),
        ("2", "System information"),
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
# Submenus
def submenuPasswords():
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
            displayMenu(screen, options, currentOption, "PASSWORD SELECTION")
            key = screen.getch()
            selectedOption, currentOption = handleInput(key, currentOption, options)
    curses.wrapper(subMenuLogic)
    return selectedOption
def submenuSystemInformation():
    options = [
        ("1", "System Scan"),
        ("0", "Back")
    ]
    currentOption = 0
    selectedOption = None

    def subMenuLogic(screen):
        nonlocal selectedOption, currentOption
        while selectedOption is None:
            displayMenu(screen, options, currentOption, "-")
            key = screen.getch()
            selectedOption, currentOption = handleInput(key, currentOption, options)
    
    while True:
        curses.wrapper(subMenuLogic)
        
        if selectedOption == '1':
            subchoice = submenuSystemScan()
            if subchoice == '0':
                selectedOption = None
                continue
            else:
                return subchoice
        elif selectedOption == '0':
            return selectedOption
# Suboptions
def subOptionsBrowsers():
    options = [
        ("1", "Passwords"),
        ("0", "Back")
    ]
    currentOption = 0
    selectedOption = None

    def subMenuLogic(screen):
        nonlocal selectedOption, currentOption
        while selectedOption is None:
            displayMenu(screen, options, currentOption, "BROWSER MENU")
            key = screen.getch()
            selectedOption, currentOption = handleInput(key, currentOption, options)
    
    while True:
        curses.wrapper(subMenuLogic)
        
        if selectedOption == '1':
            subchoice = submenuPasswords()
            if subchoice == '0':
                selectedOption = None  # Voltar ao menu de navegadores
                continue
            else:
                return subchoice  # Retornar a opção do navegador selecionado
        elif selectedOption == '0':
            return selectedOption
def submenuSystemScan():
    options = [
        ("1", "Scan for sensitive files"),
        ("2", "Scan for sensitive data"),
        ("0", "Back")
    ]
    currentOption = 0
    selectedOption = None

    def subMenuLogic(screen):
        nonlocal selectedOption, currentOption
        while selectedOption is None:
            displayMenu(screen, options, currentOption, "SYSTEM SCAN MENU")
            key = screen.getch()
            selectedOption, currentOption = handleInput(key, currentOption, options)
    curses.wrapper(subMenuLogic)
    return selectedOption

def main():
    browserPasswords = {
        '1': getPasswordsBrave,
        '2': getPasswordsChrome,
        '3': getPasswordsEdge,
        '4': getPasswordsOperaGX,
        '5': getPasswordsVivaldi
    }

    systemScanFunctions = {
        '1': None,
        '2': None
    }

    while True:
        choice = mainMenuControl()
        # Browser tool
        if choice == '1':
            while True:
                subchoice = subOptionsBrowsers()
                if subchoice == '0':
                    break

                func = browserPasswords.get(subchoice)
                if func:
                    try:
                        func()
                    except Exception as e:
                        print(f"{RED}An error occurred: {e}{RESET}")
                else:
                    print(f"{RED}Invalid option!{RESET}")

                input("Press Enter to continue...")
                os.system('cls' if os.name == 'nt' else 'clear')
        # System information        
        elif choice == '2':
            while True:
                subchoice = submenuSystemInformation()
                if subchoice == '0':
                    break

                func = systemScanFunctions.get(subchoice)
                if func:
                    try:
                        func()
                    except Exception as e:
                        print(f"{RED}An error occurred: {e}{RESET}")
                else:
                    print(f"{RED}Invalid option!{RESET}")

                input("Press Enter to continue...")
                os.system('cls' if os.name == 'nt' else 'clear')
        elif choice == '0':
            os.system('cls' if os.name == 'nt' else 'clear')
            break

if __name__ == "__main__":
    main()
