import socket
import requests
import psutil

def getInterfaces():
    def getLocalIp():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            s.connect(('10.254.254.254', 1))
            return s.getsockname()[0]
        except Exception:
            return '-'
        finally:
            s.close()

    def getPublicIpAndGeo():
        publicIpv4, publicIpv6 = "-", "-"
        geoData = {"isp": "-", "country": "-", "region": "-", "city": "-", "lat": "-", "lon": "-", "zip": "-"}

        try:
            response = requests.get("https://ipinfo.io/json", timeout=5)
            if response.status_code == 200:
                data = response.json()
                publicIpv4 = data.get("ip", "-")
                geoData["isp"] = data.get("org", "-")
        except requests.RequestException:
            pass

        try:
            response = requests.get("https://api64.ipify.org?format=json", timeout=5)
            if response.status_code == 200:
                data = response.json()
                publicIpv6 = data.get("ip", "-")
        except requests.RequestException:
            pass

        try:
            response = requests.get("http://ip-api.com/json", timeout=5)
            if response.status_code == 200:
                data = response.json()
                geoData.update({
                    "country": data.get("country", "-"),
                    "region": data.get("regionName", "-"),
                    "city": data.get("city", "-"),
                    "lat": data.get("lat", "-"),
                    "lon": data.get("lon", "-"),
                    "zip": data.get("zip", "-")
                })
        except requests.RequestException:
            pass

        return publicIpv4, publicIpv6, geoData

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

    localIp = getLocalIp()
    publicIpv4, publicIpv6, geoData = getPublicIpAndGeo()
    interfaces = getNetworkInterfaces()

    return {
        "localIp": localIp,
        "publicIpv4": publicIpv4,
        "publicIpv6": publicIpv6,
        "geoData": geoData,
        "interfaces": interfaces
    }
