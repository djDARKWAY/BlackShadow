import os
from pathlib import Path
import rookiepy
from datetime import datetime
from utils.ansiColors import BOLD_RED, BOLD_GREEN, GRAY, RESET
from utils.logo import showLogo as showLogoUtils

def getCookies():
    try:
        if os.system("tasklist | findstr opera.exe") == 0:
            os.system("taskkill /F /IM opera.exe")
            os.system('cls' if os.name == 'nt' else 'clear')

        showLogoUtils()

        dbPath = Path(os.path.expanduser("~")) / 'AppData/Roaming/Opera Software/Opera GX Stable/Network/Cookies'
        keyPath = Path(os.path.expanduser("~")) / 'AppData/Roaming/Opera Software/Opera GX Stable/Local State'

        cookies = rookiepy.any_browser(db_path=str(dbPath), key_path=str(keyPath), domains=None)

        if cookies:
            print("===================================")
            print("      ** DECRYPTED COOKIES **      ")
            print("===================================")
            for cookie in cookies:
                domain = cookie.get('domain', 'N/A')
                name = cookie.get('name', 'N/A')
                value = cookie.get('value', 'N/A')
                expires = cookie.get('expires', 'N/A')
                secure = cookie.get('secure', 'N/A')
                httpOnly = cookie.get('http_only', 'N/A')
                sameSite = { -1: "Unspecified", 0: "Strict", 1: "Lax" }.get(cookie.get('same_site', 'N/A'), "Unknown")

                if expires != 'N/A' and isinstance(expires, int):
                    expires = datetime.utcfromtimestamp(expires).strftime('%Y-%m-%d %H:%M:%S')

                print(f"{BOLD_GREEN}► {GRAY}{name}")
                print(f"{BOLD_GREEN}├ Domain    : {RESET}{domain}")
                print(f"{BOLD_GREEN}├ Value     : {RESET}{value}")
                print(f"{BOLD_GREEN}├ Expires   : {RESET}{expires}")
                print(f"{BOLD_GREEN}├ SameSite  : {RESET}{sameSite}")
                print(f"{BOLD_GREEN}├ Secure    : {RESET}{secure}")
                print(f"{BOLD_GREEN}└ HTTP Only : {RESET}{httpOnly}")
                if cookies.index(cookie) != len(cookies) - 1:
                    print("")
        else:
            print(f"{BOLD_RED}No cookies found.{RESET}")

        return cookies

    except Exception as e:
        print(f"{BOLD_RED}General error: {e}{RESET}")
        return None
