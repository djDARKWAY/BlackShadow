import socket
import psutil

def getInterfaces():
    def getNetworkInterfaces():
        interfaces = []
        for interface, addrs in psutil.net_if_addrs().items():
            ipv4, ipv6, netmask = "-", "-", "-"
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    ipv4 = addr.address
                    netmask = addr.netmask if hasattr(addr, 'netmask') else "-"
                elif addr.family == socket.AF_INET6:
                    ipv6 = addr.address
            interfaces.append({"interface": interface, "ipv4": ipv4, "ipv6": ipv6, "netmask": netmask})
        return interfaces

    interfaces = getNetworkInterfaces()

    return {
        "interfaces": interfaces
    }
