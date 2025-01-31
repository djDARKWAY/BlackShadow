import subprocess

def getWindowsDefender():
    try:
        command = "powershell Get-MpComputerStatus"
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        
        status = {}
        for line in result.splitlines():
            if ':' in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                
                if key in ["AntivirusEnabled", "RealTimeProtectionEnabled", "BehaviorMonitorEnabled", "FirewallStatus", "IsTamperProtected", "DefenderSignaturesOutOfDate", 
                           "AntivirusSignatureVersion", "AntispywareEnabled", "LastFullScanTime", "LastQuickScanTime", 
                           "SmartAppControlState", "IoavProtectionEnabled", "AntivirusSignatureLastUpdated", "TamperProtectionSource", "TDTCapable"]:
                    
                    if key == "AntivirusEnabled":
                        value = "Enabled" if value == "True" else "Disabled"
                    elif key == "LastFullScanTime" or key == "LastQuickScanTime":
                        value = f"Last scan: {value}"
                    
                    status[key] = value
        
        return status
    
    except subprocess.CalledProcessError as e:
        return {"error": f"Error calling PowerShell: {e.output}"}
