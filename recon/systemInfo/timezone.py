from datetime import datetime
import time

def getDateTimeInfo():

    current_datetime = datetime.now()

    timezone_offset = -time.timezone // 3600

    date_time_info = {
        "currentDate": current_datetime.strftime("%Y-%m-%d"),
        "currentTime": current_datetime.strftime("%H:%M:%S"),
        "timezone": f"UTC{timezone_offset:+d}"
    }

    return date_time_info