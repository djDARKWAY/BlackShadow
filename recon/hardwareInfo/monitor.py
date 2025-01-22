import wmi

def getMonitor():
    w = wmi.WMI()
    monitors = []
    
    for monitor in w.query("SELECT * FROM Win32_DesktopMonitor"):
        for video in w.query("SELECT * FROM Win32_VideoController"):
            monitors.append({
                "monitorName": monitor.Name,
                "displayIdentifier": f"\\\\.\\DISPLAY{video.DeviceID[-1]}",
                "resolution": monitor.ScreenWidth,
                "resolutionHeight": monitor.ScreenHeight,
            })
    
    return monitors
