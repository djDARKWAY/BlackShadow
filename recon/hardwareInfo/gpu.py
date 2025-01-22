import wmi
import subprocess as sp

def getGpu():
    w = wmi.WMI()
    gpuInfo = []
    
    for gpu in w.query("SELECT * FROM Win32_VideoController"):
        if gpu.AdapterRAM > 0:
            memory = gpu.AdapterRAM / (1024 ** 2)
        else:
            if "NVIDIA" in gpu.Name:
                memory = getNvidiaMemory()
            elif "AMD" in gpu.Name:
                memory = getAmdMemory(gpu.Name)
            else:
                memory = 0.0

        gpuInfo.append({
            "gpuModel": gpu.Name,
            "memory": memory,
            "driverVersion": gpu.DriverVersion
        })

    return gpuInfo

def getNvidiaMemory():
    try:
        sp.check_output(["nvidia-smi"], stderr=sp.STDOUT)
        command = "nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits"
        memoryInfo = sp.check_output(command.split()).decode('ascii').strip()
        return float(memoryInfo)
    except (sp.CalledProcessError, FileNotFoundError):
        return 0.0

def getAmdMemory(gpuName):
    try:
        command = f"wmic path win32_videocontroller where \"caption='{gpuName}'\" get AdapterRAM"
        memoryInfo = sp.check_output(command, shell=True).decode('ascii').strip().split("\n")[-1]
        memory = int(memoryInfo) / (1024 ** 2)
        return memory
    except (sp.CalledProcessError, FileNotFoundError, ValueError):
        return 0.0
