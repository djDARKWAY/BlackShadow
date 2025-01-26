from datetime import datetime
import time

def getDateTime():

    currentDateTime = datetime.now()

    timezoneOffset = -time.timezone // 3600

    dateTimeInfo = {
        "currentDate": currentDateTime.strftime("%Y-%m-%d"),
        "currentTime": currentDateTime.strftime("%H:%M:%S"),
        "timezone": f"UTC{timezoneOffset:+d}"
    }

    return dateTimeInfo