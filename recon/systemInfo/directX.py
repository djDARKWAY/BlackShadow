import subprocess
import re

def getDirectXVersion():
    try:
        subprocess.check_output("dxdiag /t dxdiag_output.txt", shell=True, text=True)
        
        with open("dxdiag_output.txt", "r") as file:
            dxdiagData = file.read()

        match = re.search(r"DirectX Version:\s*(DirectX\s*\d+)", dxdiagData)

        subprocess.run("del dxdiag_output.txt", shell=True)

        if match:
            return match.group(1).replace("DirectX ", "")
        else:
            return "Unknown"
    except Exception as e:
        return str(e)
