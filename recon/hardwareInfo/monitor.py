import wmi
import subprocess
import re
import os

def getMonitor():
    w = wmi.WMI()
    monitors = []

    pnpMonitors = w.query("SELECT * FROM Win32_PnPEntity WHERE Description LIKE '%Monitor%'")
    videoControllers = w.query("SELECT * FROM Win32_VideoController")

    dxdiagData = getMonitorViaDxDiag()

    for idx, monitor in enumerate(pnpMonitors):
        try:
            if "Monitor" not in monitor.Name or "WAN Miniport" in monitor.Name:
                continue

            cleanName = re.sub(r'Generic Monitor\s*\((.*?)\)', r'\1', monitor.Name).strip()

            video = videoControllers[idx] if idx < len(videoControllers) else None
            dxdiagInfo = dxdiagData[idx] if idx < len(dxdiagData) else {}

            resolution = f"{video.CurrentHorizontalResolution}x{video.CurrentVerticalResolution}" if video else dxdiagInfo.get("resolution", "Unknown")
            refreshRate = video.CurrentRefreshRate if video and video.CurrentRefreshRate != 0 else dxdiagInfo.get("refreshRate", "Unknown")
            output = dxdiagInfo.get("output", "Unknown")

            monitors.append({
                "monitorName": cleanName,
                "displayIdentifier": f"\\\\.\\DISPLAY{idx + 1}",
                "resolution": resolution,
                "refreshRate": refreshRate,
                "output": output
            })
        except Exception as e:
            monitors.append({
                "monitorName": "Unknown Monitor",
                "displayIdentifier": f"\\\\.\\DISPLAY{idx + 1}",
                "resolution": "Unknown",
                "refreshRate": "Unknown",
                "output": "Unknown"
            })
    
    return monitors

def getMonitorViaDxDiag():
    try:
        dxdiagFile = "dxdiag_output.txt"
        
        subprocess.run(f"dxdiag /t {dxdiagFile}", shell=True, check=True)

        with open(dxdiagFile, "r") as file:
            dxdiagData = file.readlines()

        monitorInfo = []
        currentMonitor = {}

        for line in dxdiagData:
            if "Monitor Model" in line:
                currentMonitor["monitorName"] = line.split(":")[1].strip()

            elif "Current Mode" in line:
                modeMatch = re.search(r'(\d+) x (\d+)', line)
                refreshMatch = re.search(r'(\d+)Hz', line)
                if modeMatch:
                    currentMonitor["resolution"] = f"{modeMatch.group(1)}x{modeMatch.group(2)}"
                if refreshMatch:
                    currentMonitor["refreshRate"] = refreshMatch.group(1)

            elif "Output Type" in line:
                currentMonitor["output"] = line.split(":")[1].strip()
                monitorInfo.append(currentMonitor)
                currentMonitor = {}

        os.remove(dxdiagFile)  
        return monitorInfo

    except Exception as e:
        print("Error executing dxdiag:", e)
        return []
