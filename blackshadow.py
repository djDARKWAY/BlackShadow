import curses
import os
from browsers.operaGX import getPasswords

os.system('cls' if os.name == 'nt' else 'clear')

def showLogo(screen):
    logo = """
    ⠀⠀⠀⢀⣴⣿⣿⣿⣦
   ⠀⠀⠀⣰⣿⡟⢻⣿⡟⢻⣧        ____  __           __   _____ __              __              
  ⠀⠀⠀⣰⣿⣿⣇⣸⣿⣇⣸⣿       / __ )/ /___ ______/ /__/ ___// /_  ____ _____/ /___ _      __
   ⠀⣴⣿⣿⣿⣿⠟⢻⣿⣿⣿      / __  / / __ `/ ___/ //_/\__ \/ __ \/ __ `/ __  / __ \ | /| / /
  ⣠⣾⣿⣿⣿⣿⣿⣤⣼⣿⣿⡇     / /_/ / / /_/ / /__/ ,<  ___/ / / / / /_/ / /_/ / /_/ / |/ |/ / 
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
    title_start_y = 10
    title_start_x = 5
    screen.addstr(title_start_y, title_start_x, title, curses.color_pair(1) | curses.A_BOLD)
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
            displayMenu(screen, options, currentOption, "BLACKSHADOW MENU")
            key = screen.getch()
            selectedOption, currentOption = handleInput(key, currentOption, options)

    curses.wrapper(menuLogic)
    return selectedOption
def submenuBrowsers():
    options = [
        ("1", "Opera GX"),
        ("0", "Back")
    ]
    currentOption = 0
    selectedOption = None

    def subMenuLogic(screen):
        nonlocal selectedOption, currentOption
        while selectedOption is None:
            displayMenu(screen, options, currentOption, "SELECT A BROWSER")
            key = screen.getch()
            selectedOption, currentOption = handleInput(key, currentOption, options)
    curses.wrapper(subMenuLogic)
    return selectedOption

def main():
    choice = mainMenuControl()
    if choice == '1':
        subchoice = submenuBrowsers()
        if subchoice == '1':
            getPasswords()
        elif subchoice == '0':
            main()
    elif choice == '0':
        exit()

if __name__ == "__main__":
    main()
