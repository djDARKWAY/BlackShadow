import psutil

def getDisks():
    diskInfo = []

    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            total = usage.total / (1024 ** 3)
            used = usage.used / (1024 ** 3)
            free = usage.free / (1024 ** 3)
            filesystem = partition.fstype

            diskInfo.append({
                "mountPoint": partition.mountpoint,
                "filesystem": filesystem,
                "total": round(total, 2),
                "used": round(used, 2),
                "free": round(free, 2)
            })
        except PermissionError:
            continue

    return diskInfo
