import psutil
import wmi

def getCpu():
    c = wmi.WMI()
    processor = c.query("SELECT Name, MaxClockSpeed FROM Win32_Processor")[0]
    
    cpuModel = processor.Name.replace("(R)", "").replace("(TM)", "").strip()
    
    processorInfo = {
        "cpuModel": cpuModel,
        "cores": psutil.cpu_count(logical=False),
        "threads": psutil.cpu_count(logical=True),
        "baseClock": processor.MaxClockSpeed / 1000 
    }
    
    return processorInfo