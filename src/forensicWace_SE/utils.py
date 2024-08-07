import hashlib
import os
import re
import binascii

import forensicWace_SE.globalConstants as globalConstants

from datetime import datetime, timezone
from protobuf_decoder.protobuf_decoder import Parser

def ConvertTime(timeToConvert, since2001=True):
    """Converts time values.
    If timeToConvert is an integer, it is considered as UTC Unix time and will be converted to a Python datetime object with timezone set on UTC.
    If timeToConvert is a Python datetime object, converts to UTC Unix time integer.
    If since2001 is True (default), integer values start at 2001-01-01 00:00:00 UTC, not 1970-01-01 00:00:00 UTC (as standard Unix time).
    """

    apple2001reference = datetime(2001, 1, 1, tzinfo=timezone.utc)

    if type(timeToConvert) == int or type(timeToConvert) == float:
        # Convert from UTC timestamp to datetime.datetime python object on UTC timezone
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
    """Calculate SHA256 hash of a file.
    The file path is taken as input parameter"""
    with open(databasePath, 'rb') as file:
        hashSHA256 = hashlib.sha256()
        while True:
            chunk = file.read(8192)
            if not chunk:
                break
            hashSHA256.update(chunk)
        return hashSHA256.hexdigest()

def CalculateMD5(databasePath):
    """Calculate MD5 hash of a file.
    The file path is taken as input parameter."""
    with open(databasePath, 'rb') as file:
        hashMD5 = hashlib.md5()
        while True:
            chunk = file.read(8192)
            if not chunk:
                break
            hashMD5.update(chunk)
        return hashMD5.hexdigest()

def GetFileSize(filePath):
    """Gets the file size in Bytes and converts to MegaBytes.
    The file path is taken as input parameter.
    If an error occurs, will return None."""
    try:
        # Get the file size in bytes
        bytesSize = os.path.getsize(filePath)

        # Convert bytes to megabytes (1 MB = 1024 * 1024 bytes)
        mbSize = bytesSize / (1024 * 1024)

        return mbSize
    except FileNotFoundError:
        return None  # Handle the case where the file does not exist

def FormatPhoneNumber(inputPhoneNumber):
    """Formats the input phone number into one of the following formats:
    xxx xxx xxxx
    +x xxx xxx xxxx
    +xx xxx xxx xxxx
    +xxx xxx xxx xxxx
    If the input phone number does not contains the + symbol but contains a prefix, the function will automatically add + symbol.
    If the input phone number does not contains a prefix, it will be formatted without considering any prefix."""

    # Define the regex pattern for prefix (optional) and phone number
    pattern = r'(?:(?:\+)?(\d{1,3})\s*)?(\d{3})\s*(\d{3})\s*(\d{4})'

    # Use regex to find prefix and phone number
    match = re.match(pattern, inputPhoneNumber)
    if match:
        prefix = "+" + match.group(1) if match.group(1) else ""  # Add "+" to the prefix if needed
        phoneNumber = f"{match.group(2)} {match.group(3)} {match.group(4)}"
        return f"{prefix} {phoneNumber}"
    else:
        return globalConstants.invalidPhoneNumber

def FormatPhoneNumberForPageTables(inputPhoneNumber):
    """This function is a duplicate of the function "formatPhoneNumber".
    The only difference is the return value in case the phone number does not match the given pattern.
    Formats the input phone number into one of the following formats:
    xxx xxx xxxx
    +x xxx xxx xxxx
    +xx xxx xxx xxxx
    +xxx xxx xxx xxxx
    If the input phone number does not contains the + symbol but contains a prefix, the function will automatically add + symbol.
    If the input phone number does not contains a prefix, it will be formatted without considering any prefix."""

    # Define the regex pattern for prefix (optional) and phone number
    pattern = r'(?:(?:\+)?(\d{1,3})\s*)?(\d{3})\s*(\d{3})\s*(\d{4})'

    # Use regex to find prefix and phone number
    match = re.match(pattern, inputPhoneNumber)
    if match:
        prefix = "+" + match.group(1) if match.group(1) else ""  # Add "+" to the prefix if needed
        phoneNumber = f"{match.group(2)} {match.group(3)} {match.group(4)}"
        return f"{prefix} {phoneNumber}"
    else:
        return inputPhoneNumber

def GetSentDateTime(blob):
    if (blob != None):
        hexData = binascii.hexlify(blob).decode()
        parsedData = Parser().parse(hexData)

        class ParsedResult:
            def __init__(self, field, wire_type, data):
                self.field = field
                self.wire_type = wire_type
                self.data = data

        class ParsedResults:
            def __init__(self, results):
                self.results = results

        field3Value = None
        for result in parsedData.results:
            if result.field == 3:
                field3Value = result.data
                break

        gmtDateTime = datetime.fromtimestamp(field3Value, tz=timezone.utc)
        messageDateTime = gmtDateTime.strftime('%Y-%m-%d %H:%M:%S %Z')

        return messageDateTime
    else:
        return globalConstants.infoNotAvailable

def GetReadDateTime(blob):
    if (blob != None):
        hexData = binascii.hexlify(blob).decode()
        parsedData = Parser().parse(hexData)

        class ParsedResult:
            def __init__(self, field, wire_type, data):
                self.field = field
                self.wire_type = wire_type
                self.data = data

        class ParsedResults:
            def __init__(self, results):
                self.results = results

        field3Value = None
        for result in parsedData.results:
            if result.field == 3:
                field3Value = result.data
                break

        field5InField2 = None
        for result in parsedData.results:
            if result.field == 2:
                for subResult in result.data.results:
                    if subResult.field == 5:
                        field5InField2 = subResult.data
                        break

        if(field5InField2 != None):
            readTimestamp = int(field3Value) + int(field5InField2)
            gmtDateTime = datetime.fromtimestamp(readTimestamp, tz=timezone.utc)
            messageDateTime = gmtDateTime.strftime('%Y-%m-%d %H:%M:%S %Z')
        else:
            messageDateTime = globalConstants.infoNotAvailable

        return messageDateTime
    else:
        return globalConstants.infoNotAvailable

def DeleteFilesIfExist(filePathArray):
    for filePath in filePathArray:
        if os.path.isfile(filePath):
            os.remove(filePath)
            print(f"Deleted file: {filePath}")
        else:
            print(f"File not found: {filePath}")

def VcardTelExtractor(vcardText):
    # Pattern to extract phone number
    phoneNumberPattern = re.compile(r"TEL(?:;[^:]*):(\+?\d+(?: \d+)*)")

    # Retrieve all phone numbers in VCARD
    phoneNumber = phoneNumberPattern.findall(vcardText)

    print("Retrieved phone number:")
    print(phoneNumber)

    if not phoneNumber:
        phoneNumber = ["Number not available"]

    return phoneNumber