import psutil
import json

def getOpenPorts(protocolFile='./utils/jsons/protocols.json', filterStates=None):
    if filterStates is None:
        filterStates = ["ESTABLISHED", "LISTEN", "CLOSE_WAIT", "TIME_WAIT", "SYN", "CLOSING", "FIN_WAIT", "NONE"]

    with open(protocolFile, 'r') as file:
        protocols = json.load(file)

    connections = psutil.net_connections(kind='inet')

    if not connections:
        print("No active network connections")
        return

    connectionsInfo = []

    for conn in connections:
        if conn.status not in filterStates:
            continue

        localAddress = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "-"
        remoteAddress = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
        status = conn.status if conn.status else "NONE"
        pid = conn.pid if conn.pid else "-"
        
        protocol = protocols.get(str(conn.type), str(conn.type))

        connectionInfo = {
            "Local Address": localAddress,
            "Remote Address": remoteAddress,
            "Status": status,
            "PID": pid,
            "Protocol": protocol
        }
        connectionsInfo.append(connectionInfo)

    return connectionsInfo
