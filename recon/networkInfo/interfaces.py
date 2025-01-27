import socket
import requests
import psutil

def getInterfaces():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('10.254.254.254', 1))
        localIp = s.getsockname()[0]
    except Exception:
        localIp = '-'
    finally:
        s.close()

    try:
        response = requests.get('https://api64.ipify.org?format=json')
        publicIp = response.json()['ip']
    except requests.RequestException:
        publicIp = '-'

    interfaces = []
    for interface, addrs in psutil.net_if_addrs().items():
        ipv4, ipv6, netmask = '-', '-', '-'
        for addr in addrs:
            if addr.family == socket.AF_INET:
                ipv4 = addr.address
                netmask = addr.netmask if hasattr(addr, 'netmask') else '-'
            elif addr.family == socket.AF_INET6:
                ipv6 = addr.address
        interfaces.append({
            'interface': interface,
            'ipv4': ipv4,
            'ipv6': ipv6,
            'netmask': netmask
        })

    networkDetails = {
        "localIp": localIp,
        "publicIp": publicIp,
        "interfaces": interfaces
    }
    return networkDetails
