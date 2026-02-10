from datetime import datetime

def getTime():
    currentTime = str(datetime.now())
    currentTime = currentTime.replace(' ', 'T')
    currentTime = currentTime.replace(':', '_')
    currentTime = currentTime[:19]
    return currentTime