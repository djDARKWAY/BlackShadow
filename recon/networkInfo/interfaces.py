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
        services = [
            ("https://ipinfo.io/json", "ip", "org", "country", "region", "city"),
            ("http://ip-api.com/json", "query", "isp", "country", "regionName", "city"),
            ("https://api64.ipify.org?format=json", "ip", None, None, None, None)
        ]
        publicIpv4, publicIpv6 = "-", "-"
        geoData = {"isp": "-", "country": "-", "region": "-", "city": "-"}
        for url, ip_key, isp_key, country_key, region_key, city_key in services:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    ip = data.get(ip_key, "-")
                    if ":" in ip:
                        publicIpv6 = ip
                    else:
                        publicIpv4 = ip
                    if isp_key:
                        geoData.update({
                            "isp": data.get(isp_key, "-"),
                            "country": data.get(country_key, "-"),
                            "region": data.get(region_key, "-"),
                            "city": data.get(city_key, "-")
                        })
                    if publicIpv4 != "-" and publicIpv6 != "-":
                        break
            except requests.RequestException:
                continue
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
            interfaces.append({
                "interface": interface,
                "ipv4": ipv4,
                "ipv6": ipv6,
                "netmask": netmask
            })
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
