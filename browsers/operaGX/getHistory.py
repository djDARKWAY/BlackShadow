import os
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from utils.ansiColors import BOLD_RED, BOLD_GREEN, GRAY, RESET
from utils.logo import showLogo as showLogoUtils

def getHistory():
    try:
        if os.system("tasklist | findstr opera.exe") == 0:
            os.system("taskkill /F /IM opera.exe")
            os.system('cls' if os.name == 'nt' else 'clear')

        showLogoUtils()

        dbPath = Path(os.path.expanduser("~")) / 'AppData/Roaming/Opera Software/Opera GX Stable/History'

        temp_db = Path(os.getenv("TEMP")) / "OperaGX_History.db"
        with open(dbPath, "rb") as src, open(temp_db, "wb") as dst:
            dst.write(src.read())

        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT url, title, last_visit_time 
            FROM urls 
            ORDER BY last_visit_time DESC
        """)

        history_list = []
        for row in cursor.fetchall():
            url = row[0]
            title = row[1] if row[1] else "Unknown"
            timestamp = row[2]

            if timestamp and timestamp > 11644473600000000:
                visit_time = datetime(1601, 1, 1) + timedelta(microseconds=timestamp)
                visit_time = visit_time.strftime('%Y-%m-%d %H:%M:%S')
            else:
                visit_time = "Unknown"

            history_list.append({
                "url": url,
                "title": title,
                "visit_time": visit_time
            })

        conn.close()
        os.remove(temp_db)

        if history_list:
            print("==========================================")
            print("      ** HISTORY OF VISITED SITES **      ")
            print("==========================================")
            for item in history_list:
                print(f"{BOLD_GREEN}► {GRAY}{item['title']}")
                print(f"{BOLD_GREEN}├ URL        : {RESET}{item['url']}")
                print(f"{BOLD_GREEN}└ Visit Time : {RESET}{item['visit_time']}")
                if history_list.index(item) != len(history_list) - 1:
                    print("")
        else:
            print(f"{BOLD_RED}No history found.{RESET}")
            
        return history_list

    except Exception as e:
        print(f"{BOLD_RED}Error retrieving history: {e}{RESET}")
        return None
