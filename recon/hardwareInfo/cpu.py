import psutil
import wmi

def getCpu():
    c = wmi.WMI()
    cpuModel = c.query("SELECT * FROM Win32_Processor")[0].Name.replace("(R)", "").replace("(TM)", "").strip()

    processorInfo = {
        "cpuModel": cpuModel,
        "cores": psutil.cpu_count(logical=False),
        "threads": psutil.cpu_count(logical=True),
        "baseClock": c.query("SELECT * FROM Win32_Processor")[0].MaxClockSpeed / 1000
    }

    return processorInfo
