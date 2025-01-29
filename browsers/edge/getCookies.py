import os
from pathlib import Path
import rookiepy
from datetime import datetime

RESET = "\033[0m"
BOLD_GREEN = "\033[1;32m"
BOLD_RED = "\033[1;31m"
GRAY = "\033[90m"

def getCookies():
    try:
        # Check if the Edge browser is open and close it if necessary
        if os.system("tasklist | findstr msedge.exe") == 0:
            os.system("taskkill /F /IM msedge.exe")
            os.system('cls' if os.name == 'nt' else 'clear')

        localappdata = os.getenv('LOCALAPPDATA')
        dbPath = Path(localappdata) / 'Microsoft/Edge/User Data/Default/Network/Cookies'
        keyPath = Path(localappdata) / 'Microsoft/Edge/User Data/Local State'

        # Use rookiepy to extract cookies
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
                sameSite = cookie.get('same_site', 'N/A')
                if sameSite == -1:
                    sameSite = "Unspecified" # The browser will decide whether to send the cookie based on the request type
                elif sameSite == 0:
                    sameSite = "Strict" # Cookies are sent only to the same site
                elif sameSite == 1:
                    sameSite = "Lax" # Cookies are sent to the same site and to the some third-party sites
                else:
                    sameSite = "Unknown"

                # Converting the expiration date to a readable format if it is a timestamp
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