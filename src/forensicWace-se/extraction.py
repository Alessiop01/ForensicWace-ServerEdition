import plistlib
import os

import utils

#region Data Types

iosInfoFiles = {
    'manifest': 'Manifest.plist',
    'manifestDB': 'Manifest.db',
    'info': 'Info.plist',
    'status': 'Status.plist'
}

#endregion

def GetDeviceExtractionList(deviceExtractionPath):

    toReturnList = []

    if deviceExtractionPath:
        (_, dirnames, _) = next(os.walk(deviceExtractionPath))

        for i in dirnames:
            GetDeviceBasicInfo(udid=i, path=deviceExtractionPath)
            toReturnList.append(GetDeviceBasicInfo(udid=i, path=deviceExtractionPath))

        return toReturnList
    else:
        raise Exception("Need valid backup root folder path passed through 'deviceExtractionPath'.")

def GetDeviceBasicInfo(udid, path):

    if udid and path:
        manifestFile = os.path.join(path, udid, iosInfoFiles['manifest'])
        info = {}
        try:
            with open(manifestFile, 'rb') as infile:
                manifest = plistlib.load(infile)
        except FileNotFoundError:
            print(f"{udid} under {path} doesn't seem to have a manifest file.")
            return None
        info = {
            "udid": udid,
            "name": manifest['Lockdown']['DeviceName'],
            "ios": manifest['Lockdown']['ProductVersion'],
            "serial": manifest['Lockdown']['SerialNumber'],
            "type": manifest['Lockdown']['ProductType'],
            "date": utils.ConvertTime(os.path.getmtime(manifestFile), since2001=False),
        }
    else:
        raise Exception("Need valid backup root folder path and a device UDID.")

    return info