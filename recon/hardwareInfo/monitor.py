import wmi
import re
import os

def getMonitor():
    w = wmi.WMI()
    monitors = []
    
    pnpMonitors = w.query("SELECT * FROM Win32_PnPEntity WHERE Description LIKE '%Monitor%'")
    videoControllers = w.query("SELECT * FROM Win32_VideoController")

    dxdiagData = None

    for idx, monitor in enumerate(pnpMonitors):
        if "Monitor" not in monitor.Name or "WAN Miniport" in monitor.Name:
            continue

        cleanName = re.sub(r'Generic Monitor\s*\((.*?)\)', r'\1', monitor.Name).strip()
        video = videoControllers[idx] if idx < len(videoControllers) else None

        resolution = f"{video.CurrentHorizontalResolution}x{video.CurrentVerticalResolution}" if video else "Unknown"
        refreshRate = video.CurrentRefreshRate if video and video.CurrentRefreshRate != 0 else "Unknown"
        output = "Unknown"

        if resolution == "Unknown" or refreshRate == "Unknown":
            if dxdiagData is None:
                dxdiagData = getMonitorViaDxDiag()

            dxdiagInfo = dxdiagData[idx] if idx < len(dxdiagData) else {}
            resolution = dxdiagInfo.get("resolution", resolution)
            refreshRate = dxdiagInfo.get("refreshRate", refreshRate)
            output = dxdiagInfo.get("output", output)

        monitors.append({
            "monitorName": cleanName,
            "displayIdentifier": f"\\\\.\\DISPLAY{idx + 1}",
            "resolution": resolution,
            "refreshRate": refreshRate,
            "output": output
        })

    return monitors


def getMonitorViaDxDiag():
    dxdiagFile = "./utils/dxdiag/dxdiag_output.txt"

    if not os.path.exists(dxdiagFile):
        print(f"Erro: O ficheiro {dxdiagFile} não existe.")
        return []

    monitorInfo = []
    currentMonitor = {}

    try:
        with open(dxdiagFile, "r", encoding="utf-8") as file:
            for line in file:
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

    except Exception as e:
        print(f"Erro ao ler {dxdiagFile}: {e}")

    return monitorInfo
