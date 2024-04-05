import hashlib
import os

from datetime import datetime, timezone

def ConvertTime(timeToConvert, since2001=True):
    """Smart and static method that converts time values.
    If timeToConvert is an integer, it is considered as UTC Unix time and will be converted to a Python datetime object with timezone set on UTC.
    If timeToConvert is a Python datetime object, converts to UTC Unix time integer.
    If since2001 is True (default), integer values start at 2001-01-01 00:00:00 UTC, not 1970-01-01 00:00:00 UTC (as standard Unix time).
    """

    apple2001reference = datetime(2001, 1, 1, tzinfo=timezone.utc)

    if type(timeToConvert) == int or type(timeToConvert) == float:
        # convert from UTC timestamp to datetime.datetime python object on UTC timezone
        if since2001:
            return datetime.fromtimestamp(timeToConvert + apple2001reference.timestamp(), timezone.utc)
        else:
            return datetime.fromtimestamp(timeToConvert, timezone.utc)

    if isinstance(timeToConvert, datetime):
        # convert from timezone-aware datetime Python object to UTC UNIX timestamp
        if since2001:
            return (timeToConvert - apple2001reference).total_seconds()
        else:
            return timeToConvert.timestamp()

def CalculateSHA256(databasePath):

    with open(databasePath, 'rb') as file:
        hashSHA256 = hashlib.sha256()
        while True:
            chunk = file.read(8192)
            if not chunk:
                break
            hashSHA256.update(chunk)
        return hashSHA256.hexdigest()

def CalculateMD5(databasePath):

    with open(databasePath, 'rb') as file:
        hashMD5 = hashlib.md5()
        while True:
            chunk = file.read(8192)
            if not chunk:
                break
            hashMD5.update(chunk)
        return hashMD5.hexdigest()

def GetFileSize(filePath):
    try:
        # Get the file size in bytes
        bytesSize = os.path.getsize(filePath)

        # Convert bytes to megabytes (1 MB = 1024 * 1024 bytes)
        mbSize = bytesSize / (1024 * 1024)

        return mbSize
    except FileNotFoundError:
        return None  # Handle the case where the file does not exist