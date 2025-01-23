import wmi
import subprocess
import re
import os

def getMonitor():
    w = wmi.WMI()
    monitors = []

    # Pegar monitores físicos (PnP)
    pnpMonitors = w.query("SELECT * FROM Win32_PnPEntity WHERE Description LIKE '%Monitor%'")
    videoControllers = w.query("SELECT * FROM Win32_VideoController")

    dxdiag_data = getMonitorViaDxDiag()

    for idx, monitor in enumerate(pnpMonitors):
        try:
            if "Monitor" not in monitor.Name or "WAN Miniport" in monitor.Name:
                continue

            clean_name = re.sub(r'Generic Monitor\s*\((.*?)\)', r'\1', monitor.Name).strip()

            # Garantir que o índice de videoControllers seja válido
            video = videoControllers[idx] if idx < len(videoControllers) else None
            dxdiag_info = dxdiag_data[idx] if idx < len(dxdiag_data) else {}

            resolution = f"{video.CurrentHorizontalResolution}x{video.CurrentVerticalResolution}" if video else dxdiag_info.get("resolution", "Unknown")
            refreshRate = video.CurrentRefreshRate if video and video.CurrentRefreshRate != 0 else dxdiag_info.get("refreshRate", "Unknown")
            output = dxdiag_info.get("output", "Unknown")

            monitors.append({
                "monitorName": clean_name,
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
        dxdiag_file = "dxdiag_output.txt"
        
        subprocess.run(f"dxdiag /t {dxdiag_file}", shell=True, check=True)

        with open(dxdiag_file, "r") as file:
            dxdiag_data = file.readlines()

        monitor_info = []
        current_monitor = {}

        for line in dxdiag_data:
            if "Monitor Model" in line:
                current_monitor["monitorName"] = line.split(":")[1].strip()

            elif "Current Mode" in line:
                mode_match = re.search(r'(\d+) x (\d+)', line)
                refresh_match = re.search(r'(\d+)Hz', line)
                if mode_match:
                    current_monitor["resolution"] = f"{mode_match.group(1)}x{mode_match.group(2)}"
                if refresh_match:
                    current_monitor["refreshRate"] = refresh_match.group(1)

            elif "Output Type" in line:
                current_monitor["output"] = line.split(":")[1].strip()
                monitor_info.append(current_monitor)
                current_monitor = {}

        os.remove(dxdiag_file)  
        return monitor_info

    except Exception as e:
        print("Erro ao executar dxdiag:", e)
        return []
