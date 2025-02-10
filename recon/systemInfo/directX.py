import subprocess
import re
import os

def getDirectXVersion():
    try:
        dxdiagFile = "./utils/dxdiag/dxdiag_output.txt"

        with open(dxdiagFile, "r") as file:
            dxdiagData = file.readlines()

        match = re.search(r"DirectX Version:\s*(DirectX\s*\d+)", dxdiagData)

        if match:
            return match.group(1).replace("DirectX ", "")
        else:
            return "Unknown"
    except Exception as e:
        return str(e)
