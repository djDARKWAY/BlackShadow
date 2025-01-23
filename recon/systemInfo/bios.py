import wmi
from datetime import datetime
import re

def getBiosInfo():
    c = wmi.WMI()
    bios = c.query("SELECT * FROM Win32_BIOS")[0]

    raw_date = bios.ReleaseDate.split('.')[0] if bios.ReleaseDate else "Unknown"
    formatted_date = (
        datetime.strptime(raw_date[:8], "%Y%m%d").strftime("%Y-%m-%d") if raw_date != "Unknown" else "Unknown"
    )

    version = bios.SMBIOSBIOSVersion.strip() if bios.SMBIOSBIOSVersion else "Unknown"

    serial_number = bios.SerialNumber.strip() if bios.SerialNumber else "Unknown"
    if serial_number.lower() in ["system serial number", "to be filled by oem"]:
        serial_number = "Not Available"

    bios_info = {
        "manufacturer": bios.Manufacturer.strip() if bios.Manufacturer else "Unknown",
        "version": version, 
        "releaseDate": formatted_date,
        "serialNumber": serial_number
    }

    return bios_info
