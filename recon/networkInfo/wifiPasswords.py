import subprocess
import re

def isWlanServiceRunning():
    try:
        result = subprocess.check_output(["sc", "query", "wlansvc"], universal_newlines=True, encoding="utf-8", errors="ignore")
        return "RUNNING" in result
    except subprocess.CalledProcessError:
        return False

def getWifiPasswords():
    if not isWlanServiceRunning():
        return {"error": "The WLAN AutoConfig (wlansvc) service is not running. Please start it to retrieve Wi-Fi networks."}

    try:
        command = ["netsh", "wlan", "show", "profiles"]
        output = subprocess.check_output(command, universal_newlines=True, encoding="utf-8", errors="ignore")

        profiles = re.findall(r"All User Profile\s*:\s*(.*)", output)

        if not profiles:
            return {"error": "No stored Wi-Fi networks found."}

        wifiCredentials = []
        for profile in profiles:
            profile = profile.strip()
            try:
                command = ["netsh", "wlan", "show", "profile", profile, "key=clear"]
                result = subprocess.check_output(command, universal_newlines=True, encoding="utf-8", errors="ignore")

                passwordMatch = re.search(r"Key Content\s*:\s*(.*)", result)
                password = passwordMatch.group(1) if passwordMatch else "-"

                wifiCredentials.append({"SSID": profile, "Password": password})

            except subprocess.CalledProcessError:
                wifiCredentials.append({"SSID": profile, "Password": "Failed"})

        return wifiCredentials

    except Exception as e:
        return {"error": f"Error executing netsh command: {str(e)}"}
