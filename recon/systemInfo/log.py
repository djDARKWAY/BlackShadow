import win32evtlog
import win32evtlogutil

def getSystemLogs(log_type="System", num_records=100):
    server = "localhost"
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    hand = win32evtlog.OpenEventLog(server, log_type)

    logs = []
    while num_records > 0:
        events = win32evtlog.ReadEventLog(hand, flags, 0)
        if not events:
            break
        for event in events:
            try:
                description = win32evtlogutil.FormatMessage(event, hand)
            except:
                description = None

            if not description:
                if event.StringInserts:
                    description = "|".join(event.StringInserts)
                else:
                    description = "No description available"

            logs.append({
                "time": event.TimeGenerated.Format(),
                "source": event.SourceName,
                "event_id": event.EventID,
                "category": event.EventCategory,
                "message": description
            })
            num_records -= 1
            if num_records <= 0:
                break
    win32evtlog.CloseEventLog(hand)
    return logs
