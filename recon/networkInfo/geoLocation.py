import socket
import requests

def getGeoLocation():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('10.254.254.254', 1))
        localIp = s.getsockname()[0]
    except Exception:
        localIp = '-'
    finally:
        s.close()

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

    return {
        "localIp": localIp,
        "publicIpv4": publicIpv4,
        "publicIpv6": publicIpv6,
        "geoData": geoData
    }
