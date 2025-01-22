import wmi
import psutil

memoryTypeMapping = {20: "DDR", 21: "DDR2", 24: "DDR3", 26: "DDR4", 27: "DDR5"}

def getRam():
    ramInfo = []

    totalRam = psutil.virtual_memory().total / (1024 ** 3)

    w = wmi.WMI()
    for ram in w.query("SELECT * FROM Win32_PhysicalMemory"):
        try:
            capacity = float(ram.Capacity) / (1024 ** 3) if ram.Capacity else 0
        except (ValueError, TypeError):
            capacity = 0

        ramInfo.append({
            "ramModel": ram.PartNumber.strip() if ram.PartNumber else "Unknown",
            "capacity": round(capacity, 2),
            "speed": int(ram.Speed) if ram.Speed and str(ram.Speed).isdigit() else "Unknown",
            "manufacturer": ram.Manufacturer if ram.Manufacturer else "Unknown",
            "type": memoryTypeMapping.get(ram.SMBIOSMemoryType, "Unknown")
        })

    ramInfo.insert(0, {"totalRam": round(totalRam, 2)})

    return ramInfo
