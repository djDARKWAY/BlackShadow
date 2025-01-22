import wmi
import subprocess as sp
import pyopencl as cl

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
                memory = getAmdMemory()
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

def getAmdMemory():
    platforms = cl.get_platforms()
    for platform in platforms:
        if "AMD" in platform.name:
            devices = platform.get_devices()
            for device in devices:
                return device.global_mem_size / (1024 ** 2)
    return 0.0
