import subprocess

def getFirewall():
    try:
        result = subprocess.check_output("netsh advfirewall show allprofiles state", shell=True, stderr=subprocess.STDOUT)
        result = result.decode('utf-8')
        if "State" in result and "ON" in result:
            return "Active"
        else:
            return "Inactive"
    except subprocess.CalledProcessError as e:
        return {"error": f"Error checking firewall status: {e}"}