import wmi
from datetime import datetime

def getBios():
    c = wmi.WMI()
    bios = c.query("SELECT * FROM Win32_BIOS")[0]

    rawDate = bios.ReleaseDate.split('.')[0] if bios.ReleaseDate else "Unknown"
    formattedDate = (
        datetime.strptime(rawDate[:8], "%Y%m%d").strftime("%Y-%m-%d") if rawDate != "Unknown" else "Unknown"
    )

    version = bios.SMBIOSBIOSVersion.strip() if bios.SMBIOSBIOSVersion else "Unknown"

    serialNumber = bios.SerialNumber.strip() if bios.SerialNumber else "Unknown"
    if serialNumber.lower() in ["system serial number", "to be filled by oem"]:
        serialNumber = "Not Available"

    biosInfo = {
        "manufacturer": bios.Manufacturer.strip() if bios.Manufacturer else "Unknown",
        "version": version, 
        "releaseDate": formattedDate,
        "serialNumber": serialNumber
    }

    return biosInfo
